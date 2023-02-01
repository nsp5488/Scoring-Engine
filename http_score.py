import requests
from time import sleep

def score_HTTP(queue, alive, lock, target):
    while alive:
        try:
            res = requests.get(target, timeout=5)

            # We got a 200 response code
            if res.ok:
                lock.acquire()
                queue.put({'service': 'http', 'status': 'OK'})
                lock.release()
            # We got a 
            else:
                lock.acquire()
                queue.put({'service': 'http', 'status': 'DOWN'})
                lock.release()

        # HTTP Server failed to respond
        except requests.exceptions.ConnectionError:
            lock.acquire()
            queue.put({'service': 'http', 'status': 'DOWN'})
            lock.release()
        sleep(60)


       
