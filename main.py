from queue import Queue
from http_score import score_HTTP
import threading

shared_queue = Queue()


def main():
    alive = True
    lock = threading.Lock()

   # spawn the threads
    t = threading.Thread(target=score_HTTP, args=(shared_queue, alive, lock))
    t.start()

    # main loop
    try:
        while(True):
            print(shared_queue.get())
    except KeyboardInterrupt:
        print('exiting')

    alive = False



if __name__ == '__main__':
    main()

