from multiprocessing.connection import Listener
from helperClasses import DataBaseUtilities
import sys

message = 'JCof4yui0981sjxRlKmZzSOufNdGBIcsFCNOnzJMi3QxJiMJKHqqjqwX0i7nR5YZvByPuahJ2X2noAt2gH2U2Y7ra6Sj9AJfobvsuENKsTfot5QUYrfQnLmWacjep3vk1a7ioanIazXUxRdUI0O8yTQfSvKgZt5Cjx4WBomOdHHHx5QZqCMCyuvODg3IhwCGpJO0CwyZ1GfDwzSPGHQTE7engZKfvsU2t7EOOgcQwpB41KXkX8UufUWTK3iU5FvfI3vatS4bU32EJth4QpjsfiNizLeiKNeSiE4azTrvkC8blq0QUiGwGxqfBz86Hv3BYQlFwV5AIHWhkl2011PDeK3QaoQBYSCQ4MN92TU3JhFJoFSTYJ9kWZXVGmpworlv1LuX34ZERS8vIzMBIBUPXOMUAQ4xDqn7FoMYxLLXKKG7xYwPrzzc9lSwX59FGejHMmqX4m5QXVxNEHDiGBgYjsHh03MMrn2cwS6FHR9KHWSEXuabWoPx1DIIepdepq6l\n'

while(True):
    #print("listen on port 6300")
    address = ('localhost', 6300)
    listener = Listener(address, authkey=b'PyToPyCom')
    con = listener.accept()
    msg = con.recv()
    if ((str.encode('\n') == msg) or (str.encode('') == msg)):
        listener.close()
        continue
    sys.stdout.write("-->  {}".format(msg.decode()))
    #DataBaseUtilities.insertMessageAndSender('mockup', msg.decode())

    listener.close()
