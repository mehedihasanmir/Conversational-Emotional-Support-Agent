import audio_handler
import langchain_services as ls
import threading
import sounddevice as sd
import numpy as np


#Contunously listens for user speech to interrupt the ai.
def listen_for_interruption(interrupt_event):
    with sd.InputStream(samplerate=audio_handler.SAMPLE_RATE, 
                        channels=audio_handler.CHANNELS, 
                        blocksize=audio_handler.CHUNK_SIZE, 
                        dtype='int16') as stream:
        while not interrupt_event.is_set():
            audio_chunk, _ = stream.read(audio_handler.CHUNK_SIZE)
            rms = np.sqrt(np.mean(audio_chunk.astype(np.float32)**2))
            if rms > audio_handler.SILENCE_THRESHOLD:
                interrupt_event.set()
                break
            

#Prompts the user to select a voice for the AI.
def get_voice_selection():
    while True:
        choice = input("Choose a voice for the AI (male/female): ").lower()
        if choice == "male":
            return "alloy"
        elif choice == "female":
            return "nova"
        else:
            print("Invalid choice. Please type 'male' or 'female'.")
            
            
# store history as a list of message tuples compatible with MessagesPlaceholder e.g., ("human", "..."), ("ai", "...")            
def main():
    conversation_history: list[tuple[str, str]] = []
    ai_voice = get_voice_selection()
    print(f"Starting conversation...")
    
    is_interruption = False
    
    #Main Conversational Loop
    while True:
        if not is_interruption:
            audio_file = audio_handler.record_audio_vad()
        else:
            audio_file = audio_handler.record_audio_vad(is_interruption=True)
            is_interruption = False

        if audio_file is None: continue
            
        user_text = ls.speech_to_text(audio_file)
        if not user_text: continue
        if "goodbye" in user_text.lower(): break
            
        #NEW: Special handling for the first turn
        is_first_turn = not conversation_history
        if is_first_turn:
            print("Detecting initial emotion explicitly...")
            emotion = ls.emotion_chain.invoke({"input": user_text})
            print(f"Detected Emotion: **{emotion}**")

        conversation_history.append(("human", user_text))

        # Call the single, optimized response chain for a faster interaction.
        full_response = ""
        print("\nAI Assistant: ", end="", flush=True)
        # Pass the conversation history as a list of message tuples so
        # MessagesPlaceholder can format them into BaseMessage objects.
        stream = ls.response_chain.stream({
            "input": user_text,
            "history": conversation_history,
        })

        for chunk in stream:
            print(chunk, end="", flush=True)
            full_response += chunk
        print()

        conversation_history.append(("ai", full_response))

        response_audio_file = ls.text_t0_speech(full_response, voice=ai_voice)

        if response_audio_file:
            interrupt_event = threading.Event()
            playback_thread = threading.Thread(target=audio_handler.play_audio_interruptible, 
                                               args=(response_audio_file, interrupt_event))
            playback_thread.start()
            listen_for_interruption(interrupt_event)
            playback_thread.join()
            if interrupt_event.is_set():
                is_interruption = True
                continue
            

    #Post-Conversation Analysis
    print("\nOur conversation has ended. Generating analysis...")
    # Convert message tuples back into readable lines for post-conversation
    dialogue_lines = [f"User: {text}" if role in ("human", "user") else f"Assistant: {text}" for role, text in conversation_history]
    dialogue = "\n".join(dialogue_lines)
    
    analysis = ls.post_conversation_analyzer.invoke({"dialogue": dialogue})
    
    print("\nEmotional Journey Summary")
    print(analysis['summary'])
    print("\nEmotion Keywords")
    print(analysis['keywords'])

if __name__ == "__main__":
    main()