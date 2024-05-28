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

# 播放yutobe
def PlayYoutube(query="Never Gonna Give You Up"):
    search_term = extract_yt_term(query)
    speak(f"playing {search_term if search_term else query} on YouTube")
    kit.playonyt(search_term)

# 播放烟花
def PlayFirework(video_file="www\\assets\\video\\firework.mp4"):
    clip = VideoFileClip(video_file)
    clip.preview()
    clip.close()

# 获取城市对应的天气
def GetWeather(query):
    cityCode = getLocationCodeByQuery(query)
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

    cityCodeByCN = {'成都': 'S1003',
    '北京': '54511',
    '南京': '58238',
    '南宁': '59431',
    '南昌': '58606',
    '合肥': '58321',
    '哈尔滨': '50953',
    '广州': '59287',
    '徐家汇': '58367',
    '拉萨': '55591',
    '昆明': '56778',
    '杭州': '58457',
    '武汉': '57494',
    '沈阳': '54342',
    '沙坪坝': '57516',
    '济南': '54823',
    '海口': '59758',
    '深圳': '59493',
    '石家庄': '53698-sjz',
    '福州': '58847',
    '萝岗': '59287-lg',
    '西宁': '52866',
    '西安': 'V8870',
    '贵阳': '57816',
    '郑州': '57083',
    '银川': '53614',
    '长春': '54161',
    '长沙黄花': '57679',
    '鹿泉': '53698',
    '乌鲁木齐': '51463',
    '兰州': '52889',
    '黑牛城': '54517',
    '香港天文台': '45005',
    '大潭山': '45011',
    '台北': '58968'}

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

def getLocationCodeByQuery(query):
    cityCode = {'成都': 'S1003',
    '北京': '54511',
    '南京': '58238',
    '南宁': '59431',
    '南昌': '58606',
    '合肥': '58321',
    '哈尔滨': '50953',
    '广州': '59287',
    '徐家汇': '58367',
    '拉萨': '55591',
    '昆明': '56778',
    '杭州': '58457',
    '武汉': '57494',
    '沈阳': '54342',
    '沙坪坝': '57516',
    '济南': '54823',
    '海口': '59758',
    '深圳': '59493',
    '石家庄': '53698-sjz',
    '福州': '58847',
    '萝岗': '59287-lg',
    '西宁': '52866',
    '西安': 'V8870',
    '贵阳': '57816',
    '郑州': '57083',
    '银川': '53614',
    '长春': '54161',
    '长沙黄花': '57679',
    '鹿泉': '53698',
    '乌鲁木齐': '51463',
    '兰州': '52889',
    '黑牛城': '54517',
    '香港天文台': '45005',
    '大潭山': '45011',
    '台北': '58968',
    'chengdu': 'S1003',
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
    for key,value in cityCode.items():
        if key in query:
            return value

    return '54511'

def extract_yt_term(command):
    #定义一个规则表达模式用来捕获歌曲名称
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    #在命令中找匹配项
    match=re.search(pattern,command,re.IGNORECASE)
    #如果找到就提取名称，否则为None
    return match.group(1) if match else None