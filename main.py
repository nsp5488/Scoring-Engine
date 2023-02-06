from queue import Queue
from http_score import score_HTTP
from ssh_score import score_SSH
from ftp_score import score_FTP
from sql_score import score_SQL
import threading

shared_queue = Queue()


def main():
    alive = True
    lock = threading.Lock()

   # spawn the threads
    t = threading.Thread(target=score_HTTP, args=(shared_queue, alive, lock, 'http://google.com'))
    t.start()

    t = threading.Thread(target=score_SSH, args=(shared_queue, alive, lock))
    t.start()

    t = threading.Thread(target=score_FTP, args=(shared_queue, alive, lock))
    t.start()
    
    t = threading.Thread(target=score_SQL, args=(shared_queue, alive, lock))
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

