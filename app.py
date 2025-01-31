import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi


load_dotenv() ##load all environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Youtube video summarizer. You will be taking the transcript text 
and summairzing the entire video and providing the important summary in points
within 250 words. Please provde the summary of transcript provided here:  """

## getting transcript data from YT Video ID
def extract_transcript_details(video_url):
    try:
        video_id=video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id,languages=['en','en-IN','hi'])
        transcrpt=""
        for i in transcript_text:
            transcrpt+=" " + i["text"]
        return transcrpt

    except Exception as e:
        raise e

## getting the summary based on prompt from google gemini
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt+transcript_text)
    return response.text

## Streamlit UI

st.title("Youtube transcript to detail notes convertor")
youtube_link=st.text_input("Enter Youtbe Video Link:")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.write(summary)


