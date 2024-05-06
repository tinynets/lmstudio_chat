from openai import OpenAI
import os

# Read the system prompt from the prompts directory
prompts_directory = "prompts"
sys_zombie_path = os.path.join(prompts_directory, "sys_zombie.txt")

with open(sys_zombie_path, "r") as file:
    system_prompt = file.read().strip()


# system_prompt = "You are to pretend to be a chef teaching me how to do stuff. We will only talk about food."

class ChatApp:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    def send_message(self, content):
        completion = self.client.chat.completions.create(
            model="LoneStriker/Meta-Llama-3-70B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content

    def start_chat(self):
        print("Chat started. Type 'quit' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            response = self.send_message(user_input)
            print("AI: ", response)

if __name__ == "__main__":
    app = ChatApp()
    app.start_chat()