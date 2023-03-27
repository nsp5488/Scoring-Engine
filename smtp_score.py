from smtplib import SMTP
from time import sleep
DPORT = 587

def score_SMTP(queue, alive, lock, target, port=DPORT, value=1):
    mail_server = SMTP()
    while alive():

        try:
            conn = mail_server.connect(host=target, port=int(port))
            
            # if we got this far, the server properly responded
            lock.acquire()
            queue.put({'service': 'SMTP', 'status': 'UP', 'host' : target, 'value':value})
            lock.release()
        except Exception: # If any exception is thrown, it's the result of the server being down or misconfigured
            lock.acquire()
            queue.put({'service': 'SMTP', 'status': 'DOWN', 'host' : target, 'value':value})
            lock.release()
        
        sleep(60)



