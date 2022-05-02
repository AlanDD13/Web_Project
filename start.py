import time
from subprocess import *

Popen('python parser_updater.py')
time.sleep(1)
Popen('python main.py')
