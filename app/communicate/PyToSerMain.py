from ArduinoConection import ArduinoConection
from threading import Thread
from multiprocessing.connection import Listener
from multiprocessing.connection import Client

import time

def SerDuplexRead(ArdCon):
    for i in range(0,100):
        readInput = ArdCon.readline()
        address = ('localhost', 6300)
        con = Client(address, authkey=b'PyToPyCom')
        con.send(readInput)
        con.close()

def SerDuplexWrite(ArdCon):    
    for i in range(0,100):
        print("listen on port 6200")
        address = ('localhost', 6200)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        print ('connection accepted from {}'.format(listener.last_accepted))
        
        msg = con.recv()
        try:
            ArdCon.write(str.encode(msg))
        except:
            listener.close()
            return
        listener.close()

def WaitForPyReq(ArdCon):
    while True:
        print("listen on port 6000")
        address = ('localhost', 6000)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        print ('connection accepted from {}'.format(listener.last_accepted))
        while True:
            msg = con.recv()
            if msg == 'ArdConState':
                con.send(str(ArdCon.getArdConState()))
            elif msg == 'CommunicationState':
                con.send(str(ArdCon.getArdComState()))
            else:
                con.close()
                break
        listener.close()

def main():
    # TODO read this identifier from the STDIn to get the information >> Max in following
    ArdCon = ArduinoConection("936DA01F-9ABD-4D9D-80C7-02AF85C822A8")
    PyListener = Thread(target=WaitForPyReq,args=(ArdCon,))
    PySerWrite = Thread(target=SerDuplexWrite,args=(ArdCon,))
    PySerRead = Thread(target=SerDuplexRead,args=(ArdCon,))
    print("waiting 5")
    time.sleep(5)
    print("starting the threads")
    PyListener.start()
    if (ArdCon != None):
        PySerWrite.start()
        PySerRead.start()
    '''for i in range(0,20):
        time.sleep(2)
        print("con-try {}:".format(i))
        print(ArdCon.getArdConState())
        print(ArdCon.getArdComState())
    print("Wait for ListenerThread")
    PyListener.join()
    print("finished")'''
    
    
if __name__ == '__main__':
    main() 