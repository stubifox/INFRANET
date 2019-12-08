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
        time.sleep(1)


if __name__ == '__main__':
    main()
