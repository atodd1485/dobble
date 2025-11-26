from message import RxMessage, TxMessage
import threading, socket

class NetworkInterface:

    HOST = "127.0.0.1"
    PORT = 5000

    def __init__(self,name):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.sock.settimeout(0.1)
        self.rx_messages = list()
        self.name = name
        self.new_message_ready = False
        threading.Thread(target=self.network_loop, args=(self.sock,), daemon=True).start()
    
    def network_loop(self,sock):
        while True:
            if self.new_message_ready:
                self.send_message()
                self.new_message_ready = False
            try:
                data = sock.recv(1024)
                if not data:
                    continue
                self.rx_messages.append(RxMessage(data))
                print(f"RX:{data.decode().strip()}")
            except socket.timeout:
                pass  
    def queue_message(self,tag,message_content):
        self.new_message = TxMessage(self.name,tag,message_content)
        self.new_message_ready = True

    def send_message(self):
        print(f"Sending message {self.new_message.content}")
        self.sock.sendall(self.new_message.encoded_message)

    def get_new_messages(self):
        new_messages = self.rx_messages.copy()
        self.rx_messages.clear()
        for message in new_messages:
            yield message