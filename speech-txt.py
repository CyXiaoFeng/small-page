import whisper
import speech_recognition as sr
import numpy as np

# 加载 Whisper 模型
model = whisper.load_model("base")

# 创建一个识别器实例
recognizer = sr.Recognizer()

# 使用麦克风作为音频源
with sr.Microphone() as source:
    print("请说话...")
    # 调整麦克风噪声水平
    recognizer.adjust_for_ambient_noise(source)
    # 捕获音频
    audio = recognizer.listen(source)

# 获取音频数据
audio_data = audio.get_raw_data()

# 将音频数据转换为 numpy 数组
audio_array = np.frombuffer(audio_data, dtype=np.int16)

# 转换为浮点型并归一化
audio_array = audio_array.astype(np.float32) / 32768.0

# 使用 Whisper 模型进行语音识别
result = model.transcribe(audio_array, language="zh", fp16=False)

# 输出识别结果
print("你说的是: " + result["text"])