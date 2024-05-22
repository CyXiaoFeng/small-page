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

def GetWeather(city='beijing'):
    cityCode = getLocation(city.lower())
    webbrowser.open(f"https://weather.cma.cn/web/weather/{cityCode}.html")

def getLocation(cityCode):
    pattern = r"weather in (\w+)"
    match = re.search(pattern, cityCode)
    city_name = 'beijing'
    if match:
        city_name = match.group(1)
        print("City name:", city_name)
    else:
        print("No match found")
    cityCodeByCity = {'chengdu': 'S1003',
    'beijing': '54511',
    'nanjing': '58238',
    'nanning': '59431',
    'nanchang': '58606',
    'hefei': '58321',
    'haerbin': '50953',
    'guangzhou': '59287',
    'xujiahui': '58367',
    'lasa': '55591',
    'kunming': '56778',
    'hangzhou': '58457',
    'wuhan': '57494',
    'shenyang': '54342',
    'shapingba': '57516',
    'jinan': '54823',
    'haikou': '59758',
    'shenzhen': '59493',
    'shijiazhuang': '53698-sjz',
    'fuzhou': '58847',
    'luogang': '59287-lg',
    'xining': '52866',
    'xian': 'V8870',
    'guiyang': '57816',
    'zhengzhou': '57083',
    'yinchuan': '53614',
    'changchun': '54161',
    'changshahuanghua': '57679',
    'luquan': '53698',
    'wulumuqi': '51463',
    'lanzhou': '52889',
    'heiniucheng': '54517',
    'xianggangtianwentai': '45005',
    'datanshan': '45011',
    'taibei': '58968'}
    code = cityCodeByCity.get(city_name)
    return code if code is not None else '54511'

def extract_yt_term(command):
    #定义一个规则表达模式用来捕获歌曲名称
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    #在命令中找匹配项
    match=re.search(pattern,command,re.IGNORECASE)
    #如果找到就提取名称，否则为None
    return match.group(1) if match else None