from whispercpp import Whisper
import os

class Transcriber:
    def __init__(self):
        self.model = Whisper("tiny")

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        text = self.model.extract_text(result)
        text = "".join(text).strip()
        self.cleanup(audio_path)
        return text
    
    def cleanup(self, audio_path):
        os.remove(audio_path)