# Libraries
import os
from queue import Queue
import time
import threading
from datetime import datetime, timedelta

from alarm import run_alarm_checking
from utils import log

class FileMonitor(threading.Thread):
    
    def __init__(self, path, files_to_maintain: Queue):
        super().__init__(daemon=True)
        self.kill = threading.Event()
        self.path = path
        self.files_to_maintain = files_to_maintain    
        
    def search_files(self):
        files = set(os.listdir(self.path))
        return files
    
    def run(self):
        # self.record_action("[%s] Action: start raw file monitor" % self.get_datetime())
        previous_files = self.search_files()
        last_alarm_time = datetime.now() - timedelta(days = 1)
        while not self.kill.is_set():
            files = self.search_files()
            diff = files.difference(previous_files)
            # Caso identificado um novo arquivo na pasta, realiza a conversao
            if diff:
                filename = list(diff)[0]
                if filename.endswith('.txt'):
                    alarm, messages = run_alarm_checking(path = os.path.join(self.path, filename), last_alarm = last_alarm_time)
                    if alarm:
                        _ = [log(message) for message in messages]
                        last_alarm_time = datetime.now()
                        self.files_to_maintain.put(os.path.join(self.path, filename))

            previous_files = files
            time.sleep(2)