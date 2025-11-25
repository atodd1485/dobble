import socket
import threading

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

        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()


    def broadcast(self,message):
        dead = []
        for client in self.clients:
            try:
                client.conn.sendall((message + "\n").encode())
            except:
                dead.append(client)

        for d in dead:
            self.clients.remove(d)

    def handle_client(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                decoded_message = data.decode().strip()

                parts = decoded_message.split("|")
                if len(parts) != 3:
                    print(f"Invalid message from {addr}: {decoded_message}")
                    continue

                name, tag, message_content = parts

                if tag == 'HELLO':
                    self.clients.append(Client(conn, name))
                    print(f"{name} connected from {addr}")

                elif tag == 'MSG':
                    self.broadcast(f"{name} says {message_content}")

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