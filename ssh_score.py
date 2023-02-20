import paramiko
from time import sleep

DPORT = '22'
DUSERNAME = 'root'
DPASSWORD = 'password'

def score_SSH(queue, alive, lock, target, port=DPORT, value=1, username=DUSERNAME, password=DPASSWORD):
    while alive():
        try:
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(target, int(port), username, password)
            
            # SSH Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'ssh', 'status': 'UP', 'host':target, 'value': value})
            lock.release()

        # SSH Server failed to login
        except paramiko.ssh_exception.AuthenticationException:
            queue.put({'service': 'ssh', 'status': 'UP', 'host':target, 'value': value})

        # SSH Server failed to respond
        except:
            print('connection error')
            lock.acquire()
            queue.put({'service': 'ssh', 'status': 'DOWN', 'host':target, 'value':value})
            lock.release()
            
        sleep(60)
