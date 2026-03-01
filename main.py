import speech_recognition as sr
import webbrowser
import win32com.client   # <-- replaced pyttsx3
import musicLibrary
import requests
from groq import Groq
groq_client = Groq(api_key="your_api_key")  # <-- Groq API key

# pip install pocketsphinx

recognizer = sr.Recognizer()
speaker = win32com.client.Dispatch("SAPI.SpVoice")  # <-- new offline TTS engine
newsapi = "206125b762c443d5bcd30d7f30afb2ce"

def speak(text):
    speaker.Speak(text)   # <-- simple offline voice
def ask_ai(question):
    chat = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": question}]
    )
    return chat.choices[0].message.content 

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()
        link = musicLibrary.music.get(song)
        webbrowser.open(link)

    elif "news" in c.lower() or "headline" in c.lower() or "latest" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=india+news&sortBy=publishedAt&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        reply = ask_ai(c)
        speak(reply)



if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        r = sr.Recognizer()
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
                word = r.recognize_google(audio)

            if (word.lower() == "jarvis"):
                speak("Yes?")     
                with sr.Microphone() as source:
                    print("Jarvis active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)

        except Exception as e:
            print("Error:", e)   
