import os
import re
import sqlite3
import webbrowser

from moviepy.editor import VideoFileClip
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
con = sqlite3.connect("小页.db")
cursor = con.cursor()
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()
    print(f"open app: {app_name}")
    if app_name != "":

        try:
            speak("Opening "+query)
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()
            #open system command
            if len(results) > 0:
                print(f"open app from system_command {results[0][0]}")
                os.startfile(results[0][0])
            #open webbrowser
            else: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) > 0:
                    print(f"open app from web_command {results[0][0]}")
                    webbrowser.open(results[0][0])

                else:
                    try:
                        print("open app from start")
                        os.system('start '+query)
                    except:
                        speak("not found")
        except Exception as e:
            print(f"some thing went wrong {e}")
            speak("some thing went wrong")

def PlayYoutube(query="Never Gonna Give You Up"):
    search_term = extract_yt_term(query)
    speak(f"playing {search_term if search_term else query} on YouTube")
    kit.playonyt(search_term)

def PlayFirework(video_file="Never Gonna Give You Up"):
    clip = VideoFileClip(video_file)
    clip.preview()
    clip.close()
    
def extract_yt_term(command):
    #定义一个规则表达模式用来捕获歌曲名称
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    #在命令中找匹配项
    match=re.search(pattern,command,re.IGNORECASE)
    #如果找到就提取名称，否则为None
    return match.group(1) if match else None