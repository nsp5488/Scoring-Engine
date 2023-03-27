import ldap
from time import sleep

def score_AD(queue, alive, lock, servername,port, value=1):
    while alive():
        try:
            l = ldap.initialize('ldap://192.168.2.3')
            l.simple_bind_s()

            l.search('(&(objectCategory=person)(objectClass=user))', ldap.SCOPE_SUBTREE)
            lock.acquire()
            queue.put({'service': 'Active Directory', 'status': 'UP', 'host' : servername, 'value': value})
            lock.release()

        except Exception:
            lock.acquire()
            queue.put({'service': 'Active Directory', 'status': 'DOWN', 'host' : servername, 'value': value})
            lock.release()
        sleep(60)
