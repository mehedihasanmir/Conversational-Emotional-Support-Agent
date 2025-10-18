from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser


#Setup .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Openai key is not found.")


# Setup OpenAI client
client = OpenAI(api_key=api_key)

#Converts speech to text.
def speech_to_text(audio_file_path):
    print("Converting Audio to text....")
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(model="gpt-4o-transcribe", file=audio_file)
        return transcript.text
    except Exception as e:
        print(f"Error in STT: {e}")
        return None
    

#Converts text to speech with chosen voice.
def text_t0_speech(text, voice= "nova", filename= "response.mp3"):
    print("Converting respose to speech...")
    try:
        response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
        response.stream_to_file(filename)
        return filename
    except Exception as e:
        print(f"Error in TTS: {e}")
        return None


# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.6, openai_api_key=api_key)

# Dedicated Emotion Detection Chain (for first turn)
emotion_prompt = ChatPromptTemplate.from_template(
    "Analyze the following text and respond with a single word that best represents the user's primary emotion. "
    "Do not explain or add punctuation. Text: {input}"
)

emotion_chain = emotion_prompt | llm | StrOutputParser()


#Unified Coversational Chain with emphathy
empathy_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a world-class empathetic conversational AI. Your task is to respond to the user in a natural and supportive way.
     Follow these two steps in your internal thought process:
     1.  **Analyze Emotion**: Deeply analyze the user's text to identify their primary emotion.
     2.  **Generate Response**: Based on that detected emotion and the conversation history, generate a concise, empathetic, and context-aware response. Do not explicitly state the emotion you've detected."""),
    MessagesPlaceholder("history", optional=True),
    ("user", "{input}")
])
response_chain = empathy_prompt | llm | StrOutputParser()


#Post Conversation Analysis
summary_prompt = ChatPromptTemplate.from_template(
    "Analyze the following conversation and write a concise, 2-3 line summary of the user's emotional journey.\n\n---\n{dialogue}\n---"
)
summary_chain = summary_prompt | llm | StrOutputParser()

keywords_prompt = ChatPromptTemplate.from_template(
    "From the following conversation, extract the three most dominant emotion keywords. Respond with only the three words, separated by commas.\n\n---\n{dialogue}\n---"
)
keywords_chain = keywords_prompt | llm | StrOutputParser()

post_conversation_analyzer = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
)