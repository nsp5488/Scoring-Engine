from smtplib import SMTP
from time import sleep
DPORT = 587

def score_SMTP(queue, alive, lock, target, target_port=DPORT):
    mail_server = SMTP()
    while alive:

        try:
            conn = mail_server.connect(host=target, port=target_port)
            conn.ehlo_or_helo_if_needed()
            
            # if we got this far, the server properly responded
            lock.acquire()
            queue.put({'service': 'smtp', 'status': 'UP', 'host' : target})
            lock.release()
        except Exception: # If any exception is thrown, it's the result of the server being down or misconfigured
            lock.acquire()
            queue.put({'service': 'smtp', 'status': 'DOWN', 'host' : target})
            lock.release()
        
        sleep(60)



