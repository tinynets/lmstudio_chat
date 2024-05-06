import pyaudio
import numpy as np

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

print("Recording for 5 seconds, speak now...")
frames = []
for i in range(0, int(16000 / 1024 * 5)):
    data = stream.read(1024)
    frames.append(np.frombuffer(data, dtype=np.int16))
stream.stop_stream()
stream.close()
p.terminate()

# Checking if there's substantial input
volume_norm = np.linalg.norm(np.concatenate(frames))
print(f"Input volume: {volume_norm}")

if volume_norm < 1000:  # Adjust threshold as necessary
    print("Microphone input is very low. Check microphone settings.")
else:
    print("Microphone input is okay.")
