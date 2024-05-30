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
    print(f"音频振幅{amplitude}")
    return amplitude<threshold, audio_array

# 转换raw_data数据为wav fp32数据
def wav_fp32_from_raw_data(audio_array):
    wav_data = audio_array.flatten().astype(np.float32) / 32768.0
    return wav_data

# 全局变量
stop_event = threading.Event()
thread = None

def callback(recognizer, audio):
        try:
            silent, audio_array = is_silent(audio)
            print(f"静音了吗？{silent}")
            if silent:
                print("声音太小，听不清！")
                eel.displayWord("声音太小，听不清！")
                time.sleep(1)
            else:
                wav_data = wav_fp32_from_raw_data(audio_array)
                result = model.transcribe(wav_data, language="zh", fp16=False, initial_prompt='听起来不错')
                print(f"你说的是：{result['text']}")
                eel.displayWord(result['text'])
        except sr.WaitTimeoutError:
            print("监听超时")
        except KeyboardInterrupt:
            print("程序结束")

# 通过whisper做转换
def monter_whisper():
    with sr.Microphone(sample_rate=16000) as source:
        recognizer = sr.Recognizer()
    # 调整麦克风噪声水平
        while not stop_event.is_set():
            recognizer.adjust_for_ambient_noise(source)
            recognizer.pause_threshold = 1
            print("请说话...")
            # 捕获音频
            try:
                audio = recognizer.listen(source,10,6)
                silent, audio_array=is_silent(audio)
                print(f"静音了吗？{silent}")
                if(silent):
                    print("声音太小，听不清！")
                    eel.displayWord("声音太小，听不清！")
                    time.sleep(1)
                else:
                    wav_data = wav_fp32_from_raw_data(audio_array)
                    result = model.transcribe(wav_data,language="zh",fp16=False,initial_prompt='听起来不错')
                    print(f"你说的是：{result['text']}")
                    eel.displayWord(result['text'])
            except sr.WaitTimeoutError:
                print("监听超时")
            except KeyboardInterrupt:
                print("程序结束")
                break
            finally:
                # 添加检查点，以便在循环执行期间检查stop_event
                print("检查状态")
                if stop_event.is_set():
                    break

def monter_whisper_async():
    recognizer = sr.Recognizer()

    # 创建麦克风源
    microphone = sr.Microphone(sample_rate=16000)

    # 定义回调函数
    def callback(recognizer, audio):
        try:
            print("请说话...")
            silent, audio_array = is_silent(audio)
            print(f"静音了吗？{silent}")
            if silent:
                print("声音太小，听不清！")
                eel.displayWord("声音太小，听不清！")
                time.sleep(1)
            else:
                wav_data = wav_fp32_from_raw_data(audio_array)
                result = model.transcribe(wav_data, language="zh", fp16=False, initial_prompt='听起来不错')
                print(f"你说的是：{result['text']}")
                eel.displayWord(result['text'])
        except sr.WaitTimeoutError:
            print("监听超时")
        except KeyboardInterrupt:
            print("程序结束")

    # 开始在后台监听音频
    stop_listening = recognizer.listen_in_background(microphone, callback)

    # 主线程继续执行其他操作
    print("主线程继续执行")

    # 如果需要停止监听，调用返回的函数
    # stop_listening(wait_for_stop=False)

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
    # return query.lower()
    return "语音"
    # return "文字"
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
        eel.PlayVideo(video_dir)
    elif "weather" in query  or '天气' in query:
        from engine.features import GetWeather
        GetWeather(query)
    elif "to word" in query  or '文字' in query:
        eel.ImageToWord()
    elif "to voice" in query  or '语音' in query:
        eel.monitorSpeech()
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
def listenAudio2Word():
    monter_whisper_async()
    # global thread
    # print(f"启动线程。{thread==None}")
    # if(thread != None):
    #     return
    # # 确保停止事件被清除
    # stop_event.clear()
    # # 启动新的线程并传递参数
    # thread = threading.Thread(target=monter_whisper_async)
    # thread.start()


@eel.expose
def stoplistenAudio2Word():
    print("停止线程")
    global thread
    # 设置停止事件
    stop_event.set()
    # 等待线程结束
    if thread:
        thread.join()
    print("线程已停止。")
    return "success"

@eel.expose
def initIndex():
    print("initIndex")

@eel.expose
def initSpeech():
    print("initSpeech")