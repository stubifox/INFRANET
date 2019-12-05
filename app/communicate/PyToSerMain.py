from ArduinoConection import ArduinoConection

from threading import Thread
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import time

# thread function: Listener on Serial, write to DB


def serDuplexRead(ardCon):
    while(True):
        readInput = str.decode(ardCon.readline())
        # filter
        if readInput in ('', '\n'):
            continue
        # TODO use decryption here
        # TODO write to DB instead of console
        address = ('localhost', 6300)
        con = Client(address, authkey=b'PyToPyCom')
        con.send(readInput)
        con.close()

# thread function: Listener to write recieved message on serial connection


def serDuplexWrite(ardCon):
    # TODO use encryption here
    # TODO return error Msg to FE to tell user message could not be send
    while(True):
        address = ('localhost', 6200)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        msg = con.recv()
        try:
            ardCon.write(str.encode(msg))
        except:
            listener.close()
            return
        listener.close()

# thread function: Listener for Arduino State requests


def waitForArdStateReq(ardCon):
    while True:
        address = ('localhost', 6000)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        msg = con.recv()
        if msg == 'ArdConState':
            con.send(str(ardCon.getArdConState()))
        elif msg == 'CommunicationState':
            con.send(str(ardCon.getArdComState()))
        con.close()
        listener.close()


def main():
    # TODO read this identifier from the STDIn to get the information >> Max in following
    ardCon = ArduinoConection("936DA01F-9ABD-4D9D-80C7-02AF85C822A8")
    ardStateReqListener = Thread(target=waitForArdStateReq, args=(ardCon,))
    pyToSerWriteListener = Thread(target=serDuplexWrite, args=(ardCon,))
    serReadToPyListener = Thread(target=serDuplexRead, args=(ardCon,))
    # still testing
    print("waiting 5")
    time.sleep(5)
    print("starting the threads")
    ardStateReqListener.start()
    if(ardCon != None):
        pyToSerWriteListener.start()
        serReadToPyListener.start()


if __name__ == '__main__':
    main()
