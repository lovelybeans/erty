import subprocess
import time
import sys

print('Starting launcher.py')

print('a')
api = subprocess.Popen([sys.executable, "api.py"])
print('b')
#bot = subprocess.Popen([sys.executable, "bot.py"])
print('c')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:

    print('Stopping...')
    api.terminate()
    #bot.terminate()
    print('Stopped all processes.')