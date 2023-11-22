import streamlit as st
import requests
from celery.result import AsyncResult
from celery_tasks import celery
import time
import math
from config import Config

def main():

    if 'transcribe_button' in st.session_state and st.session_state.transcribe_button == True:
        st.session_state.running = True
    else:
        st.session_state.running = False

    st.write("Audio Transcription App")
    
    uploaded_file = st.file_uploader("Choose an audio file", type=Config.ALLOWED_EXTENSIONS)

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav', start_time=0)

        if st.button("Transcribe", disabled=st.session_state.running, key="transcribe_button"):
            response = transcribe_audio(uploaded_file)

            task = AsyncResult(response["task_id"], app=celery)
            status_container = st.empty()
            status_container.write("Transcribing please wait...")

            status = st.progress(0) 
            t = 0
            while task.state != "SUCCESS":
                time.sleep(1)
                task = AsyncResult(response["task_id"], app=celery)
                if task.state == "FAILURE":
                    st.error('Sorry! There was some issue in transcribing your audio. Please try again...', icon="🚨")
                    break
                if task.state == "SUCCESS":
                    status.progress(1)
                else:
                    status.progress(min(0.95, (t+1)/math.ceil(response["audio_length"])))
                    
                t+=1

            status.empty()
            if task.state == "SUCCESS":
                status_container.write("Transcription completed :tada: :partying_face:")
                st.write(f"Transcription:")
                st.write(task.result)
                st.snow()
            else:
                status_container.empty()

            st.session_state.output = "Done"

            

def transcribe_audio(audio_file):
    url = "http://flask-app:5000/transcribe"
    files = {'file': audio_file}
    response = requests.post(url, files=files)
    return response.json()

if __name__ == '__main__':
    main()
