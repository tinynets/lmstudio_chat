import os
import sys
import json
import pyaudio
from vosk import Model, KaldiRecognizer

model_path = "vosk-model-en-us-0.42-gigaspeech"
if not os.path.exists(model_path):
    print("Model directory not found.")
    exit(1)

model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

print("Start speaking...\n")
try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("Final result:", result.get('text', 'No text recognized'))
        else:
            print("Partial result:", json.loads(rec.PartialResult())['partial'])
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stream closed")
