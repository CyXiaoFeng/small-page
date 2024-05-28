import whisper
import speech_recognition as sr
import numpy as np
import io
import os
import torch
from queue import Queue
import soundfile as sf
from datetime import datetime
import time
#  检查是否有 GPU 可用
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("base", device=device)

# model = whisper.load_model("base")


#初始化数据
data_queue = Queue()
# 创建一个识别器实例
recognizer = sr.Recognizer()

# 过滤杂音
def is_silent(audio_data,threshold=1000):
    audio_array = np.frombuffer(audio_data.get_raw_data(),np.int16)
    amplitude = np.abs(audio_array).mean()
    print(f"音频振幅{amplitude}")
    return amplitude<threshold, audio_array

# 通过whisper做转换
def monter_whisper(source):
# 调整麦克风噪声水平
    while True:
        recognizer.adjust_for_ambient_noise(source)
        print("请说话...")
        # 捕获音频
        try:
            audio = recognizer.listen(source)
            silent, audio_array=is_silent(audio)
            print(f"静音了吗？{silent}")
            if(silent):
                print("声音太小，听不清！")
            else:
                start_time = datetime.now()
                print(f"开始转换：{start_time}")
                wav_data = wav_fp32_from_raw_data(audio_array)
                # result = model.transcribe(audio_fp32,language="zh",fp16=False,initial_prompt='听起来不错')
                result = model.transcribe(wav_data,language="zh",fp16=False,initial_prompt='听起来不错')
                end_time = datetime.now()
                print(f"转换结束: {end_time}")
                print(f"你说的是：{result['text']},耗时{end_time-start_time}")
        except sr.WaitTimeoutError:
            print("监听超时")
        except KeyboardInterrupt:
            print("程序结束")
            return audio
            break
# 转换raw_data数据为wav fp32数据
def wav_fp32_from_raw_data(audio_array):
    wav_data = audio_array.flatten().astype(np.float32) / 32768.0
    return wav_data
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
# 谷歌语音转换
def google_transcation(source,second_languages=[]):
    audio = None
    try:
        print("谷歌")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, 10, 6)
        print('recognizing')
        # query = recognizer.recognize_google(audio,language=primary_language)
        for language in second_languages:
            print(language)
            query = recognizer.recognize_google(audio, language=language)
            print(f"{'weather' in query.lower() or '天气' in query.lower()}")
            
        if query:
            print(f"You said: {query}")
            print(f"区域:{getLocationCodeByQuery(query)}")
        else:
            print("Sorry, I could not understand the audio")
            query = "on error"
        time.sleep(2)
        
    except sr.WaitTimeoutError:
        print("WaitTimeoutError")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio")
        query = "on error"
    finally:
        return audio

# 使用麦克风作为音频源
with sr.Microphone(sample_rate=16000) as source:
    # audio = monter_whisper(source)
    audio = google_transcation(source,["zh-CN"])




# 获取流式audio32
def wav_data_from_stream(audio):
    wav_data = audio.get_wav_data()
    wav_stream = io.BytesIO(wav_data)
    audio_array,_ = sf.read(wav_stream)
    audio_fp32 = audio_array.astype(np.float32)
    return audio_fp32


def whisper_to_E_text(tmpfile="./temp.wav"):
    result = model.transcribe(tmpfile, language="zh", fp16=False, temperature=0.4,initial_prompt='听起来不错')
    text = result['text'].strip()
    print(f"text: {text}")
    return text

# 获取音频文件文本
def audio_from_wav_file(audio):
    try:
        if(audio):
            audio_data = audio.get_raw_data()
            wav = sr.AudioData(audio_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            wav_data = io.BytesIO(wav.get_wav_data())
            with open("temp.wav", 'w+b') as f:
                f.write(wav_data.read())
            print("save as")
            whisper_to_E_text("temp.wav")
    except Exception as e:
        print(f"An error occurred: {e}")

# audio_from_wav_file(audio_data)