import pyttsx3
import speech_recognition as sr # type: ignore
import eel
import time
import whisper
import numpy as np
from PIL import Image
import pytesseract
from io import BytesIO
import base64
import threading
import torch
#  检查是否有 GPU 可用
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("base", device=device)
pytesseract.pytesseract.tesseract_cmd = r'd:\Program Files\Tesseract-OCR\tesseract.exe'
def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    eel.DisplayMessage(text)  #文本输入
    engine.say(text)
    engine.runAndWait()


# 过滤杂音
def is_silent(audio_data,threshold=1000):
    audio_array = np.frombuffer(audio_data.get_raw_data(),np.int16)
    amplitude = np.abs(audio_array).mean()
    # print(f"音频振幅{amplitude}")
    return amplitude<threshold, audio_array

# 转换raw_data数据为wav fp32数据
def wav_fp32_from_raw_data(audio_array):
    wav_data = audio_array.flatten().astype(np.float32) / 32768.0
    return wav_data

stop_listening = None
is_listening = True
tips = "请说话......"
# 定义回调函数
def callback(recognizer, audio):
    global tips,is_listening
    try:
        print(tips)
        eel.updateStatus(f"{tips if is_listening else '状态'}")
        silent, audio_array = is_silent(audio)
        if silent:
            print("声音太小，听不清！")
            eel.displayWord("声音太小，听不清！")
        else:
            print("识别中...")
            eel.updateStatus(f"{'识别中...' if is_listening else '状态'}")
            wav_data = wav_fp32_from_raw_data(audio_array)
            result = model.transcribe(wav_data, language="zh", fp16=False, initial_prompt='听起来不错')
            print(f"你说的是：{result['text']}")
            eel.displayWord(result['text'])
            eel.updateStatus(f"{'识别成功' if is_listening else '状态'}")
        tips = "请继续说话！"
        print(tips)
        eel.updateStatus(f"{tips if is_listening else '状态'}")
    except Exception as e:
        print(e)

def listen_thread():
    global stop_listening
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as microphone:
        r.adjust_for_ambient_noise(microphone,duration=1)
        print("正在监听，请说话......")
    stop_listening =r.listen_in_background(microphone,callback)
    try:
        while is_listening:
            # print("任务运行中。。。。。。")
            time.sleep(1)
            pass
    except KeyboardInterrupt:
            stop_listening(wait_for_stop=False)
    print("监听已停止")

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
        query = r.recognize_google(audio, language='zh-CN')
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
    # return "语音"
    # return "文字"
    return query.lower()
   
@eel.expose
def allCommands():

    query = takecommand()

    if "open" in query or "打开" in query:
        print("open a local app")
        from engine.features import openCommand
        openCommand(query)
    elif "on youtube" in query or '在youtube' in query:
         print("on youtube website")
         from engine.features import PlayYoutube
         PlayYoutube(query)
    elif "video" in query or '视频' in query:
        print("play a firework video")
        video_dir = "www\\assets\\video\\firework.mp4"
        # from engine.features import PlayFirework
        # PlayFirework(video_dir)
        eel.stepToURL("playvideo.html")
    elif "weather" in query  or '天气' in query:
        from engine.features import GetWeather
        GetWeather(query)
    elif "to word" in query  or '文字' in query:
        print("文字识别")
        eel.stepToURL("image2txt.html")
    elif "to voice" in query  or '语音' in query:
        print("语音识别")
        eel.stepToURL("monivoice.html")
        # eel.show("monivoice.html")
    #未能识别的命令
    else:
        print("not correct command")
        speak('not correct command')

    eel.ShowHood()

@eel.expose
def playVideo():
    video_dir = "www\\assets\\video\\firework.mp4"
    print(video_dir)
    return video_dir

@eel.expose
def image2Word():
    print("Image2Word")

@eel.expose
def recognize_text(data_url):
    # 解码 base64 数据
    _, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    # # 使用 PIL 打开图片
    image = Image.open(BytesIO(data))
    # # 使用 pytesseract 识别文字
    text = pytesseract.image_to_string(image, lang='eng+chi_sim')
    print(f"识别结果:{text}")
    return text

@eel.expose
def startlistenAudio2Word():
    global is_listening
    is_listening = True
    listening_thread = threading.Thread(target=listen_thread)
    listening_thread.start()

@eel.expose
def stoplistenAudio2Word():
    global stop_listening, is_listening
    is_listening = False
    if(stop_listening):
        stop_listening(wait_for_stop=False)
        print("已停止监听....")
    return "success"

@eel.expose
def initIndex():
    print("initIndex")

@eel.expose
def initSpeech():
    print("initSpeech")