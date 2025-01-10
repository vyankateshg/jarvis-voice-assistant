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
        playsound("C:\\python project\\jarvis eri jaan\\khrate.mp3")
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
