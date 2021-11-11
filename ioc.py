import threading
from pcaspy import SimpleServer, Driver

from config import PV_NAME
   

class EpicsDriver(Driver):
    def _init_(self):
        super().__init__()
        
    def write(self, reason, value):
        self.setParam(reason, value) 
        
    def read(self, reason):
        return self.getParam(reason)
        
class IOC(threading.Thread):
    
    driver = None
    
    def _init_(self):
        super().__init__(daemon=True)
        self.kill = threading.Event()
        
    def run(self):
        server = SimpleServer()

        pv = {PV_NAME: {'type': 'int', 'scan': 1}}

        server.createPV("", pv)
        IOC.driver = EpicsDriver()
        while True:
            server.process(0.1)