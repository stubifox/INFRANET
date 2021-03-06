"""
 * @author Kai Fischer
 * @email kathunfischer@googlemail.com
 * @desc Script to mockup the backend function to deliver actual connection information. Closes after 20 requests.
"""
from multiprocessing.connection import Listener

print("starting")

for i in range(1, 20):
    print("listen on port 6000")
    address = ('localhost', 6000)
    listener = Listener(address, authkey=b'PyToPyCom')
    con = listener.accept()
    print('connection accepted from {}'.format(listener.last_accepted))
    while True:
        msg = con.recv()
        if msg == 'ArdConState':  # connection state
            con.send('True')
        elif msg == 'CommunicationState':  # communication state
            con.send('False')
        elif msg == 'PartnerID':
            con.send('lkjs09fu209flasjdlfj')
        else:
            con.close()
            break
        # con.close()
        # break
    print("connection closed")
    listener.close()
