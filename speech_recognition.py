# -*- coding: utf-8 -*-
# speech_recognition.py
import vosk
import sounddevice as sd
import json
import threading

def recognize_speech_from_mic():
    model = vosk.Model("vosk-model-small-cn-0.22")
    recognizer = vosk.KaldiRecognizer(model, 16000)
    result_text = []
    event = threading.Event()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if recognizer.AcceptWaveform(bytes(indata)):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text:
                result_text.append(text)
                event.set()

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("请开始说话...")
        event.wait()

    return ' '.join(result_text)
