from multiprocessing.connection import Client
import time
message = 'CommunicationState'


def send():
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'PyToPyCom')
    conn.send(message)
    print(conn.recv())
    conn.close()


def main():
    for i in range(1, 20):
        print("send {}.message".format(i))
        send()
        time.sleep(1)


if __name__ == '__main__':
    main()
