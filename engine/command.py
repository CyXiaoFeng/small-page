import pyttsx3
import speech_recognition as sr # type: ignore
import eel
import time

def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    eel.DisplayMessage(text)  #文本输入
    engine.say(text)
    engine.runAndWait()


def takecommand():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            eel.DisplayMessage('listening...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, 10, 6)
        print('recognizing')
        eel.DisplayMessage('recognizing...')
        # Recognize (convert from speech to text)
        query = r.recognize_google(audio, language='en-in')
        if query:
            print(f"You said: {query}")
        else:
            print("Sorry, I could not understand the audio")
            query = "on error"
            eel.DisplayMessage(query)
        time.sleep(2)

    except sr.WaitTimeoutError:
        print("WaitTimeoutError")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio")
        query = "on error"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    
    
    # 语音识别如果包含的有on you
    # return "on youtube"
    # return "open word"
    # return "open web"
    # return "open 有道词典"
    # return "weather in beijing"
    # return "play video"
    return query.lower()

@eel.expose
def allCommands():

    query = takecommand()

    if "open" in query:
        print("open a local app")
        from engine.features import openCommand
        openCommand(query)
    elif "on youtube" in query:
         print("on youtube website")
         from engine.features import PlayYoutube
         PlayYoutube(query)
    elif "video" in query:
        print("play a firework video")
        video_dir = "www\\assets\\video\\firework.mp4"
        # from engine.features import PlayFirework
        # PlayFirework(video_dir)
        eel.PlayVideo(video_dir)
    elif "weather" in query:
        from engine.features import GetWeather
        GetWeather(query)
    #未能识别的命令
    else:
        print("not correct command")
        speak('not correct command')

    eel.ShowHood()