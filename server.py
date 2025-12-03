from message import Message, MessageHandler
from config import Config
import socket, threading

class Client:
    def __init__(self,name,conn):

        self.name = name
        self.network_id = 101
        self.conn = conn
        self.connected = True


class Server:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.clients = {}
        self.pairs = list()
        self.num_clients = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.socket.settimeout(1.0)
        self.shutdown = False
        self.message_handler = MessageHandler()
        self.network_id = 0

        self.next_client_network_id = 1
        while not self.shutdown:
            try:
                conn, addr = self.socket.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue

    def send_message(self,client,tag,content):
        if client.connected:
            message_to_send = Message(self.network_id,client.network_id,tag,content)

            print("----TX----")
            print(message_to_send)
            encoded_message = self.message_handler.get_encoded_message(message_to_send)
            client.conn.sendall(encoded_message)

    def broadcast(self,tag,content):
        for client in self.clients.values():
            self.send_message(tag,content)

    def forward_message(self,message):
        print("Forwarding a message ....")
        receiving_client = self.clients.get(message.receiver_id)
        forwarding_error = None
        if receiving_client is None:
            forwarding_error = f"Error: receiving client {message.receiver_id} unknown"

        elif not receiving_client.connected:
            forwarding_error = "Error: receiving client {message.receiver_id} not connected"

        if forwarding_error is not None:
            print(forwarding_error)
            sending_client = self.clients.get(message.sender_id)
            if sending_client is None:
                print(f"Error: sending client {message.sender_id} unknown")
            else:
                self.send_message(sending_client,'ERROR',forwarding_error)
            return

        encoded_message = self.message_handler.get_encoded_message(message)
        print("----TX----")
        print(message)
        receiving_client.conn.sendall(encoded_message)

    def make_pairing(self):

        client1, client2 = self.clients[self.num_clients-1], self.clients[self.num_clients]
        self.pairs.append( (client1, client2) )
        self.send_message(client1, 'OPPONENT', f'{client2.network_id}:{client2.name}')
        self.send_message(client2, 'OPPONENT', f'{client1.network_id}:{client1.name}')

    def handle_client(self, conn, addr):
        this_client = None
        while not self.shutdown:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                rx_message = self.message_handler.get_decoded_message(data)
                print("----RX----")
                print(rx_message)

                if rx_message.tag == 'HELLO':
                    if rx_message.sender_id == 101:
                        seed,name = rx_message.content.split(':')
                        this_client = Client(name,conn)
                        self.send_message(this_client,'HELLO',f"{seed}:{self.next_client_network_id}")

                        new_network_id = self.next_client_network_id
                        self.next_client_network_id += 1

                        this_client.network_id = new_network_id
                        self.clients[new_network_id] = this_client
                        self.num_clients += 1

                        if self.num_clients % 2 == 0:
                            self.make_pairing()

                    elif this_client is not None:
                        self.send_message(this_client,'MSG',f"Hello {rx_message.sender_id}, I'm server")

                if this_client is None:
                    continue

                if rx_message.tag == 'MSG':
                    if rx_message.receiver_id == self.network_id:
                        self.send_message(this_client,Message(self.network_id,this_client.network_id,'MSG',f'{this_client.network_id} said {rx_message.content} to the server'))
                        if rx_message.content == 'shutdown':
                            print("{name} requested shutdown")
                            self.shutdown = True
                    elif rx_message.receiver_id == 99:
                        self.broadcast(Message(self.network_id,99,'MSG',f'{rx_message.network_id} said {rx_message.content} to everyone'))
                    else:
                        self.forward_message(rx_message)
            except Exception as e:
                print(f"Error with client {addr}: {e}")
                break

        if this_client is not None:
            del self.clients[this_client.network_id]
        conn.close()
        print(f"Client disconnected: {addr}")

if __name__ == '__main__':
    config = Config()
    host = '0.0.0.0' if config.host == 'local' else config.host
    server = Server(host,config.port)