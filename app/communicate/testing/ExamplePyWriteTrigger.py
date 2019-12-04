from multiprocessing.connection import Client
import time
message = 'JCof4yui0981sjxRlKmZzSOufNdGBIcsFCNOnzJMi3QxJiMJKHqqjqwX0i7nR5YZvByPuahJ2X2noAt2gH2U2Y7ra6Sj9AJfobvsuENKsTfot5QUYrfQnLmWacjep3vk1a7ioanIazXUxRdUI0O8yTQfSvKgZt5Cjx4WBomOdHHHx5QZqCMCyuvODg3IhwCGpJO0CwyZ1GfDwzSPGHQTE7engZKfvsU2t7EOOgcQwpB41KXkX8UufUWTK3iU5FvfI3vatS4bU32EJth4QpjsfiNizLeiKNeSiE4azTrvkC8blq0QUiGwGxqfBz86Hv3BYQlFwV5AIHWhkl2011PDeK3QaoQBYSCQ4MN92TU3JhFJoFSTYJ9kWZXVGmpworlv1LuX34ZERS8vIzMBIBUPXOMUAQ4xDqn7FoMYxLLXKKG7xYwPrzzc9lSwX59FGejHMmqX4m5QXVxNEHDiGBgYjsHh03MMrn2cwS6FHR9KHWSEXuabWoPx1DIIepdepq6l'


def send():
    address = ('localhost', 6200)
    conn = Client(address, authkey=b'PyToPyCom')
    conn.send(message)
    conn.close()


def main():
    for i in range(1, 20):
        print("send {}.message".format(i))
        send()
        time.sleep(1)


if __name__ == '__main__':
    main()
