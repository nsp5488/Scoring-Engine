from queue import Queue
import sys
import pandas as pd
from http_score import score_HTTP
from ssh_score import score_SSH
from ftp_score import score_FTP
from sql_score import score_SQL
from smtp_score import score_SMTP
from icmp_score import score_ICMP
from dns_score import score_DNS
from smb_score import score_SMB
from ad_score import score_AD
from nextcloud_score import score_NextCloud
from rocket_chat_score import score_rocket_chat
from rdp_score import score_RDP
import requests
import threading

shared_queue = Queue()
flaskServAddr = 'http://localhost:5000/update_scores'
host_list = 'xxx.csv'


def spawn_threads():

    df = pd.read_csv(host_list)
    threads = []
    for row in df:
        protocol = row['Service']
        host = row['Host (IP)']
        port = row['Port (Leave blank for default)']
        value = row['Value']

        # because python hates me and added match statements in 3.10
        if protocol == 'HTTP':
            target = score_HTTP
        elif protocol == 'SMTP':
            target = score_SMTP
        elif protocol == 'ICMP':
            target = score_ICMP
        elif protocol == 'DNS':
            target = score_DNS
        elif protocol == 'SSH':
            target = score_SSH
        elif protocol == 'SQL':
            target = score_SQL
        elif protocol == 'FTP':
            target = score_FTP
        elif protocol == 'SMB':
            target = score_SMB
        elif protocol == 'RDP':
            target = score_RDP
        elif protocol == 'AD':
            target = score_AD
        elif protocol == 'RocketChat':
            target = score_rocket_chat
        elif protocol == 'Nextcloud':
            target = score_NextCloud
        else:
            print("Undefined protocol in input")
            exit(-1)

        t = threading.Thread(target=target, args=(shared_queue, alive, lock, host, port, value))
        threads.add(t)
    return threads

def main():
    lock = threading.Lock()
    alive_bool = True
    alive = lambda : alive_bool

    # spawn the threads
    # for thread in spawn_threads(): # uncomment once we have the CSV of hosts
    #     thread.start()
    value = 1
    t1 = threading.Thread(target=score_HTTP, args=(shared_queue, alive, lock, 'http://google.com', value))
    t1.start()
    t2 = threading.Thread(target=score_SMTP, args=(shared_queue, alive, lock, 'mail.rit.edu', value))
    t2.start()
    t3 = threading.Thread(target=score_ICMP, args=(shared_queue, alive, lock, 'localhost', value))
    t3.start()
    t4 = threading.Thread(target=score_DNS, args=(shared_queue, alive, lock, '8.8.8.8', value))
    t4.start()
    t5 = threading.Thread(target=score_SSH, args=(shared_queue, alive, lock, 'glados.cs.rit.edu', value))
    t5.start()
    t6 = threading.Thread(target=score_SQL, args=(shared_queue, alive, lock, 'localhost', value))
    t6.start()
    t7 = threading.Thread(target=score_FTP, args=(shared_queue, alive, lock, 'localhost', value))
    t7.start()
    t8 = threading.Thread(target=score_SMB, args=(shared_queue, alive, lock, 'localhost', value))
    t8.start()
    t9 = threading.Thread(target=score_AD, args=(shared_queue, alive, lock, 'domainname.com', 'username', 'password'))
    t9.start()
    t10 = threading.Thread(target=score_NextCloud, args=(shared_queue, alive, lock, 'http://url:80', 'username', 'password'))
    t10.start()

    # main loop
    try:
        red_score = 0
        blue_score = 0
        while(True):
            content = shared_queue.get()

            if content['status'] == 'UP':  # Change these to talk to the database
                blue_score += content['value']
            else:
                red_score += content['value']
            print(f"Blue score: {blue_score}\n Red Score: {red_score}\n\n")


            try:
                print(f"Posting {content} to {flaskServAddr}\n")
                res = requests.post(flaskServAddr, content)
                print(f"Received response: {res} from {flaskServAddr}\n\n")

            except requests.exceptions.ConnectionError:
                print("Error while connecting to the webserver!", file=sys.stderr)

    except KeyboardInterrupt:
        print('\n\nAttempting to exit gracefully....')
    alive_bool = False

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()

    # for thread in threads:
    #     thread.join()

    print("All threads shutdown successfully!")


if __name__ == '__main__':
    main()

