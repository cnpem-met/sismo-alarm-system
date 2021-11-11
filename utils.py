from datetime import datetime
from enum import Enum, auto

class Severity(Enum):
    DANGER = auto()
    ALERT = auto()


def log(text):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f'[{now}] {text}\n'

    monitor = open("log.txt", "a")
    monitor.write(text)
    monitor.close()