from cards import Card, CardDealer
from player import Player
from event_handler import EventHandlerKey,EventHandlerNetwork

import pygame, sys, time

class Game:
    def __init__(self,config):

        pygame.init()
        pygame.display.set_caption("Dobble")
        self.width,self.height = config.window_width,config.window_height
        self.skip_player_input = config.skip_player_input
        self.no_movement = config.no_movement

        self.online = False

        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()

        self.small_font =  pygame.font.SysFont("Arial", int((30) * (self.width/1200)))
        self.medium_font = pygame.font.SysFont("Arial", int((50) * (self.width/1200)))
        self.large_font =  pygame.font.SysFont("Arial", int((120) * (self.width/1200)))

        self.dealer = CardDealer()

        self.last_click = 0
        self.last_key = 0
        self.last_update_cards = 0

        self.cards_highlighted = False

        self.mode = 0
        self.cards = list()
        self.num_cards = 0

        self.local_player_entry()
        self.generate_cards()
        self.generate_event_handlers()

    def generate_local_player(self,player_input,player_index):
        split_list = player_input.split()
        if len(split_list) != 2:
            print("Provide name and color only")
            return False
        name, colour = split_list
        try:
            if player_index == 0:
                self.player1 = Player(name,colour)
            elif player_index == 1:
                self.player2 = Player(name,colour)

        except KeyError:
            print("Use red green or blue")
            return False

        return True

    def generate_cards(self):
        self.cards_highlighted = False
        self.cards = list()
        self.load_card_position()

        for position,radius in zip(self.card_positions,self.card_radii):
            new_card = Card(position,radius,self.dealer,no_movement=self.no_movement)

            new_card.fill_with_images()
            self.cards.append( new_card )

    def update_cards(self):
        for card in self.cards:
            card.update()

    def draw_cards(self):
        for card in self.cards:
            card.draw(self.screen)

    def generate_scores(self):
        score_height = int(self.height/4 - (self.width / 8) * 0.9 )
        self.left_score_pos = (self.width//4,score_height)
        self.right_score_pos = (self.width - self.width//4,score_height)

        name_height = int(3*self.height/4 + (self.width / 8) * 0.9 )
        left_name_pos = (self.width//4,name_height)
        right_name_pos = (self.width - self.width//4,name_height)

        self.left_name = self.medium_font.render(self.player1.name, True, self.player1.colour_rgb)
        self.right_name = self.medium_font.render(self.player2.name, True, self.player2.colour_rgb)
        self.left_name_rect = self.left_name.get_rect(center=left_name_pos)
        self.right_name_rect = self.right_name.get_rect(center=right_name_pos)

    def generate_event_handlers(self):
        self.event_handlers = list()
        self.event_handlers.append(EventHandlerKey(self.quit_game,0,pygame.QUIT))
        self.load_events()

    def draw_scores(self):
        left_score = self.large_font.render(str(self.player1.score), True, self.player1.colour_rgb)
        right_score = self.large_font.render(str(self.player2.score), True, self.player2.colour_rgb)

        left_score_rect = left_score.get_rect(center=self.left_score_pos)
        right_score_rect = right_score.get_rect(center=self.right_score_pos)

        self.screen.blit(left_score, left_score_rect)
        self.screen.blit(right_score, right_score_rect)
        self.screen.blit(self.left_name, self.left_name_rect)
        self.screen.blit(self.right_name, self.right_name_rect)

    def play(self):
        self.generate_scores()
        while True:
            now = time.time()
            for e in pygame.event.get():
                for event_handler in self.event_handlers:
                    event_handler.check(e,now)
            if self.online:
                for msg in self.network_interface.get_new_messages():
                    print("MESSAGE")
                    for event_handler in self.network_event_handlers:
                        event_handler.check(msg,now)
            if (now - self.last_update_cards) > 0.005:
                self.update_cards()
                self.last_update_cards = now

            self.screen.fill((240, 240, 240))
            self.draw_cards()
            self.draw_scores()

            pygame.display.flip()
            self.clock.tick(60)

    def local_player_entry(self):

        if self.skip_player_input:
            self.generate_local_player('Player_1 red',0)
            self.generate_local_player('Player_2 blue',1)
            return

        player_input = ""
        player_index = 0

        while player_index < self.num_local_players:
            for e in pygame.event.get():

                if e.type == pygame.QUIT:
                    self.quit_game()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if not self.generate_local_player(player_input,player_index): continue
                        player_input = ""
                        player_index += 1

                    elif e.key == pygame.K_BACKSPACE:
                        player_input = player_input[:-1]

                    else:
                        if e.unicode and ord(e.unicode) >= 32:
                            player_input += e.unicode

            self.screen.fill((240, 240, 240))

            heading_text = self.small_font.render(f'Player {player_index+1}, enter your name a space and your favourite color', True, (255, 0, 0))
            self.screen.blit(heading_text, (self.width/16,self.height/4))

            input_text = self.medium_font.render(player_input, True, (255, 0, 0))
            self.screen.blit(input_text, (self.width/2,self.height/2))

            pygame.display.flip()
            self.clock.tick(60)

        self.screen.fill((240, 240, 240))
        heading_text = self.medium_font.render('Waiting for network players...', True, (255, 0, 0))
        self.screen.blit(heading_text, (self.width/16,self.height/4))

        pygame.display.flip()
        self.clock.tick(60)

    def quit_game(self):
        print("Exiting...")
        pygame.quit()
        sys.exit()
