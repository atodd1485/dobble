from message import Message, MessageHandler
from player import Player
from server import UNKNOWN_CLIENT_ID,BROADCAST_ID,SERVER_ID
import threading, socket, random, time

class NetworkInterface:

    TX_RATE_LIMIT = 0.1
    UNKNOWN_CLIENT_ID = UNKNOWN_CLIENT_ID
    SERVER_ID = SERVER_ID
    BROADCAST_ID = BROADCAST_ID
    def __init__(self, player, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(0.1)
        self.rx_messages = list()

        self.network_id = self.UNKNOWN_CLIENT_ID
        self.opponent_data = None
        self.deal_data = None

        self.tx_buffer = list()
        self.last_tx_time = 0
        self.message_handler = MessageHandler()
        self.waiting_for_dealer = False
        threading.Thread(target=self.network_loop, args=(self.sock,), daemon=True).start()

        self.seed = random.randrange(0,2000)
        self.queue_message(self.SERVER_ID, 'HELLO', f'{self.seed},{player.name},{player.colour}')


    def network_loop(self,sock):
        while True:
            now = time.time()
            if len(self.tx_buffer) != 0:
                if (now - self.last_tx_time > self.TX_RATE_LIMIT ):
                    self.send_message()

            try:
                data = sock.recv(1024)
                if not data:
                    continue
                decoded_message = self.message_handler.get_decoded_message(data)

                # network_id assignment message
                if decoded_message.receiver_id == self.UNKNOWN_CLIENT_ID and decoded_message.tag == 'HELLO':
                    seed,network_id = decoded_message.content.split(',')
                    if int(seed) == self.seed:
                        self.network_id = int(network_id)
                    continue

                # ignore message meant for others
                if decoded_message.receiver_id != self.network_id and decoded_message.receiver_id != self.BROADCAST_ID:
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

    def get_online_opponent_and_seed(self,player1):

        player_ids_established = self.network_id != self.UNKNOWN_CLIENT_ID and self.opponent_data is not None

        if not player_ids_established:
            return None, None

        player1.network_id = self.network_id

        opponent_network_id, opponent_name, opponent_colour, rng_seed = self.opponent_data.split(',')

        opponent = Player(opponent_name,opponent_colour)
        opponent.network_id = int(opponent_network_id)

        print(f'Player {opponent.name} joined')

        rng_seed = int(rng_seed)

        return opponent,rng_seed

    def request_cards(self):
        if self.waiting_for_dealer:
            return
        self.waiting_for_dealer = True
        self.queue_message(self.SERVER_ID, 'DEAL', '')
        return None

    def get_cards(self):

        if self.deal_data is None:
            return None

        deal_data = self.deal_data
        self.deal_data = None
        self.waiting_for_dealer = False
        deal_data = [int(el) for el in deal_data.split(',')]
        card1_data,card2_data = deal_data[:len(deal_data)//2], deal_data[len(deal_data)//2:]
        return (card1_data, card2_data)

    def queue_message(self,receiver_id,tag,message_content):

        network_id = self.network_id if self.network_id is not None else self.UNKNOWN_CLIENT_ID
        self.tx_buffer.append( Message(network_id,receiver_id,tag,message_content) )

    def send_message(self):
        encoded_message = self.message_handler.get_encoded_message(self.tx_buffer.pop(0))
        self.sock.sendall(encoded_message)
        self.last_tx_time = time.time()

    def get_new_messages(self):
        new_messages = self.rx_messages.copy()
        self.rx_messages.clear()
        for message in new_messages:
            yield message