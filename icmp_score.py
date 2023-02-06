from icmplib import ping
from time import sleep


def score_ICMP(queue, alive, lock, target):
    while(alive):
        try:
            host = ping(target, privileged=False)

            if host.is_alive: # Is alive === reachable
                queue.put({'service': 'icmp', 'status': 'UP', 'host' : target}) 
            else:
                queue.put({'service': 'icmp', 'status': 'DOWN', 'host' : target})

        except Exception: # I don't think this is reachable, but just in case.
            print('ahhhh!')
            queue.put({'service': 'icmp', 'status': 'DOWN', 'host' : target})
        sleep(60)

