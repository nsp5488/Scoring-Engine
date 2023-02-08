import dns.message, dns.query
from time import sleep

DPORT = 53 # UDP

def score_DNS(queue, alive, lock, target, target_port=DPORT):
    query = dns.message.make_query(".", dns.rdatatype.NS, flags=0) # Create a query to 

    while alive():
        try:
            res = dns.query.udp(query, target, timeout=10)
            if res.answer is not None:
                lock.acquire()
                queue.put({'service': 'dns', 'status': 'UP', 'host' : target})
                lock.release()
            else:
                lock.acquire()
                queue.put({'service': 'dns', 'status': 'DOWN', 'host' : target})
                lock.release()
        except Exception:
            lock.acquire()
            queue.put({'service': 'dns', 'status': 'DOWN', 'host' : target})
            lock.release()
        sleep(60)