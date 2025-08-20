import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import datetime
import wikipedia
import pyjokes
import os
import pywhatkit   

recognizer = sr.Recognizer()
engine = pyttsx3.init()


voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    print("Alexa:", text)
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    c = c.lower()

    sites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "gmail": "https://mail.google.com"
    }

    for site in sites:
        if f"open {site}" in c:
            speak(f"Opening {site}")
            webbrowser.open(sites[site])
            return

    if c.startswith("play"):
        song = c.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Please tell me the song name.")

    
    elif "send message" in c:
        speak("Whom should I send?")
        contact = input("Enter number with country code: ")  
        speak("What is the message?")
        msg = input("Type your message: ")
        pywhatkit.sendwhatmsg_instantly(contact, msg)
        speak("Message sent successfully!")

   
    elif "open website" in c:
        site = c.replace("open website", "").replace("of", "").strip()
        speak(f"Opening {site}")
        webbrowser.open(f"https://www.{site}.com")


    elif "time" in c:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in c:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    elif "wikipedia" in c:
        speak("Searching Wikipedia...")
        query = c.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except:
            speak("No results found on Wikipedia")
            

    elif "joke" in c:
        joke = pyjokes.get_joke()
        speak(joke)
    
    # elif "open google" in c:
    #     speak("Opening Google")
    #     webbrowser.open("https://www.google.com")

    elif "open notepad" in c:
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif "open calculator" in c:
        speak("Opening Calculator")
        os.system("calc.exe")
    
    
    elif "shutdown" in c:
        speak("I am shutting down the system in 10 seconds. Please close all applications.")
        os.system("shutdown /s /t 10")

    elif "restart" in c:
            speak("Restarting your system")
            os.system("shutdown /r /t 5")

    elif "exit" in c or "quit" in c:
        speak("Goodbye! Have a nice day.")
        exit()
    
    elif "remember" in c:
        if "my birthday is" in c:
            birthday = c.replace("remember my birthday is", "").strip()
            remember("birthday", birthday)
            speak(f"Okay, I will remember your birthday as {birthday}")

    elif "when is my birthday" in c:
        birthday = recall("birthday")
        speak(f"Your birthday is on {birthday}")


    else:
        speak("Sorry, I didn't understand that command")

if __name__ == "__main__":
    speak("I am Alexa, your personal assistant")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # quick adjustment
                print("Say 'Alexa' to wake me up...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            if "alexa" in word.lower():
                speak("Yes, how can I help?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    command = recognizer.recognize_google(audio)

                    processcommand(command)

        except sr.WaitTimeoutError:
            continue  
        except Exception as e:
            print("Error:", e)

