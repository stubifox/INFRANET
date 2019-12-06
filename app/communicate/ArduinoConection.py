import serial
import time
import serial.tools.list_ports
from threading import Thread
from app.communicate.encryptionHandler import EncryptionHandler
from app.communicate.helperClasses import DataBaseUtilities

# capsulates the communication to the Arduino using a Serial Com-Port connection


class ArduinoConection:

    def write(self, msg):
        try:
            self.__serCon.write(msg)
        except serial.SerialTimeoutException:
            # TODO reset arduino connection
            self.__serCon = None
        except:
            # TODO logging
            print("unknown error")

    def readline(self):
        msg = ""
        try:
            msg = self.__serCon.readline()
        except serial.SerialTimeoutException:
            # TODO reset arduino connection
            self.__serCon = None
        except:
            # TODO Logging
            print("unknown error")
        return msg

    # returns wether a arduino ist connected to the host or not
    def getArdConState(self):
        # if no connection or error in connection
        if ((self.__serCon == None)):
            # try to get a new connection
            if (self.SearchArdThread.is_alive() == False):
                self.SearchArdThread = Thread(
                    target=self.__getSerCon(), args=(self,))
                self.SearchArdThread.start()
            return False
        else:
            return True

    def handleIncomingMessage(self, incomingByteArray):
        encryptionHandler = EncryptionHandler()
        decryptedMessage = encryptionHandler.decryptByteArray(incomingByteArray)
        DataBaseUtilities.insertMessageAndSender(self.__partnerId, decryptedMessage)

    # returns wether another Arduino to Communicate with was found or not
    def getArdComState(self):
        # TODO More logic if needed
        return self.__conToArd

    def __startComListener(self):
        # TODO Implement the listener if the arduino finds a com partner
        raise NotImplementedError

    # searches all local ports for connected arduinos then checks if the respond correctly
    # returns the SerialConnection to the first correct responding arduino
    def __getSerCon(self):
        self.__serCon = None
        AllPorts = list(serial.tools.list_ports.comports())
        for port in AllPorts:
            # if not a arduino, no testing required
            if(str(port).__contains__("Arduino") == False):
                continue
            # also tests if correct software on arduino
            try:
                # Handshake Process
                testCon = serial.Serial(
                    port=port.device, baudrate=115200, timeout=2, write_timeout=2)
                # on each new connection the arduino will restart, waiting for it
                time.sleep(2)
                testCon.write(str.encode("~echo~\n"))
                answer = testCon.readline()
                if (answer == str.encode("~ping~\n")):
                    # searching successfull
                    # set guid
                    # wait for response -> check if guid was correctly recieved
                    testCon.write(str.encode(str(self.__localId) + "\n"))
                    answer = testCon.readline()
                    if (answer != str.encode("~okay~\n")):
                        # TODO log handshake failed
                        print("handshake failed")
                        self.__serCon = None
                        continue
                    else:
                        # handshake successfull
                        self.__serCon = testCon
                        break
            except:
                # TODO Log Fail
                print("error connecting to serialport: {}".format(port.device))
        # return FoundConnection

    def __init__(self, localId):
        self.__localId = localId
        self.__partnerId = None
        self.__serCon = None
        self.SearchArdThread = Thread()
        self.getArdConState()
        if (self.getArdConState()):
            self.__startComListener()
        self.__conToArd = False
