import json
import requests
import pandas as pd
import threading
import time

StartTime=time.time()

INTERVAL_IN_SECONDS = 30

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()


def getMinterChanges():
    query = """
    {
      minters{
        id
        address
      }
    }
    """
    request = requests.post('https://api.thegraph.com/subgraphs/id/QmbuC5GvyA9eFq8vKBAvEj4ZRjSdbzrW9WgeSqtyMW3dM2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def action():
    transfers_data = getMinterChanges()
    transfers_data = transfers_data['data']['minters']
    df = pd.DataFrame(transfers_data)
    file = open('minters.txt', 'w')
    file.write(df.to_string())
if __name__== "__main__":
    action()
    inter = setInterval(INTERVAL_IN_SECONDS, action)
