import sounddevice as sd
import whisper

# Load the model
model = whisper.load_model("base")
print("Start speaking now...")

# Record audio from the microphone
duration = 15  # duration in seconds
sample_rate = 16000  # sample rate in Hz
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
sd.wait()  # wait for the recording to complete

# Ensure audio is 1D and of type float32
audio = audio.squeeze()  # Convert to 1D array if not already

# Use the model to transcribe the audio directly
result = model.transcribe(audio)

# Print the recognized text and detected language
print(f"Detected language: {result['language']}")
print(result['text'])
