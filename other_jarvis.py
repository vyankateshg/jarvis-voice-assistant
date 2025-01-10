import wikipedia  # Install with `pip install wikipedia`
import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import random
import requests
from playsound import playsound
import random
from datetime import datetime
from plyer import notification
import pyautogui
import pywhatkit as pwk
import mygmail
import smtplib
import ssl

engine = pyttsx3.init()

# Get current time
now = datetime.now()

# Format: YYYY-MM-DD HH:MM:SS
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

def speak(text):
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

#speech recognition
def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("say something ! ...")
            audio = r.listen(source)

        try:
            content= r.recognize_google(audio,language='en-in')
            print("command = "+ content)
        except Exception as e:
            print("please try again.....")
        return content
def main_process():
    while True:
        request = command().lower()
        # print(request)
        if "hello" in request:
            speak("hello sir , how may i help you.")
        elif request.lower().startswith("play"):
            song = request.lower().split(" ")[1]
            link = musiclibrary.music.get(song, None)
            if link:
                speak(f"Playing {song}")
                webbrowser.open(link)
        elif "what is time" in request.lower():
            print("Current Time:", formatted)
            speak(f"date and time is{formatted} ")
        elif "new task" in request:
            task = request.replace("new task", "")
            task = task.strip()
            if task != "":
                speak("adding task : "+ task)
                with open ("todo.txt","a") as f:
                    f.write(task + "\n")   

        elif "speak task" in request:
            with open ("todo.txt","r") as f:
                    speak("Work we have to do today is :" + f.read())    
                    print("Work we have to do today is :" + f.read())    

        elif "show work" in request:
            with open ("todo.txt","r") as f:
                    task =  f.read()  
                    notification.notify(
                        title = "Today's work",
                        message = task
                    )
                    
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")
        elif "open" in request:
            query =  request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
                                  
        elif "wikipedia" in request:
            request = request.replace("jarvis ","")
            request = request.replace("search wikipedia ", "")
            result = wikipedia.summary(request,sentences=0.5)
            print(result)
            speak(result)
        elif "search google" in request:
            request = request.replace("jarvis ","")
            request = request.replace("search google ", "")
            webbrowser.open("https://www.google.com/search?q="+request)
            
        elif "send whatsapp" in request:
            pwk.sendwhatmsg("+918830620971","radhe radhe",11,00,30)
        # elif "send email" in request:
        #     pwk.send_mail("vyankateshg17@gmail.com",mygmail.app_password,"test","radhe radhe bhai ","guptavyankatesh617@gmail.com")
        #     speak("email sent ")
        elif "send email" in request:
            s= smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login("vyankateshg17@gmail.com",mygmail.app_password)
            message ='''
            this is the message
            from vyanki
            to vyankatesh
            for testting 
            i can format my gmail 
            as per
            my requirements 
            thanks
            radhe
            radhe

            '''
            s.sendmail("vyankateshg17@gmail.com","guptavyankatesh617@gmail.com",message)
            s.quit()

            # pwk.send_mail("vyankateshg17@gmail.com",mygmail.app_password,"test","radhe radhe bhai ","guptavyankatesh617@gmail.com")
            speak("email sent ")

main_process()
# speak("jai shree ram")