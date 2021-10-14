import json
import requests
import pandas as pd
import threading
import time

StartTime=time.time()

AMOUNT_MIN = 1
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


def getDaoTransfers(amount, timestamp):
    query = """
    {
      transfers(orderBy:timestamp, orderDirection:desc, where:{amount_gte:%d, timestamp_gte:%d, from:"0x245cc372C84B3645Bf0Ffe6538620B04a217988B"}){
        id
        from
        to
        amount
        timestamp
      }
    }
    """ % (amount, timestamp)
    request = requests.post('https://api.thegraph.com/subgraphs/id/QmbuC5GvyA9eFq8vKBAvEj4ZRjSdbzrW9WgeSqtyMW3dM2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def action():
    timestamp = time.time() - INTERVAL_IN_SECONDS - 20
    dao_data = getDaoTransfers(AMOUNT_MIN, timestamp)
    dao_data = dao_data['data']['transfers']
    df = pd.DataFrame(dao_data)
    file = open('dao.txt', 'w')
    file.write(df.to_string())
if __name__== "__main__":
    action()
    inter = setInterval(INTERVAL_IN_SECONDS, action)
