import serial
import time
import serial.tools.list_ports
from threading import Thread

# capsulates the communication to the Arduino using a Serial Com-Port connection
class ArduinoConection:

    def write(self,msg):
        print("send message: {}".format(msg))
        try:
            self.__serCon.write(msg)
        except serial.SerialTimeoutException:
            print("arduino not reachable")
            self.__serCon = None
        except:
            print("unkonw error occurd")
        


    def readline(self):
        msg = ""
        try:
            msg = self.__serCon.readline()         
            print("got ser message: {}".format(msg))    
        except serial.SerialTimeoutException:
            print("arduino not reachable")
            self.__serCon = None
        except:
            print("unkonw error occurd")
        return msg  

    # returns wether a arduino ist connected to the host or not
    def getArdConState(self):
        # if no connection or error in connection
        if ((self.__serCon == None)):
            # try to get a new connection 
            if (self.SearchArdThread.is_alive() == False):
                self.SearchArdThread = Thread(target=self.__getSerCon(),args=(self,))
                self.SearchArdThread.start()
            return False
        else:
            return True

    # returns wether another Arduino to Communicate with was found or not
    def getArdComState(self):
        # TODO More logic if needed
        return self.__conToArd

    def __startComListener(self):
        # TODO Implement
        print("not jet implemented")        

    # searches all local ports for connected arduinos then checks if the respond correctly
    # returns the SerialConnection to the first correct responding arduino
    def __getSerCon(self):
        print("start thread")
        self.__serCon = None
        AllPorts = list(serial.tools.list_ports.comports())
        for port in AllPorts:
            # if not a arduino no testing required
            if(str(port).__contains__("Arduino") == False):
                continue
            # also tests if correct software on arduino
            print("tried port{}".format(port.device))    
            try:
                # Handshake Process
                TestCon = serial.Serial(port=port.device,baudrate=115200,timeout=2,write_timeout=2)
                time.sleep(2) # on each new connection the arduino will restart, waiting for it
                TestCon.write(str.encode("~echo~\n"))
                answer = TestCon.readline()
                if (answer == str.encode("~ping~\n")):
                    print("searching successfull")
                    # searching successfull
                    # set guid
                    # wait for response -> check if guid was correctly recieve
                    print("send guid")
                    print(str.encode(str(self.__localId) + "\n"))
                    TestCon.write(str.encode(str(self.__localId) + "\n"))
                    print("wait for answer")
                    answer = TestCon.readline()
                    print("got answer")
                    print(answer)
                    if (answer != str.encode("~okay~\n")):
                        print("Handshake failed")
                        # handshake failed
                        self.__serCon = None
                        continue
                    else:
                        #handshake successfull
                        self.__serCon = TestCon
                        print("Handshake success")
                        break
            except:
                # TODO Log Fail
                print("error connecting to serialport: {}".format(port.device))
        #return FoundConnection

    def __init__(self, localId):
        self.__localId = localId
        self.__serCon = None
        self.SearchArdThread = Thread()
        self.getArdConState()
        if (self.getArdConState()):
            self.__startComListener()
        self.__conToArd = False