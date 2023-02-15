from rocketchat_API.rocketchat import RocketChat
from time import sleep


def score_rocket_chat(queue, alive, lock, server, value):
    while alive():
        try:
            rocket = RocketChat('Username', 'Password', server_url=server)
            
            lock.aquire()
            queue.put({'service': 'RocketChat', 'status': 'UP', 'host':server, 'value':value})
            lock.release()

        # SQL Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'RocketChat', 'status': 'DOWN', 'host':server, 'value':value})
            lock.release()
        sleep(60)

