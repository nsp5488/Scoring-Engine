from ftplib import FTP, error_perm
from time import sleep

DUSERNAME = 'username'
DPASSWORD = 'password'
DPORT = 21

def score_FTP(queue, alive, lock, target,port=DPORT, value=1, username=DUSERNAME, password=DPASSWORD):
    while alive():
        try:
        
            ftp = FTP(target)
            ftp.login()
            ftp.quit()
            
            # FTP Server connects sucessfully 
            lock.acquire()
            queue.put({'service': 'FTP', 'status': 'UP', 'host':target, 'value':value})
            lock.release()
        except error_perm:
            queue.put({'service': 'FTP', 'status': 'UP', 'host':target, 'value':value})
        # FTP Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'FTP', 'status': 'DOWN', 'host':target, 'value':value})
            lock.release()
        sleep(60)
