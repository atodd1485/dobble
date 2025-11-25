import socket
import threading

class Client:

    HOST = "127.0.0.1"
    PORT = 5000

    def __init__(self,name):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.rx_messages = list()
        self.name = name
        threading.Thread(target=self.listen_for_messages, args=(self.sock,), daemon=True).start()

        self.send_message("HELLO",'')
    def listen_for_messages(self,sock):
        while True:
            data = sock.recv(1024)
            if not data:
                break
            self.rx_messages.append(data.decode().strip())

    def send_message(self,tag,message_content):
        full_message = self.name + '|' + tag + '|' + message_content
        self.sock.sendall(full_message.encode())


if __name__ == '__main__':
    name = input("Enter name")
    client = Client(name)
    while True:
        message = input("Enter a message")
        client.send_message('MSG', message)