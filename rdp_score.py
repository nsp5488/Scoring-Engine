from time import sleep
import socket

PORT = 3389

def score_RDP(queue, alive, lock, server, value):
    while alive():
        try:
            s = socket.socket((server, PORT))
            s.connect()
            
            # SQL Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'RDP', 'status': 'UP', 'host':server, 'value':value})
            lock.release()

        # SQL Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'RDP', 'status': 'DOWN', 'host':server, 'value':value})
            lock.release()
        sleep(60)