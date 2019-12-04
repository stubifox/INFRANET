from multiprocessing.connection import Listener

while True:
    print("listen on port 6000")
    address = ('localhost', 6000)
    listener = Listener(address, authkey=b'PyToPyCom')
    con = listener.accept()
    print('connection accepted from {}'.format(listener.last_accepted))
    msg = con.recv()
    if msg == 'ArdConState':  # connection state
        con.send(str(True))
    elif msg == 'CommunicationState':  # communication state
        con.send(str(False))
    else:
        con.close()
        break
    print("connection closed")
    listener.close()
