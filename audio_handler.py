import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from collections import deque
from pydub import AudioSegment


#Voice Analysis Detection Configuration
SILENCE_THRESHOLD = 600
SILENCE_DURATION = 1
SAMPLE_RATE = 44100
CHANNELS = 1
CHUNK_SIZE = 1024


#plays an audio file in chunks and stops immediately if the interrupt_event is set. 
def play_audio_interruptible(audio_file_path, interrupt_event):
    try:
        audio = AudioSegment.from_mp3(audio_file_path)
        audio = audio.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)
        audio_data = np.array(audio.get_array_of_samples(), dtype=np.int16)

        with sd.OutputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16') as stream:
            print("🔊 Playing response (interruptible)...")
            for i in range(0, len(audio_data), CHUNK_SIZE):
                if interrupt_event.is_set():
                    print("\nPlayback interrupted by user.")
                    stream.stop()
                    return
                chunk = audio_data[i:i + CHUNK_SIZE]
                stream.write(chunk)
            stream.close()
    except Exception as e:
        print(f"Error playing audio: {e}")

#Records Audio using Voice Analysis Detection.
def record_audio_vad(filename="input.wav", is_interruption=False):
    if is_interruption:
        print("Interruption detected, recording...")
    else:
        print("Listening... Speak when you're ready.")
    
    silent_chunks_needed = int(SILENCE_DURATION * SAMPLE_RATE / CHUNK_SIZE)
    silent_chunks = deque(maxlen=silent_chunks_needed)
    recorded_frames = []
    is_speaking = is_interruption 

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=CHUNK_SIZE, dtype='int16') as stream:
        if not is_interruption:
            while True:
                audio_chunk, _ = stream.read(CHUNK_SIZE)
                rms = np.sqrt(np.mean(audio_chunk.astype(np.float32)**2))
                if rms > SILENCE_THRESHOLD:
                    print("Speech detected, recording...")
                    is_speaking = True
                    recorded_frames.append(audio_chunk)
                    break
        
        while is_speaking:
            audio_chunk, _ = stream.read(CHUNK_SIZE)
            recorded_frames.append(audio_chunk)
            rms = np.sqrt(np.mean(audio_chunk.astype(np.float32)**2))
            if rms < SILENCE_THRESHOLD:
                silent_chunks.append(1)
            else:
                silent_chunks.clear()
            if len(silent_chunks) >= silent_chunks_needed:
                print("Silence detected. Finishing recording.")
                break
    
    if not recorded_frames:
        print("No speech was detected.")
        return None

    recording = np.concatenate(recorded_frames, axis=0)
    wav.write(filename, SAMPLE_RATE, recording)
    print(f"Audio saved to {filename}")
    return filename