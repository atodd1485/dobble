from message import Message, MessageHandler
from player import Player
import threading, socket, random, time

class NetworkInterface:

    def __init__(self, player, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(0.1)
        self.rx_messages = list()

        self.network_id = 101
        self.opponent_data = None
        self.deal_data = None

        self.new_message_ready = False
        self.message_handler = MessageHandler()
        threading.Thread(target=self.network_loop, args=(self.sock,), daemon=True).start()

        self.seed = random.randrange(0,2000)
        self.queue_message(0, 'HELLO', f'{self.seed},{player.name},{player.colour}')


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
                    seed,network_id = decoded_message.content.split(',')
                    if int(seed) == self.seed:
                        self.network_id = int(network_id)
                    continue

                # ignore message meant for others
                if decoded_message.receiver_id != self.network_id and decoded_message != 99:
                    continue

                # opponent network assignment message
                if decoded_message.tag == 'OPPONENT':
                    self.opponent_data = decoded_message.content
                    continue

                # card deal message
                if decoded_message.tag == 'DEAL':
                    self.deal_data = decoded_message.content
                    continue

                self.rx_messages.append(self.message_handler.get_decoded_message(data))

            except socket.timeout:
                pass

    def get_online_opponent(self,player1):

        player_ids_established = self.network_id != 101 and self.opponent_data is not None
        waiting_message_printed = False

        while not player_ids_established:
            player_ids_established = self.network_id != 101 and self.opponent_data is not None
            if not waiting_message_printed:
                print("Waiting for players to be established on the network")
                waiting_message_printed = True
            else:
                print('.',end='',flush=True)

            time.sleep(0.5)
        print('\n')

        player1.network_id = self.network_id

        opponent_network_id, opponent_name, opponent_colour = self.opponent_data.split(',')

        opponent = Player(opponent_name,opponent_colour)
        opponent.network_id = int(opponent_network_id)

        print(f'Player {opponent.name} joined')

        return opponent

    def get_cards(self):

        received_card = False
        waiting_message_printed = False

        self.queue_message(self,0,'DEAL','')
        while not received_card:

            if not waiting_message_printed:
                print("Waiting for network to deal new cards")
                waiting_message_printed = True
            else:
                print('.',end='',flush=True)

            time.sleep(0.5)
        print('\n')

        cards_data = self.deal_data.split(',')

        opponent = Player(opponent_name,opponent_colour)
        opponent.network_id = int(opponent_network_id)

        print(f'Player {opponent.name} joined')

        return opponent

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