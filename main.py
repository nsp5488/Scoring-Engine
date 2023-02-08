from queue import Queue
from http_score import score_HTTP
from smtp_score import score_SMTP
from icmp_score import score_ICMP
from dns_score import score_DNS
import requests
import threading

shared_queue = Queue()


def main():
    lock = threading.Lock()
    alive_bool = True
    alive = lambda : alive_bool
   # spawn the threads
    t1 = threading.Thread(target=score_HTTP, args=(shared_queue, alive, lock, 'http://google.com'))
    t1.start()
    t2 = threading.Thread(target=score_SMTP, args=(shared_queue, alive, lock, 'localhost'))
    t2.start()
    t3 = threading.Thread(target=score_ICMP, args=(shared_queue, alive, lock, 'localhost'))
    t3.start()
    t4 = threading.Thread(target=score_DNS, args=(shared_queue, alive, lock, '8.8.8.8'))
    t4.start()

    # main loop
    try:
        while(True):
            content = shared_queue.get()
            print(content)
            requests.post('http://localhost:5000/update_scores', content)
    except KeyboardInterrupt:
        print('exiting')

    alive_bool = False
    t1.join()
    t2.join()
    t3.join()
    t4.join()


if __name__ == '__main__':
    main()

