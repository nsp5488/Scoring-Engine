import paramiko
from time import sleep

port = 22
username = 'username'
password = 'password'

def score_SSH(queue, alive, lock, target):
    while alive():
        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()

            s.connect(ssh_hostname, port, username, password, timeout=5)
            
            # SSH Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'ssh', 'status': 'UP', 'host':target})
            lock.release()

        # SSH Server failed to login
        except paramiko.AuthenticationException:
            print("SSH credentials bad")

        # SSH Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'ssh', 'status': 'DOWN', 'host':target})
            lock.release()
        sleep(60)