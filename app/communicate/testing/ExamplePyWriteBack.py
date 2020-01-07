"""
 * @author Kai Fischer
 * @email kathunfischer@googlemail.com
 * @desc Script to mockup entered chat messages, which should get send to the partner computer. Sends 20 messages. Used for stress testing in early states.
"""

from multiprocessing.connection import Client
import time
message = 'PartnerID'


def send():
    address = ('localhost', 6200)
    conn = Client(address, authkey=b'PyToPyCom')
    conn.send("dostuff")
    conn.close()


def main():
    print("starting")
    for i in range(1, 20):
        print("send {}.message".format(i))
        send()
        #Use "time.sleep()" to vary the send messages per second.
        time.sleep(1)


if __name__ == '__main__':
    main()
