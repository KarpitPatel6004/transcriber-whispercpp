import uuid
from config import Config
from pydub import AudioSegment

def generate_unique_id(without_hyphen=True):
    if without_hyphen:
        return uuid.uuid4().hex
    else:
        return str(uuid.uuid4())
    
def preprocess_audio(audio_path):
        audio = AudioSegment.from_file(audio_path)
        trimmed_audio = audio[:Config.MAX_DURATION_MS]
        trimmed_audio = trimmed_audio.set_frame_rate(16000)
        trimmed_audio = trimmed_audio.set_channels(1)
        trimmed_audio = trimmed_audio.set_sample_width(2)
        trimmed_audio.export(audio_path, format="wav")

        return audio_path, trimmed_audio.duration_seconds