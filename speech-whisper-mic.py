import speech_recognition as sr
import whisper
import numpy as np
import torch

# 检查是否有 GPU 可用
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("base", device=device)

# 初始化识别器
recognizer = sr.Recognizer()

# 设置麦克风采样率
sample_rate = 16_000

def audio_to_text(audio_data):
    # 将 AudioData 转换为 numpy 数组
    wav_data = np.frombuffer(audio_data.get_wav_data(), np.int16).flatten().astype(np.float32) / 32768.0
    
    # Whisper 要求输入音频数据范围在 [-1, 1] 之间
    result = model.transcribe(wav_data ,language="zh", fp16=False, initial_prompt='听起来不错')
    
    # 提取转录结果文本
    text = result['text']
    
    return text

def callback(_, audio:sr.AudioData):
    print("回调")
    try:
        # 使用 Whisper 进行语音转文字
        text = audio_to_text(audio)
        print("转录结果: " + text)
    except Exception as e:
        print(f"识别错误: {e}")

with sr.Microphone(sample_rate=sample_rate) as source:
    recognizer.adjust_for_ambient_noise(source)
    print("请开始说话...")
    
stop_listening = recognizer.listen_in_background(source, callback)
try:
    while True:
        pass
except KeyboardInterrupt:
    stop_listening(wait_for_stop=False)
print("程序结束")