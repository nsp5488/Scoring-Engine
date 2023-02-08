from ftplib import FTP
from time import sleep

username = 'username'
password = 'password'

def score_FTP(queue, alive, lock, target):
    while alive():
        try:
            ftp = FTP(target, username, password, timeout=5)
            ftp.login()
            ftp.quit()
            
            # FTP Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'ftp', 'status': 'UP', 'host':target})
            lock.release()

        # FTP Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'ftp', 'status': 'DOWN', 'host':target})
            lock.release()
        sleep(60)