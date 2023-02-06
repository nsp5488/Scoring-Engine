import dnspython
from time import sleep

DPORT = 53 # UDP

def score_DNS(queue, alive, lock, target, target_port=DPORT):
    while alive:

        n = dnspython.dns.name(target)
        