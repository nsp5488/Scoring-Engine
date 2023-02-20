from ftplib import FTP
from time import sleep

DUSERNAME = 'username'
DPASSWORD = 'password'
DPORT = 21

def score_FTP(queue, alive, lock, target,port=DPORT, value=1, username=DUSERNAME, password=DPASSWORD):
    while alive():
        #try:
        print(target)
        print(username)
        print(password)
        
        ftp = FTP(target)
        ftp.login()
        ftp.quit()
        
        # FTP Server connects sucessfully 
        lock.aquire()
        queue.put({'service': 'ftp', 'status': 'UP', 'host':target, 'value':value})
        lock.release()

        # FTP Server failed to respond
        #except:
        #    lock.acquire()
        #    queue.put({'service': 'ftp', 'status': 'DOWN', 'host':target, 'value':value})
        #    lock.release()
        sleep(60)
