import speech_recognition as sr
import time
import whisper
import torch
import numpy as np
import threading
#  检查是否有 GPU 可用
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("base", device=device)

# 过滤杂音
def is_silent(audio_data,threshold=1500):
    audio_array = np.frombuffer(audio_data.get_raw_data(),np.int16)
    amplitude = np.abs(audio_array).mean()
    print(f"音频振幅{amplitude}")
    return amplitude<threshold, audio_array

# 转换raw_data数据为wav fp32数据
def wav_fp32_from_raw_data(audio_array):
    wav_data = audio_array.flatten().astype(np.float32) / 32768.0
    return wav_data

stop_listening = None
is_listening = True
def callback(re,audio):
    try:
        silent, audio_array=is_silent(audio)
        if(silent):
            print("声音太小，听不清！")
        else:
            wav_data = wav_fp32_from_raw_data(audio_array)
            print("正在识别......")
            result = model.transcribe(wav_data,language="zh",fp16=False,initial_prompt='听起来不错')
            print(f"识别结果:{result['text']}")
        print("请继续说话！")
    except Exception as e:
        print(e)

def listen_thread():
    global stop_listening
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as microphone:
        r.adjust_for_ambient_noise(microphone,duration=1)
        print("正在监听，请说话......")
    stop_listening =r.listen_in_background(microphone,callback,6)
    try:
        while is_listening:
            # print("任务运行中。。。。。。")
            time.sleep(1)
            pass
    except KeyboardInterrupt:
            stop_listening(wait_for_stop=False)
    print("监听已停止")

def stop_listen():
    global stop_listening, is_listening
    if(stop_listening):
        stop_listening(wait_for_stop=False)
        print("已停止监听....")
    is_listening = False

def start_listen():
    listening_thread = threading.Thread(target=listen_thread)
    listening_thread.start()

start_listen()
# 等待一段时间以确保监听开始
time.sleep(30)
stop_listen()


