import smbclient
from time import sleep

USERNAME = "username"
PASSWORD = "password"

def score_SMB(queue, alive, lock, target):
    while alive():
        try:
            
            smbclient.register_session(target, USERNAME, PASSWORD)
            lock.acquire()
            queue.put({'service': 'smb', 'status': 'UP', 'host' : target})
            lock.release()
        except Exception:
            lock.acquire()
            queue.put({'service': 'smb', 'status': 'DOWN', 'host' : target})
            lock.release()
        sleep(60)