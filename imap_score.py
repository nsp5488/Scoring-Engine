from imaplib import IMAP4
from time import sleep

def score_IMAP(queue, alive, lock, server, value):
    while alive():
        try:
            M = IMAP4(server)
            res = M.noop()           
            lock.aquire()
            queue.put({'service': 'RocketChat', 'status': 'UP', 'host':server, 'value':value})
            lock.release()

        # SQL Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'RocketChat', 'status': 'DOWN', 'host':server, 'value':value})
            lock.release()
        sleep(60)
