import paramiko
from time import sleep

DPORT = 22
DUSERNAME = 'root'
DPASSWORD = 'password'

def score_SSH(queue, alive, lock, target, value, port=DPORT, username=DUSERNAME, password=DPASSWORD):
    while alive():
        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()

            s.connect(target, port, username, password, timeout=5)
            
            # SSH Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'ssh', 'status': 'UP', 'host':target, 'value': value})
            lock.release()

        # SSH Server failed to login
        except paramiko.AuthenticationException:
            # print("SSH credentials bad") # Commented out because this still allows us to check that the service is up
            queue.put({'service': 'ssh', 'status': 'UP', 'host':target, 'value': value})

        # SSH Server failed to respond
        except:
            print('connection error')
            lock.acquire()
            queue.put({'service': 'ssh', 'status': 'DOWN', 'host':target, 'value':value})
            lock.release()
            
        sleep(60)