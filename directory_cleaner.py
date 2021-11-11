import os
from queue import Queue
import threading
import time
from datetime import datetime
from shutil import copy2

from utils import log
from config import ADJACENT_FILES_NUMBER

class DirectoryCleaner(threading.Thread):
    def __init__(self, path: str, files_to_maintain: Queue):
        super().__init__(daemon=True)
        self.kill = threading.Event()
        self.base_path = path
        self.files_to_maintain = files_to_maintain

    def create_directory(self, directories: list):
        # creating directory to save images
        path = os.path.join(*directories)

        if not os.path.exists(path):
            os.mkdir(path)

        return path

    def run(self):
        self.path = self.create_directory([self.base_path, 'alarm_data'])
        while not self.kill.is_set():
            time.sleep(3600)
            now = datetime.now()
            if now.hour >= 23:
                # creating dir specific for the current day
                ts = now.strftime("%d-%m-%Y")
                self.create_directory([self.path, ts])
                
                # saving files that contains data that triggered the alarm
                if not self.files_to_maintain.empty():
                    files = []
                    while not self.files_to_maintain.empty():
                        files.append(self.files_to_maintain.get())

                    for file in files:
                        # creating a directory specific to each alarm
                        save_path = self.create_directory([self.path, ts, os.path.basename(file).split('.')[0]])

                        # also saving x files right before and after based on the number in its name
                        ref_number = int(os.path.basename(file).split('.')[0].split('-')[1])
                        for i in range(ref_number - ADJACENT_FILES_NUMBER, ref_number + ADJACENT_FILES_NUMBER + 1):
                            file_to_save = file.replace(str(ref_number), str(i))
                            try:
                                copy2(file_to_save, os.path.join(save_path, os.path.basename(file_to_save)))
                            except (FileNotFoundError, PermissionError):
                                log(f'Failed to save file {os.path.basename(file_to_save)}.')


                    log(f'Files {[os.path.basename(file) for file in files]} and its neighbors maintained.')
                
                # excluding files
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f'[{now}] removing files...')
                for file in os.listdir(self.base_path):
                    if file.endswith('.txt'):
                        try:
                            os.remove(os.path.join(self.base_path, file))
                        except PermissionError:
                            log(f'Failed to exclude file {file}.')

                log('Files excluded.')

            