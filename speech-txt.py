import whisper
import speech_recognition as sr
import numpy as np
import io
import os
from queue import Queue
import soundfile as sf
model = whisper.load_model("base")


#初始化数据
data_queue = Queue()
# 创建一个识别器实例
recognizer = sr.Recognizer()



# 使用麦克风作为音频源
with sr.Microphone(sample_rate=16_000) as source:
    print("请说话...")
    # 调整麦克风噪声水平
    recognizer.adjust_for_ambient_noise(source)
    # 捕获音频
    audio = recognizer.listen(source)

    wav_data = audio.get_wav_data()
    wav_stream = io.BytesIO(wav_data)
    audio_array,_ = sf.read(wav_stream)
    audio_fp32 = audio_array.astype(np.float32)
    result = model.transcribe(audio_fp32,language="zh",fp16=False,initial_prompt='听起来不错')
    print(result["text"])

# 获取音频数据
audio_data = audio.get_raw_data()
data_queue.put(audio_data)
def whisper_to_E_text(tmpfile="./temp.wav"):
    result = model.transcribe(tmpfile, language="zh", fp16=False, temperature=0.4,initial_prompt='听起来不错')
    text = result['text'].strip()
    print(f"text: {text}")
    return text

def _audio(audio_data):
    try:
        wav = sr.AudioData(audio_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
        wav_data = io.BytesIO(wav.get_wav_data())
        with open("temp.wav", 'w+b') as f:
            f.write(wav_data.read())
        print("save as")
        whisper_to_E_text("temp.wav")
    except Exception as e:
        print(f"An error occurred: {e}")

_audio(audio_data)




# 将音频数据转换为 numpy 数组

wav_data = np.frombuffer(audio_data, dtype=np.int16).flatten().astype(np.float32) / 32768.0


audio_array = np.expand_dims(wav_data, axis=0)

# audio_array = np.frombuffer(audio_data, dtype=np.int16)

# # 转换为浮点型并归一化
# audio_array = audio_array.astype(np.float32) / 32768.0

# 使用 Whisper 模型进行语音识别
result = model.transcribe(wav_data, language="zh", fp16=False, initial_prompt='听起来不错')

# 输出识别结果
print("你说的是: " + result["text"])