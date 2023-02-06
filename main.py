from queue import Queue
from http_score import score_HTTP
from smtp_score import score_SMTP
from icmp_score import score_ICMP
import threading

shared_queue = Queue()


def main():
    alive = True
    lock = threading.Lock()

   # spawn the threads
    t1 = threading.Thread(target=score_HTTP, args=(shared_queue, alive, lock, 'http://google.com'))
    t1.start()
    t2 = threading.Thread(target=score_SMTP, args=(shared_queue, alive, lock, 'localhost'))
    t2.start()
    t3 = threading.Thread(target=score_ICMP, args=(shared_queue, alive, lock, 'localhost'))
    t3.start()
    # main loop
    try:
        while(True):
            print(shared_queue.get())
    except KeyboardInterrupt:
        print('exiting')

    alive = False
    t1.join()
    t2.join()
    t3.join()



if __name__ == '__main__':
    main()

