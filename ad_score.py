from pyad import *
from time import sleep

def score_AD(queue, alive, lock, servername, username='User', password='Pass'):
    pyad.set_defaults(ldap_server=servername, username=username, password=password)
    while alive():
        try:
            user = pyad.aduser.ADUser.from_cn("myuser")
            if user is not None:
                lock.acquire()
                queue.put({'service': 'ad', 'status': 'UP', 'host' : servername})
                lock.release()
            else:
                lock.acquire()
                queue.put({'service': 'ad', 'status': 'DOWN', 'host' : servername})
                lock.release()
        except Exception:
            lock.acquire()
            queue.put({'service': 'ad', 'status': 'DOWN', 'host' : servername})
            lock.release()
        sleep(60)
