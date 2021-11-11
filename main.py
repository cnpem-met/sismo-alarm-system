import sys
from queue import Queue

from filemonitor import FileMonitor
from directory_cleaner import DirectoryCleaner
from config import PATH_TO_MONITOR, ALERT_ALARM_ENABLED
from ioc import IOC

def main():
    print('Starting program...')

    files_to_maintain = Queue()

    monitor = FileMonitor(path=PATH_TO_MONITOR, files_to_maintain=files_to_maintain)
    monitor.start()

    cleaner = DirectoryCleaner(path=PATH_TO_MONITOR, files_to_maintain=files_to_maintain)
    cleaner.start()

    if ALERT_ALARM_ENABLED:
        ioc = IOC()
        ioc.start()
        print('> IOC is on\n\n')
    


if __name__ == '__main__':
    main()
    sys.exit()