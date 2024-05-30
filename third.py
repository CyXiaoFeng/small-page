import threading
import time

# 定义全局变量来控制线程的运行
running = True

def long_running_task():
    while running:
        print("任务正在运行...")
        time.sleep(1)
    print("任务已停止")

def start_task():
    global task_thread
    task_thread = threading.Thread(target=long_running_task)
    task_thread.start()

def stop_task():
    global running
    running = False
    task_thread.join()  # 等待线程结束

# 启动任务
start_task()

# 主线程等待一段时间后停止任务
time.sleep(5)
stop_task()

print("主线程已结束")
