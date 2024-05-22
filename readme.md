## 创建并进入虚拟环境
    python -m venv venv
    .\venv\Scripts\activate
## 安装依赖包
    pip install --no-cache-dir -r requirements.txt

## 初始化数据
    python .\engine\db.py

## 执行程序
    python .\main.py

## 目前支持的命令说明
> 1. 打开一个本地程序时，命令必须包含"open"，例如说：open word
> 2. 用油管播放时，命令必须包含"on youtube"，例如说：play Never Gonna Give You Up on youtube
> 3. 查询天气时，命令必须包含"weather in 城市"，例如说：weather in beijing
> 4. 播放烟花，命令必须包含"play video"，例如说：wplay video
> 上述4个命令可在engine\command.py的allCommands方法中自定义，依赖语音识别的方便程度，
    
## db.py中的sql语句全部改为小写（因为代码中的关键字都被转为小写了）

## db.py中的可执行程序位置必须正确