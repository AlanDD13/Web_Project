import time
from parser import parse

import schedule

print('Hello There')
schedule.every(3).hours.do(parse())

while True:
    schedule.run_pending()
    time.sleep(1)
