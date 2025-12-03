import socket, threading, random

from message import MessageHandler, Message
from config import Config

def network_id_input(prompt,blacklisted_ids=None):
    if blacklisted_ids is not None:
        blacklisted_ids = [0] + [_id for _id in blacklisted_ids]
    else:
        blacklisted_ids = [0]
    while True:
        id_input = input(prompt)
        try:
            network_id = int(id_input)
        except ValueError:
            print("Enter an integer")
            continue
        if network_id in blacklisted_ids:
            print("You cannot have that id")
            continue
        break
    return network_id

class Client:

    def __init__(self, name, host, port):

        self.name = name
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.rx_messages = list()
        self.network_id = None
        self.message_handler = MessageHandler()
        threading.Thread(target=self.listen_for_messages, args=(self.sock,), daemon=True).start()

        self.seed = random.randrange(0,2000)
        self.send_hello()

    def send_hello(self):
        hello_message = Message(101,0,'HELLO',f'{self.seed}:{self.name}')
        self.send_message(hello_message)

    def listen_for_messages(self,sock):
        while True:
            data = sock.recv(1024)
            if not data:
                break
            decoded_message = self.message_handler.get_decoded_message(data)

            if decoded_message.receiver_id == self.network_id or decoded_message.receiver_id == 99 or decoded_message.receiver_id == 101:
                self.rx_messages.append(decoded_message)
                print(decoded_message)
                if decoded_message.tag == 'HELLO':
                    seed,network_id = decoded_message.content.split(':')
                    if int(seed) == self.seed:
                        self.network_id = int(network_id)
                        print(f"Assinged network_id {self.network_id}")

    def send_message(self,message):
        encoded_message = self.message_handler.get_encoded_message(message)
        self.sock.sendall(encoded_message)

if __name__ == '__main__':

    config = Config()
    host =  '127.0.0.1' if config.host == 'local' else config.host
    name = input("Enter name")
    client = Client(name)
    while True:
        if client.network_id is None:
            continue
        message_content = input("Enter a message")
        receiver_id = network_id_input('Enter receiver network id')
        message = Message(client.network_id,receiver_id,'MSG',message_content)
        print(message)
        client.send_message(message)