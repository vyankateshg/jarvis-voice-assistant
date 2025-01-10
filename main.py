# import speech_recognition as sr
# import webbrowser
# import pyttsx3
# import musiclibrary
# import requests
# from playsound import playsound
# import random

# #pip install PocketSphinx module

# recognizer = sr.Recognizer()
# engine = pyttsx3.init()
# newsapi = "ec83e6a81aa64b92ac304de6adbf84b1"


# def speak(text):
#      engine.say(text)
#      engine.runAndWait()
#      rate = engine.getProperty('rate')
#      engine.setProperty('rate',180)


# def processcomand(c):
#     print(c)
#     if "open google" in c.lower():
#         print("Opening Google")
#         speak("Opening Google")

#         webbrowser.open("https://google.com")
#     elif "open facebook" in c.lower():
#         speak("Opening face book")
#         print("Opening face book")
#         webbrowser.open("https://facebook.com")
#     elif "youtube" in c.lower():
#         print("Opening Youtube")
#         speak("Opening Youtube")


#         webbrowser.open("https://youtube.com")
#     elif "linkedin" in c.lower():
#         print("Opening linkedin")
#         speak("Opening linkedin")
#         webbrowser.open("https://www.linkedin.com/")
#     elif c.lower().startswith("play"):
#         song = c.lower().split(" ")[1]
#         link = musiclibrary.music[song]
#         webbrowser.open(link)

#     elif "how create you"  in c.lower():
#         print("I am an ai assistan , vyankatesh gupta made me as per his dream") 
#         speak("I am an ai assistan , vyanki gupta made me as per his dream") 
#     elif "so jao"  in  c.lower():
#         print("ok sir getting to sleep ")
#         speak("ok sir getting to sleep ")
#         # Replace with the path to your music file
#         playsound("C:\python project\jarvis meri jaan/khrate.mp3")
#         exit();    
    
#     elif "news" in c.lower():
#         r = requests.get("https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=ec83e6a81aa64b92ac304de6adbf84b1")

#         # Check if the request was successful
#         if r.status_code == 200:
#             data = r.json()
#             # Extract and print the headlines
#             articles = data.get("articles", [])
#             for i, article in enumerate(articles, start=1):
#                 print(f"{i}. {article['title']}")
#                 speak(f"{i}. {article['title']}")
#                 if i== random.randint(1,5)or  random.randint(5,10):
#                     break
#     else:
#         #let open ai handle the request   
#         pass      


        
# if __name__ == "__main__":
#     speak("Initializing Jarvis.....")

#     while True:
#         #listen for the wake "jarvis"
#         #obtain audio from microphone 
#         r = sr.Recognizer()
    
#          # recognize speech using google
#         print("recognizing...") 
#         try: 
#             with sr.Microphone() as source:
#                 print("listening...")
#                 audio = r.listen(source,timeout=4,phrase_time_limit=1)
#             word = r.recognize_google(audio)
#             if (word.lower()== "jarvis"):
#                 speak("ya")
#                 #listen for command  
#                 with sr.Microphone() as source:
#                     print("jarvis Activated ....")
#                     audio = r.listen(source)
#                     command = r.recognize_google(audio)
#                     processcomand(command)

        
#         except Exception as e:
#             print("error; {0}".format(e))

import wikipedia  # Install with `pip install wikipedia`
import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from playsound import playsound
import random
from datetime import datetime

# Get current time
now = datetime.now()

# Format: YYYY-MM-DD HH:MM:SS
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "ec83e6a81aa64b92ac304de6adbf84b1"

def speak(text):
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()

def fetch_answer_locally(question):
    """
    Uses Wikipedia to fetch answers for general questions.
    """
    try:
        # Fetch a summary with a maximum of 1 sentence
        summary = wikipedia.summary(question, sentences=1)
        
        # Truncate the summary to a max of ~150 characters for brevity
        if len(summary) > 150:
            summary = summary[:147] + "..."  # Add ellipsis if too long
        return summary
    except wikipedia.DisambiguationError as e:
                # Handle ambiguous queries by suggesting options
                return f"Your question could refer to multiple topics, such as {', '.join(e.options[:3])}. Please clarify."
    except wikipedia.PageError:
                # Handle cases where no Wikipedia page matches the query
            return "I couldn't find any relevant information on that topic."
    except Exception as e:
            return "I encountered an error while fetching the answer. Please try again."

    
def process_command(c):
    global is_busy
    is_busy = True
    print(f"Command: {c}")
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song, None)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find the song in the library.")
    elif "who create you" in c.lower():
        speak("I am an AI assistant. Vyanki Gupta created me as per his dream.")
    elif "so jao" in c.lower():
        speak("Okay sir, going to sleep.")
        playsound("C:\\python project\\jarvis meri jaan\\khrate.mp3")
        exit()
    elif "what is time" in c.lower():
        print("Current Time:", formatted)
        speak(f"date and time is{formatted} ")
        
    elif "close yourself" in c.lower():
        print("Ok sir, turning off.")
        speak("Ok sir, turning off.")
        exit()
    elif "news" in c.lower():
        fetch_news()
    else:
        # Assume it's a general question and attempt to answer
        speak("according to wikipedia....")
        answer = fetch_answer_locally(c)
        print(answer)
        speak(answer)
    is_busy = False

def fetch_news():
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=" + newsapi)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            for i, article in enumerate(articles[:5], start=1):  # Limit to 5 articles
                title = article.get("title", "No title available")
                print(f"{i}. {title}")
                speak(title)
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("I couldn't fetch the news. Please check your internet connection.")

def listen_for_command(prompt=None):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        if prompt:
            speak(prompt)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            speak("No input detected. Please try again.")
        except sr.UnknownValueError:
            speak("I couldn't understand that. Please try again.")
        except sr.RequestError as e:
            speak("There was an issue with the speech recognition service.")
        return None

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    first_time = True  # Flag to track if it's the first run
    is_busy = False    # Tracks if Jarvis is currently busy
    while True:
        if first_time:
            word = listen_for_command("Say 'Jarvis' to activate...")
            first_time = False
        else:
            word = listen_for_command()
        if word and word.lower() == "jarvis":
            if not is_busy:  # Only ask "What can I do for you?" if idle
                command = listen_for_command("Yes, I am listening.")
                if command:
                    process_command(command)
            else:
                command = listen_for_command()
                if command:
                    process_command(command)
