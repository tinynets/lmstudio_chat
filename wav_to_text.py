import os
import wave
import json
from vosk import Model, KaldiRecognizer

# Load the model
model = Model("vosk-model-en-us-0.42-gigaspeech")

# Open the wav file
wf = wave.open("test.wav", "rb")

# Check if the sample rate of the wav file is supported
if wf.getframerate() != 16000:
    print("Please make sure the sample rate of the wav file is 16000.")
    exit(1)

# Create a recognizer
rec = KaldiRecognizer(model, wf.getframerate())

# Process the audio file
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

# Get the final result
print(rec.FinalResult())