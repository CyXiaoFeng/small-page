import os
import eel
import multiprocessing
from engine.features import *
from engine.command import *    #导入command的所有功能
eel.init("www")
def oth_thread():
     while True:
        #   print("i am a thread")
          eel.sleep(1)
eel.spawn(oth_thread)
def start():
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html',mode='chrom',host='localhost',block=True)

if __name__ == '__main__':
     p1 = multiprocessing.Process(target=start)
     p1.start()