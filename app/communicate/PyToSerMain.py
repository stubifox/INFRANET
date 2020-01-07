"""
 * @author Kai Fischer
 * @coauthor Tim Heinze for the encryption and decryption part
 * @email kathunfischer@googlemail.com
 * @desc The main-backend file, starts other threads, gets started by the frontend.
"""

from ArduinoConection import ArduinoConection
import serial
from threading import Thread
import multiprocessing.connection
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from encryptionHandler import EncryptionHandler
from helperClasses import DataBaseUtilities
import time


def serDuplexRead(ardCon):# thread function: Listener on Serial, write to DB
    while(True):
        if ardCon.getArdConState() == False:
            continue
        try:
            readInput = ardCon.readline()
            # filter unwanted nonsense
            if readInput in (b'', b'\n', b' '):
                continue
            print("readInput after filter:", readInput)
            __handleIncomingMessage(ardCon, readInput)
        except serial.SerialTimeoutException:
            ardCon.resetArdCon()
            continue
        except ConnectionRefusedError:
            print("Cannot connect to localhost:6300")


def serDuplexWrite(ardCon):# thread function: Listener to write recieved message on serial connection
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
    listener.close()
    print("connection closed")




def waitForArdStateReq(ardCon):# thread function: Listener for Arduino State requests
    print("start listening for ardConrequests")
    while(True):
        address = ('localhost', 6000)
        listener = Listener(address, authkey=b'PyToPyCom')
        con = listener.accept()
        while True:
            msg = con.recv()
            if msg == 'ArdConState':  # arduino connected?
                con.send(str(ardCon.getArdConState()))
            elif msg == 'CommunicationState':  # partner found?
                con.send(str(ardCon.getArdComState()))
            elif msg == 'PartnerID':
                con.send('mockup')
            else:
                con.close()
                listener.close()
                break
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
    ardCon = ArduinoConection()  # 936DA01F-9ABD-4D9D-80C7-02AF85C822A8
    ardStateReqListener = Thread(target=waitForArdStateReq, args=(ardCon,))
    pyToSerWriteListener = Thread(target=serDuplexWrite, args=(ardCon,))
    serReadToPyListener = Thread(target=serDuplexRead, args=(ardCon,))
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
