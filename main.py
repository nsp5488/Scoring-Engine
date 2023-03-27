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
from imap_score import score_IMAP
from nextcloud_score import score_NextCloud
from rocket_chat_score import score_rocket_chat
from rdp_score import score_RDP
import requests
import threading

shared_queue = Queue()
flaskServAddr = 'http://127.0.0.1:5000'
host_list = 'services.csv'
SCORE_FILE = 'scores.txt'
lock = threading.Lock()


def spawn_threads(alive):

    df = pd.read_csv(host_list)
    threads = []
    for idx, row in df.iterrows():
        protocol = row['Service']
        host = row['Host (IP)']
        port = row['Port (Leave blank for default)']
        value = int(row['Value'])
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
        elif protocol == 'NextCloud':
            target = score_NextCloud
        elif protocol == 'IMAP':
            target = score_IMAP
        else:
            print("Undefined protocol in input")
            exit(-1)

        t = threading.Thread(target=target, args=(shared_queue, alive, lock, host, port, value))
        threads.append(t)
    return threads

def main():
    alive_bool = True
    alive = lambda : alive_bool
    threads = spawn_threads(alive)
    # spawn the threads
    for thread in threads:
        thread.start()

    # main loop
    try:
        red_score = 0
        blue_score = 0
        try: 
            f = open(SCORE_FILE, 'r')
            line = f.readline()
            scores = line.split(',')
            print(f"Reading scores from file: blue: {scores[0]}, red: {scores[1]}")
            # If we got this far, the score file exists and is populated.
            blue_score = int(scores[0])
            red_score = int(scores[1])
        except FileNotFoundError:
            red_score = 0
            blue_score = 0

        while(True):
            content = shared_queue.get()
            print(content)

            if content['status'] == 'UP':
                blue_score += int(content['value'])
            else:
                red_score += int(content['value'])
            
            print(f"Blue score: {blue_score}\n Red Score: {red_score}\n\n")


            try:
                print(f"Posting {content} to {flaskServAddr}\n")
                res = requests.post(flaskServAddr + '/update_services', content)
                print(f"Received response: {res} from {flaskServAddr}\n\n")
                print(f"Posting current scores to {flaskServAddr}\n")
                res = requests.post(flaskServAddr + '/update_scores', {'blue_score' : blue_score, 'red_score' : red_score})
                print(f"Received response: {res} from {flaskServAddr}\n\n")
            except requests.exceptions.ConnectionError:
                print("Error while connecting to the webserver!", file=sys.stderr)

    except KeyboardInterrupt:
        print('\n\nAttempting to exit gracefully....')
    alive_bool = False


    for thread in threads:
        thread.join()

    print("All threads shutdown successfully!")
    print("Writing score state: ")
    with open(SCORE_FILE, 'w') as f:
        f.write(f"{blue_score}, {red_score}")
    


if __name__ == '__main__':
    main()

