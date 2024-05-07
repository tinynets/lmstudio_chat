import os
import sounddevice as sd
import whisper
from openai import OpenAI
from pynput import keyboard

class VoiceToChatApp:
    def __init__(self, model_path, prompts_directory, api_base_url, api_key):
        # Initialize Whisper model
        self.whisper_model = whisper.load_model(model_path)
        # Load the system prompt
        sys_prompt_path = os.path.join(prompts_directory, "sys_zombie.txt")
        with open(sys_prompt_path, "r") as file:
            self.system_prompt = file.read().strip()
        # Initialize chat client
        self.client = OpenAI(base_url=api_base_url, api_key=api_key)
        self.sample_rate = 16000  # sample rate in Hz
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.is_recording = False
        self.audio = None

    def on_press(self, key):
        if key == keyboard.Key.enter:
            if not self.is_recording:
                print("Start recording... Press 'Enter' to stop.")
                self.audio = sd.rec(int(3600 * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32')
                self.is_recording = True
            else:
                sd.stop()
                print("Recording stopped.")
                self.process_audio()
                self.is_recording = False

    def process_audio(self):
        audio = self.audio.squeeze()
        transcribed_text = self.whisper_model.transcribe(audio)
        print(f"Detected language: {transcribed_text['language']}")
        print(f"You said: {transcribed_text['text']}")
        response = self.send_message(transcribed_text['text'])
        print("AI: ", response)
        self.speak(response)  # Speak the response using macOS's say command

    def send_message(self, content):
        completion = self.client.chat.completions.create(
            model="LoneStriker/Meta-Llama-3-70B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content

    def speak(self, text):
        os.system(f'say "{text}"')

    def start_chat(self):
        self.listener.start()
        print("Chat started. Press 'Enter' to start/stop recording. Type 'quit' and press 'Enter' to exit.")
        self.listener.join()

if __name__ == "__main__":
    prompts_directory = "prompts"
    model_path = "base"
    api_base_url = "http://localhost:1234/v1"
    api_key = "lm-studio"
    app = VoiceToChatApp(model_path, prompts_directory, api_base_url, api_key)
    app.start_chat()
