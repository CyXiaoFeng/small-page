import os
import eel

from engine.features import *
from engine.command import *    #导入command的所有功能
eel.init("www")

os.system('start msedge.exe --app="http://localhost:8000/index.html"')

eel.start('index.html',mode=None,host='localhost',block=True)
