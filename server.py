from message import RxMessage, TxMessage
import socket, threading

class Client:
    def __init__(self,name,conn):
        self.name = name
        self.conn = conn
        self.connected = True

class Server:
    HOST = "0.0.0.0"
    PORT = 5000

    def __init__(self):

        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        self.socket.settimeout(1.0)
        self.shutdown = False
        while not self.shutdown:
            try:
                conn, addr = self.socket.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
    
    def send_message(self,client,message):
        if client.connected:
            client.conn.sendall(message.encoded_message)
    
    def broadcast(self,message):
        dead = []
        for client in self.clients:
            if client.connected:
                print("sending to {client.name}")
                client.conn.sendall(message.encoded_message)

    def handle_client(self, conn, addr):
        this_client = None
        while not self.shutdown:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                rx_message = RxMessage(data)

                if rx_message.tag == 'HELLO':
                    this_client = Client(rx_message.name,conn)
                    self.clients.append(this_client)
                    self.broadcast(TxMessage('server','MSG',f"Hello {rx_message.name}, I'm server"))

                elif rx_message.tag == 'MSG_SERVER':
                    self.send_message(this_client,TxMessage('server','MSG',f'{rx_message.name} said {rx_message.content} to the server'))
                    if rx_message.content == 'shutdown':
                        print("{name} requested shutdown")
                        self.shutdown = True
                elif rx_message.tag == 'MSG_ALL':
                    self.broadcast(TxMessage('server','MSG',f'{rx_message.name} said {rx_message.content} to everyone'))
                    if rx_message.content == 'score':
                        self.broadcast(rx_message.convert())
                if rx_message.content == 'shutdown':
                    print("{name} requested shutdown")
                    self.shutdown = True
            except Exception as e:
                print(f"Error with client {addr}: {e}")
                break

        for c in list(self.clients):
            if c.conn is conn:
                self.clients.remove(c)

        conn.close()
        print(f"Client disconnected: {addr}")

    print(f"Server listening on {HOST}:{PORT}")


if __name__ == '__main__':
    server = Server()