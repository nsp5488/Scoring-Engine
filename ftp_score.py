from ftplib import FTP
from time import sleep

hostname = 'localhost'
username = 'username'
password = 'password'

def score_FTP(queue, alive, lock):
    while alive:
        try:
            ftp = FTP(hostname, username, password, timeout=5)
            ftp.login()
            ftp.quit()
            
            # FTP Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'ftp', 'status': 'UP'})
            lock.release()

        # FTP Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'ftp', 'status': 'DOWN'})
            lock.release()
        sleep(60)