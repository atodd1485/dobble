from game import Game
from event_handler import EventHandlerKey, EventHandlerNetwork
from network_interface import NetworkInterface
from message import TxMessage
import numpy as np
import pygame

class SimpleTwoPlayer(Game):

    DEBOUNCE_TIME = 0.2

    def load_card_position(self):
        self.num_cards = 2
        self.card_positions = ( np.array( (self.width//4, self.height//2), dtype=float ),
                                np.array( (3 * self.width//4, self.height//2), dtype=float) )
        self.card_radii = ( int( (self.width / 4) * 0.9 ), int( (self.width / 4) * 0.9 ))

    def higlight_matching_images(self):

        match = {img.key for img in self.cards[0].images} & \
                {img.key for img in self.cards[1].images}

        for el in match:
            self.cards[0].higlight_image(el,highlight_colour=(0,0,0))
            self.cards[1].higlight_image(el,highlight_colour=(0,0,0))

        self.cards_highlighted = True

    def event_player_1_score(self):
        
        if not self.cards_highlighted:
            self.player1.score += 1
        self.generate_cards()
        

    def event_player_2_score(self):

        if not self.cards_highlighted:
            self.player2.score += 1
        self.generate_cards()

    def event_reset_scores(self):

        self.player1.score = 0
        self.player2.score = 0

    def event_higlight_images(self):
        if not self.cards_highlighted:
            self.higlight_matching_images()
        else:
            self.generate_cards()

    def load_events(self):
        self.event_handlers +=  [ EventHandlerKey(self.event_player_1_score,  self.DEBOUNCE_TIME, pygame.MOUSEBUTTONDOWN),
                                  EventHandlerKey(self.event_player_2_score,  self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_LCTRL),
                                  EventHandlerKey(self.event_reset_scores,    self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_RCTRL),
                                  EventHandlerKey(self.event_higlight_images, self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_SPACE) ]

class FullTwoPlayer(Game):

    DEBOUNCE_TIME = 0.2
    MULTIPLAYER = True
    def load_card_position(self):

        self.num_cards = 3
        self.card_positions = ( np.array( (self.width//2, self.height//4), dtype=float ),
                                np.array( (3 * self.width//16, self.height//2), dtype=float ),
                                np.array( (13 * self.width//16, self.height//2), dtype=float ) )
        self.card_radii = ( int( (self.width / 8) * 1.3 ),
                           int( (self.width / 8) * 1.3 ),
                           int( (self.width / 8) * 1.3 ))

    def higlight_matching_images(self):

        match1 = {img.key for img in self.cards[0].images} & \
                 {img.key for img in self.cards[1].images}
        match2 = {img.key for img in self.cards[0].images} & \
                 {img.key for img in self.cards[2].images}

        double_match = match1 == match2

        for el in match1:
            self.cards[1].higlight_image(el,self.player1.colour_rgb)
            if not double_match:
                self.cards[0].higlight_image(el,self.player1.colour_rgb)
            else:
                self.cards[0].higlight_image(el,(0,0,0))

        for el in match2:
            self.cards[2].higlight_image(el,self.player2.colour_rgb)
            if not double_match:
                self.cards[0].higlight_image(el,self.player2.colour_rgb)

        self.cards_highlighted = True

    def event_player_1_score(self):
        if not self.cards_highlighted:
            self.player1.score += 1
        self.generate_cards()

    def event_player_2_score(self):

        if not self.cards_highlighted:
            self.player2.score += 1
        self.generate_cards()

    def event_reset_scores(self):

        self.player1.score = 0
        self.player2.score = 0

    def event_higlight_images(self):
        if not self.cards_highlighted:
            self.higlight_matching_images()
        else:
            self.generate_cards()

    def load_events(self):
        self.event_handlers +=  [ EventHandlerKey(self.event_player_1_score,  self.DEBOUNCE_TIME, pygame.MOUSEBUTTONDOWN),
                                  EventHandlerKey(self.event_player_2_score,  self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_LCTRL),
                                  EventHandlerKey(self.event_reset_scores,    self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_RCTRL),
                                  EventHandlerKey(self.event_higlight_images, self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_SPACE) ]

class SimpleOnline(Game):

    DEBOUNCE_TIME = 0.2
    NETWORK_RATE_LIMIT = 0.2
    def __init__(self,config):
        super().__init__(config)
        self.online = True
        self.network_interface = NetworkInterface(self.player1.name)
        self.network_interface.queue_message('HELLO','')

    def load_card_position(self):
        self.num_cards = 2
        self.card_positions = ( np.array( (self.width//4, self.height//2), dtype=float ),
                                np.array( (3 * self.width//4, self.height//2), dtype=float) )
        self.card_radii = ( int( (self.width / 4) * 0.9 ), int( (self.width / 4) * 0.9 ))

    def higlight_matching_images(self):

        match = {img.key for img in self.cards[0].images} & \
                {img.key for img in self.cards[1].images}

        for el in match:
            self.cards[0].higlight_image(el,highlight_colour=(0,0,0))
            self.cards[1].higlight_image(el,highlight_colour=(0,0,0))

        self.cards_highlighted = True

    def event_player_score(self):
        
        if not self.cards_highlighted:
            self.player1.score += 1
            self.network_interface.queue_message('MSG_ALL','score')
        self.generate_cards()

    def event_other_player_score(self):

        if not self.cards_highlighted:
            self.player2.score += 1
        self.generate_cards()

    def event_reset_scores(self):

        self.player1.score = 0
        self.player2.score = 0
        self.network_interface.queue_message('MSG_ALL','reset')

    def event_higlight_images(self):
        if not self.cards_highlighted:
            self.higlight_matching_images()
        else:
            self.generate_cards()

    def load_events(self):
        self.event_handlers +=  [ EventHandlerKey(self.event_player_score,     self.DEBOUNCE_TIME, pygame.MOUSEBUTTONDOWN),
                                  EventHandlerKey(self.event_reset_scores,    self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_RCTRL),
                                  EventHandlerKey(self.event_higlight_images, self.DEBOUNCE_TIME, pygame.KEYDOWN, event_key=pygame.K_SPACE),

                                  EventHandlerNetwork(self.event_other_player_score, self.NETWORK_RATE_LIMIT, TxMessage(self.player2.name,'MSG_ALL','score')),
                                  EventHandlerNetwork(self.event_reset_scores,       self.NETWORK_RATE_LIMIT, TxMessage(self.player2.name,'MSG_ALL','reset')) ]