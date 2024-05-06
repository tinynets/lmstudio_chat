import sounddevice as sd
import whisper
from openai import OpenAI
import os

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

    def transcribe_audio(self):
        print("Start speaking now...")
        duration = 8  # duration in seconds
        sample_rate = 16000  # sample rate in Hz
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()  # wait for the recording to complete
        audio = audio.squeeze()  # Convert to 1D array if not already
        result = self.whisper_model.transcribe(audio)
        print(f"Detected language: {result['language']}")
        return result['text']

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

    def start_chat(self):
        print("Chat started. Type 'quit' to exit.")
        while True:
            transcribed_text = self.transcribe_audio()
            if transcribed_text.lower() == 'quit':
                break
            print(f"You said: {transcribed_text}")
            response = self.send_message(transcribed_text)
            print("AI: ", response)

if __name__ == "__main__":
    prompts_directory = "prompts"
    model_path = "base"
    api_base_url = "http://localhost:1234/v1"
    api_key = "lm-studio"
    app = VoiceToChatApp(model_path, prompts_directory, api_base_url, api_key)
    app.start_chat()
