import requests
from time import sleep
DPORT = 80

def score_HTTP(queue, alive, lock, target, target_port=DPORT):
    while alive():
        try:
            res = requests.get(target, timeout=5)

            # We got a 200 response code
            if res.ok:
                lock.acquire()
                queue.put({'service': 'http', 'status': 'UP', 'host':target})
                lock.release()
            # We got a non-200 response code
            else:
                lock.acquire()
                queue.put({'service': 'http', 'status': 'DOWN', 'host':target})
                lock.release()

        # HTTP Server failed to respond
        except requests.exceptions.ConnectionError:
            lock.acquire()
            queue.put({'service': 'http', 'status': 'DOWN', 'host':target})
            lock.release()
        sleep(60)


       
