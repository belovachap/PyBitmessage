import Queue
import threading

import addresses
from helper_threading import StoppableThread
from .fix_circular_imports import BMConnectionPool
from queues import addrQueue
import protocol
import state

class AddrThread(threading.Thread, StoppableThread):
    def __init__(self):
        threading.Thread.__init__(self, name="AddrBroadcaster")
        self.initStop()
        self.name = "AddrBroadcaster"

    def run(self):
        while not state.shutdown:
            chunk = []
            while True:
                try:
                    data = addrQueue.get(False)
                    chunk.append((data[0], data[1]))
                    if len(data) > 2:
                        source = BMConnectionPool().getConnectionByAddr(data[2])
                except Queue.Empty:
                    break
                except KeyError:
                    continue

            #finish

            addrQueue.iterate()
            for i in range(len(chunk)):
                addrQueue.task_done()
            self.stop.wait(1)
