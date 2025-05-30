

import pyttsx3
import speech_recognition as sr

class VoiceAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)

    def get_user_input(self):
        with sr.Microphone() as source:
            print("🎤 Listening... Please speak.")
            audio = self.recognizer.listen(source)

        try:
            print("🔍 Transcribing...")
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Sorry, could not understand audio.")
            return ""
        except sr.RequestError:
            print("❌ Could not request results from Google Speech Recognition.")
            return ""

    def speak_text(self, text):
        print(f"💬 Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()


if __name__ == "__main__":
    agent = VoiceAgent()
    query = agent.get_user_input()
    if query:
        agent.speak_text("You said: " + query)
