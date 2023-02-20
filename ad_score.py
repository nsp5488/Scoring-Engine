import pyads
from time import sleep

def score_AD(queue, alive, lock, servername,port, value=1):
    plc = None
    while alive():
        try:
            plc = pyads.Connection(servername)
            plc.open()
            lock.acquire()
            queue.put({'service': 'Active Direcctory', 'status': 'DOWN', 'host' : servername, 'value': value})
            lock.release()

        except Exception:
            lock.acquire()
            queue.put({'service': 'Active Directory', 'status': 'DOWN', 'host' : servername, 'value': value})
            lock.release()
        sleep(60)
    plc.close()
