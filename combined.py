import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import queue
import threading

def int_or_timeout():
    ''' Wait for a specific key press on the console to stop recording. '''
    input("Recording... Press Enter to stop.\n")

# Set the sample rate and other parameters
sample_rate = 16000  # Hz
model_path = "vosk-model-en-us-0.42-gigaspeech"

# Load Vosk model
model = Model(model_path)
rec = KaldiRecognizer(model, sample_rate)

# Buffer for storing audio
audio_buffer = queue.Queue()

# Callback to capture audio data
def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    # Convert numpy array to bytes and ensure it is pushed as int16
    audio_buffer.put(indata.astype(np.int16).tobytes())

# Thread to process audio data
def process_audio():
    while True:
        data = audio_buffer.get()
        if data is None:  # Check for stop signal
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("Result:", result['text'])
        else:
            partial = json.loads(rec.PartialResult())['partial']
            print("Partial result:", partial)

try:
    # Start recording and processing in parallel
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback):
        # Start audio processing thread
        processing_thread = threading.Thread(target=process_audio)
        processing_thread.start()

        # Wait for user to stop recording
        int_or_timeout()
except KeyboardInterrupt:
    print("Recording stopped by user.")
finally:
    # Stop processing
    audio_buffer.put(None)  # Send signal to stop the processing thread
    processing_thread.join()

# Get the final result
final_result = json.loads(rec.FinalResult())
print("Final result:", final_result.get('text', 'No text recognized'))
