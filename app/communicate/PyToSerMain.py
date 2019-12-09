from ArduinoConection import ArduinoConection
import serial
from threading import Thread
import multiprocessing.connection
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from encryptionHandler import EncryptionHandler
from helperClasses import DataBaseUtilities
import time

# thread function: Listener on Serial, write to DB


def serDuplexRead(ardCon):
    while(True):
        if ardCon.getArdConState() == False :
            continue
        try:
            readInput = ardCon.readline()
            # filter
            if readInput in (b'', b'\n', b' '):
                continue
            print("readInput after filter:", readInput)
            __handleIncomingMessage(ardCon, readInput)
            # TODO write to DB instead of console
            #address = ('localhost', 6300)
            #con = Client(address, authkey=b'PyToPyCom')
            #con.send(readInput)
            #con.close()
            DataBaseUtilities.insertMessageAndSender("mockup", readInput.decode())
        except serial.SerialTimeoutException:
            # TODO reset arduino connection
            ardCon.resetArdCon()
            continue
        except ConnectionRefusedError:
            print("Cannot connect to localhost:6300")

# thread function: Listener to write recieved message on serial connection


def serDuplexWrite(ardCon):
    # TODO use encryption here
    # TODO return error Msg to FE to tell user message could not be send
    print("start listening for MsgConrequests")
    while(True):
        address = ('localhost', 6200)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        while True:
            msg = con.recv()
            print("Sending this msg now:", msg)
            try:
                encryptedMessage = __encryptOutgoingMessage(msg)
                print("encrpytedMessage:", encryptedMessage)
                ardCon.write(encryptedMessage) 
                con.close()
                listener.close()
                break
            except:
                con.close()
                listener.close()
                return
            # con.close()
            # break
    listener.close()
    print("connection closed")

# thread function: Listener for Arduino State requests


def waitForArdStateReq(ardCon):
    print("start listening for ardConrequests")
    while(True):
        #print("listen on port 6000")
        address = ('localhost', 6000)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        #print('connection accepted from {}'.format(listener.last_accepted))
        while True:
            msg = con.recv()
            if msg == 'ArdConState':  # connection state
                con.send(str(ardCon.getArdConState()))
            elif msg == 'CommunicationState':  # communication state
                con.send(str(ardCon.getArdComState()))
            elif msg == 'PartnerID':
                con.send('mockup')
            else:
                con.close()
                listener.close()
                break
            # con.close()
            # break
    print("connection closed")
    listener.close()

def __handleIncomingMessage(ardCon, incomingByteArray):
    encryptionHandler = EncryptionHandler()
    decryptedMessage = encryptionHandler.decryptByteArray(incomingByteArray)
    if decryptedMessage != None:
        print("Decrpyted Message:", decryptedMessage)
        print("partnerId", ardCon.partnerId)
        DataBaseUtilities.insertMessageAndSender("mockup", decryptedMessage)

def __encryptOutgoingMessage(outgoingString):
    encryptionHandler = EncryptionHandler()
    return encryptionHandler.encryptString(outgoingString)

def main():
    # TODO read this identifier from the STDIn to get the information >> Max in following
    ardCon = ArduinoConection()#936DA01F-9ABD-4D9D-80C7-02AF85C822A8
    ardStateReqListener = Thread(target=waitForArdStateReq, args=(ardCon,))
    pyToSerWriteListener = Thread(target=serDuplexWrite, args=(ardCon,))
    serReadToPyListener = Thread(target=serDuplexRead, args=(ardCon,))
    # still testing
    print("waiting 5")
    time.sleep(5)
    print("starting the threads")
    ardStateReqListener.start()
    if(ardCon.IsSerCon()):
        print("not none lol")
        pyToSerWriteListener.start()
        serReadToPyListener.start()


if __name__ == '__main__':
    main()
