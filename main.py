import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re
from dotenv import load_dotenv
import streamlit.components.v1 as components

load_dotenv()


openai.api_key = st.secrets["OPEN_AI"]

def extract_youtube_video_id(url):
    
    found = re.search(r"(?:youtu\.be\/|watch\?v=)([\w-]+)", url)
    if found:
        return found.group(1)
    return None

def get_video_transcript(video_id):
   
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
    except TranscriptsDisabled:
        # The video doesn't have a transcript
        return None

    text = " ".join([line["text"] for line in transcript])
    
    return text

def generate_summary(text):
   
    instructions = """Eres un generador de contenido para una empresa. Recibes subtitulos de vídeos de Youtube y con ellos generas artículos para un blog.
    El artículo que generes debe de ser muy detallado, en un tono muy profesional, y fácil de leer. Los pasos que debes seguir son los
    siguientes: 
    1. Leer todo la transcripción.
    2. Dividir la transcripción en secciones.
    3. Escribir un artículo para blog que contenga todos los elementos clave de la charla.
    4. Devuelveme el artículo entre tags html con texto blanco."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ],
        temperature=0.1,
        n=1,
        
    )

    # Return the generated summary
    return response.choices[0].message.content.strip()


st.title("Generador contenido Youtube Aire Limpio:")
url = st.text_input("Introduce la url del webinar que quieras convertir", "")

if url:
    id =  extract_youtube_video_id(url)
    text = get_video_transcript(id)
    summary = generate_summary(text)
    components.html(summary, height=2500)
    
    
