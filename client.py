import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def listen_for_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode().strip())


# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Send your name once at login
name = input("Enter your name: ").strip()
sock.sendall((name + "\n").encode())

# Start thread to receive broadcast messages
threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

print("Press Enter to notify the server...")

# Main loop: press Enter → send message
while True:
    input()
    sock.sendall(b"ENTER\n")
