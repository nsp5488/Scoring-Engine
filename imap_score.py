from imaplib import IMAP4
from time import sleep

def score_IMAP(queue, alive, lock, server, port, value):
    while alive():
        try:
            M = IMAP4(server)
            res = M.noop()           
            lock.acquire()
            queue.put({'service': 'IMAP', 'status': 'UP', 'host':server, 'value':value})
            lock.release()

        # SQL Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'IMAP', 'status': 'DOWN', 'host':server, 'value':value})
            lock.release()
        sleep(60)
