import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []

def broadcast(message):
    dead = []
    for conn, _ in clients:
        try:
            conn.sendall((message + "\n").encode())
        except:
            dead.append((conn, _))

    for d in dead:
        clients.remove(d)


def handle_client(conn, addr):
    try:

        name = conn.recv(1024).decode().strip()
        clients.append((conn, name))

        print(f"{name} connected from {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            broadcast(f"{name} pressed Enter")
    except:
        pass
    finally:
        for c in clients:
            if c[0] is conn:
                clients.remove(c)
        conn.close()
        print(f"Client disconnected: {addr}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
