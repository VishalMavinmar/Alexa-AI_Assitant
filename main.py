import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary 
import requests
#    7440f30f198c4bb6b1a7bc9e2c6539a6
recognizer = sr.Recognizer()
engine = pyttsx3.init()



voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():  
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    if c.lower() =="open google":
        speak("opening google")
        webbrowser.open("https://www.google.com")
    
    elif c.lower() == "open youtube":
        speak("opening youtube")
        webbrowser.open("https://www.youtube.com")

    elif c.lower()=="open facebook":
        speak("opening facebook")
        webbrowser.open("https://www.facebook.com")

    elif c.lower().startswith("play"):
        song =c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "newz" in c.lower():
        speak("Fetching the latest news headlines")
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=7440f30f198c4bb6b1a7bc9e2c6539a6")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                 for article in articles[:5]:  # Limit to 5 headlines
                    speak(article.get('title', 'No title available'))
        else:
            speak("I could not find any news right now.")
    elif c.lower() == "exit":
        speak("Exiting the program")
        exit()


if __name__ == "__main__":
    speak("Initializing Alexa")

    while True:
        
        r = sr.Recognizer()
        print("Recognizing")
        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source, timeout=3, phrase_time_limit=4)

            word = r.recognize_google(audio)
            if word.lower() == "alexa":
                speak("Yes, how can I help?")
                with sr.Microphone() as source:
                    print("alexa active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processcommand(command)

        except Exception as e:
            print("error; {0}".format(e))

      


