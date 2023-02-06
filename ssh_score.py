import paramiko
from time import sleep

ssh_hostname = 'localhost'
ssh_port = 22
ssh_username = 'username'
ssh_password = 'password'

def score_SSH(queue, alive, lock):
    while alive:
        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()

            s.connect(ssh_hostname, ssh_port, ssh_username, ssh_password, timeout=5)
            
            # SSH Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'ssh', 'status': 'UP'})
            lock.release()

        # SSH Server failed to login
        except paramiko.AuthenticationException:
            print("SSH credentials bad")

        # SSH Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'ssh', 'status': 'DOWN'})
            lock.release()
        sleep(60)