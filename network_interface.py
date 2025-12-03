from message import Message, MessageHandler
import threading, socket, random, time

class NetworkInterface:

    def __init__(self,player_name, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(0.1)
        self.rx_messages = list()

        self.network_id = 101
        self.opponent_data = None

        self.new_message_ready = False
        self.message_handler = MessageHandler()
        threading.Thread(target=self.network_loop, args=(self.sock,), daemon=True).start()

        self.seed = random.randrange(0,2000)
        self.queue_message(0, 'HELLO', f'{self.seed}:{player_name}')


    def network_loop(self,sock):
        while True:
            if self.new_message_ready:
                self.send_message()
                self.new_message_ready = False
            try:
                data = sock.recv(1024)
                if not data:
                    continue
                decoded_message = self.message_handler.get_decoded_message(data)

                # network_id assignment message
                if decoded_message.receiver_id == 101 and decoded_message.tag == 'HELLO':
                    seed,network_id = decoded_message.content.split(':')
                    if int(seed) == self.seed:
                        self.network_id = int(network_id)
                        print(f"Assinged network_id {self.network_id}")
                    continue

                # ignore message meant for others
                if decoded_message.receiver_id != self.network_id and decoded_message != 99:
                    continue

                # opponent network assignment message
                if decoded_message.tag == 'OPPONENT':
                    self.opponent_data = decoded_message.content
                    continue

                self.rx_messages.append(self.message_handler.get_decoded_message(data))

            except socket.timeout:
                pass

    def get_player_network_ids(self,player1,player2):

        player_ids_established = False
        while True:
            player_ids_established = self.network_id != 101 and self.opponent_data is not None
            if player_ids_established:
                break
            print("Waiting for players to be established on the network")
            time.sleep(2)

        player1.network_id = self.network_id

        opponent_network_id, opponent_name = self.opponent_data.split(':')
        player2.network_id = int(opponent_network_id)
        player2.name = opponent_name
        print("PLAYER 2 IS ", player2.name )

    def queue_message(self,receiver_id,tag,message_content):

        network_id = self.network_id if self.network_id is not None else 101
        self.new_message = Message(network_id,receiver_id,tag,message_content)
        self.new_message_ready = True

    def send_message(self):
        encoded_message = self.message_handler.get_encoded_message(self.new_message)
        self.sock.sendall(encoded_message)

    def get_new_messages(self):
        new_messages = self.rx_messages.copy()
        self.rx_messages.clear()
        for message in new_messages:
            yield message