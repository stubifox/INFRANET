"""
 * @author Kai Fischer
 * @email kathunfischer@googlemail.com
 * @desc Script to test the backend function to deliver actual connection information. Does 20 requests.
"""

from multiprocessing.connection import Client
import time
message = 'PartnerID'


def send():
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'PyToPyCom')
    conn.send(message)
    print(conn.recv())
    conn.send('ArdConState')
    print(conn.recv())
    conn.send('CommunicationState')
    print(conn.recv())
    conn.send('finstuffwhat')
    conn.close()


def main():
    print("starting")
    for i in range(1, 20):
        print("send {}.message".format(i))
        send()
        #Use "time.sleep()" to vary the connection-state requests per second.
        time.sleep(10)


if __name__ == '__main__':
    main()
