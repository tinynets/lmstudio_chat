import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Set the sample rate and duration of the recording
sample_rate = 16000  # You can adjust this value if needed
duration = 5  # Recording duration in seconds

# Record audio from the microphone
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()

# Convert the recording to 16-bit PCM
recording_pcm = np.int16(recording * 32767)

# Save the recording to a WAV file
wav.write('test.wav', sample_rate, recording_pcm)