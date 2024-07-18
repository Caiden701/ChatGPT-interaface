import os
from openai import OpenAI
from gtts import gTTS
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import time

# Initialize OpenAI client
openai = OpenAI(
    api_key='' # Your OpenAi API key
)
client = ElevenLabs(
  api_key="", # Your Eleven labs API key
)

def get_chatgpt_response(prompt):
    print("Sending prompt to ChatGPT API...")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo"
    )
    print("Received response from ChatGPT API.")
    return chat_completion.choices[0].message.strip()

def speak_text(response):
    print("Playing speech...")
    audio = client.generate(
    text=response,
    voice="Jessie",
    model="eleven_multilingual_v1"
)
    play(audio)


if __name__ == "__main__":
    while True:
        user_input = input("Enter your message: ")
        
        if user_input:
            # Using OpenAI API call
            response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Call me sir. {user_input}"}])
            response_text = response.choices[0].message.content
            print(f"ChatGPT: {response_text}")
            speak_text(response_text)
