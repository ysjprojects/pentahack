import numpy as np
import pandas as pd
import librosa

import sys
import os

from transformers import AutoProcessor, AutoModelForAudioClassification, Wav2Vec2FeatureExtractor

from pydub import AudioSegment
from pydub.utils import make_chunks


model1 = AutoModelForAudioClassification.from_pretrained("ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")

id2label = {
        0: "angry",
        1: "calm",
        2: "disgust",
        3: "fearful",
        4: "happy",
        5: "neutral",
        6: "sad",
        7: "surprised"
    }

label2id = {y:x for x, y in id2label.items()}

UPLOAD_DIR = os.path.abspath("upload")

def predict_emotion(wave_data):
    # sig, sr = librosa.load(audio_file)
    # wav_data = librosa.resample(sig, orig_sr=sr, target_sr=16000)

    # sound_array = np.array(wav_data.get_array_of_samples())

    input = feature_extractor(
        raw_speech=wav_data,
        sampling_rate=16000,
        padding=True,
        return_tensors="pt")

    result = model1.forward(input.input_values.float())
    # making sense of the result 
    id2label = {
        "0": "angry",
        "1": "calm",
        "2": "disgust",
        "3": "fearful",
        "4": "happy",
        "5": "neutral",
        "6": "sad",
        "7": "surprised"
    }
    interp = dict(zip(id2label.values(), list(round(float(i),4) for i in result[0][0])))

    pred = np.argmax(result[0][0].detach().numpy())
    return pred, interp

def analyse(filename):
    ext = filename.split(".")[1]
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        print("[ERROR] Audio script: File not found")
        return 
    elif ext == "mp4":
        audio = AudioSegment.from_file(file_path, format="mp4")
    elif ext == "wav":
        audio = AudioSegment.from_file(filename, format = "wav")
    