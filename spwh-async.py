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
import threading
#  检查是否有 GPU 可用
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("base", device=device)
# 过滤杂音
def is_silent(audio_data,threshold=1000):
    audio_array = np.frombuffer(audio_data.get_raw_data(),np.int16)
    amplitude = np.abs(audio_array).mean()
    print(f"音频振幅{amplitude}")
    return amplitude<threshold, audio_array

is_listening = True
listening_thread = None
# 通过whisper做转换
def monter_whisper():
    global is_listening, listening_thread
    recognizer = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        
            recognizer.adjust_for_ambient_noise(source)
            print("请说话...")
            # 捕获音频
            try:
                audio = recognizer.listen(source)
                silent, audio_array=is_silent(audio)
                print(f"静音了吗？{'是' if silent else '否'}")
                if(silent):
                    print("声音太小，听不清！")
                else:
                    start_time = datetime.now()
                    # print(f"开始转换：{start_time}")
                    wav_data = wav_fp32_from_raw_data(audio_array)
                    # result = model.transcribe(audio_fp32,language="zh",fp16=False,initial_prompt='听起来不错')
                    result = model.transcribe(wav_data,language="zh",fp16=False,initial_prompt='听起来不错')
                    end_time = datetime.now()
                    # print(f"转换结束: {end_time}")
                    print(f"你说的是：{result['text']},耗时{end_time-start_time}")
                if is_listening:
                    monter_whisper()
                else:
                    if(listening_thread):
                       listening_thread.join()
                    print("已停止监听....")      
            except sr.WaitTimeoutError:
                print("监听超时")
            except KeyboardInterrupt:
                print("程序结束")
     
# 转换raw_data数据为wav fp32数据
def wav_fp32_from_raw_data(audio_array):
    wav_data = audio_array.flatten().astype(np.float32) / 32768.0
    return wav_data

def stop_listen():
    global listening_thread, is_listening
    is_listening = False
    print("停止监听....")

def start_listen():
    listening_thread = threading.Thread(target=monter_whisper)
    listening_thread.start()

start_listen()
# 等待一段时间以确保监听开始
time.sleep(60)
stop_listen()
