import os
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
from elevenlabs import play
from elevenlabs.client import ElevenLabs

# Initialize OpenAI client
openai = OpenAI(
    api_key='Your API key'  # Replace with your actual OpenAI API key
)

client = ElevenLabs(
    api_key="Your API key"  # Replace with your actual ElevenLabs API key
)

def get_chatgpt_response(prompt):
    print("Sending prompt to ChatGPT API...")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print("Received response from ChatGPT API.")
    return response.choices[0].message.content.strip()

def speak_text(response):
    print("Playing speech...")
    audio = client.generate(
        text=response,
        voice="Jessie",
        model="eleven_multilingual_v1"
    )
    play(audio)

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
    response = {"success": True, "error": None, "transcription": None}
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Unable to recognize speech"
    
    return response

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print("Please say something...")
        speech_response = recognize_speech_from_mic(recognizer, microphone)
        
        if speech_response["success"]:
            user_input = speech_response["transcription"]
            print(f"You said: {user_input}")
            
            if user_input:
                response_text = get_chatgpt_response(f"Call me sir. {user_input}")
                print(f"ChatGPT: {response_text}")
                speak_text(response_text)
        else:
            print("I didn't catch that. Could you please repeat?")
            if speech_response["error"]:
                print(f"ERROR: {speech_response['error']}")
