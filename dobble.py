from cards import Card, CardDealer
from player import Player
import pygame, sys, time
import numpy as np

WIDTH = 1200
HEIGHT = 800

class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Dobble")
        self.width,self.height = WIDTH,HEIGHT
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()

        self.small_font = pygame.font.SysFont("Arial", int((50) * (self.width/1200)))
        self.large_font = pygame.font.SysFont("Arial", int((120) * (self.width/1200)))

        self.dealer = CardDealer()

        self.last_click = 0
        self.last_key = 0
        self.last_update_cards = 0

        self.cards_highlighted = False

        self.mode = 0
        self.cards = list()
        self.num_cards = 0

        self.player_entry()
        self.generate_cards()
        self.generate_scores()

    def generate_player(self,player_input,player_index):
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
        if self.mode == 0:
            self.num_cards = 2
            card_positions = ( np.array( (self.width//4, self.height//2), dtype=float ),
                               np.array( (3 * self.width//4, self.height//2), dtype=float) )
            card_radii = ( int( (self.width / 4) * 0.9 ), int( (self.width / 4) * 0.9 ))

        elif self.mode == 1:
            self.num_cards = 3
            card_positions = ( np.array( (self.width//2, self.height//2), dtype=float ),
                               np.array( (3 * self.width//4, self.height//2), dtype=float ),
                               np.array( (3 * self.width//4, self.height//2), dtype=float ) )
            card_radii = ( int( (self.width / 8) * 1.8 ),
                           int( (self.width / 8) * 1.8 ),
                           int( (self.width / 8) * 1.8 ))

        for position,radius in zip(card_positions,card_radii):
            new_card = Card(position,radius,self.dealer)
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
        print(score_height)
        self.left_score_pos = (self.width//4,score_height)
        self.right_score_pos = (self.width - self.width//4,score_height)

        name_height = int(3*self.height/4 + (self.width / 8) * 0.9 )
        left_name_pos = (self.width//4,name_height)
        right_name_pos = (self.width - self.width//4,name_height)

        self.left_name = self.small_font.render(self.player1.name, True, self.player1.colour_rgb)
        self.right_name = self.small_font.render(self.player2.name, True, self.player2.colour_rgb)
        self.left_name_rect = self.left_name.get_rect(center=left_name_pos)
        self.right_name_rect = self.right_name.get_rect(center=right_name_pos)

    def draw_scores(self):
        left_score = self.large_font.render(str(self.player1.score), True, self.player1.colour_rgb)
        right_score = self.large_font.render(str(self.player2.score), True, self.player2.colour_rgb)

        left_score_rect = left_score.get_rect(center=self.left_score_pos)
        right_score_rect = right_score.get_rect(center=self.right_score_pos)

        self.screen.blit(left_score, left_score_rect)
        self.screen.blit(right_score, right_score_rect)
        self.screen.blit(self.left_name, self.left_name_rect)
        self.screen.blit(self.right_name, self.right_name_rect)

    def higlight_matching_images(self):

        if self.mode == 0:
            match = {img.key for img in self.cards[0].images} & \
                    {img.key for img in self.cards[1].images}
            for el in match:
                self.cards[0].higlight_image(el)
                self.cards[1].higlight_image(el)

            self.cards_highlighted = True

    def play(self):

        while True:
            now = time.time()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit_game()

                elif e.type == pygame.MOUSEBUTTONDOWN and (now - self.last_click) > 0.2:
                    if not self.cards_highlighted:
                        self.player1.score += 1
                    self.generate_cards()
                    self.last_click = now

                elif e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL and (now - self.last_key) > 0.2:
                    if not self.cards_highlighted:
                        self.player2.score += 1
                    self.generate_cards()
                    self.last_key = now

                elif e.type == pygame.KEYDOWN and e.key == pygame.K_RCTRL:
                    self.player1.score = 0
                    self.player2.score = 0

                elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    if not self.cards_highlighted:
                        self.higlight_matching_images()
                    else:
                        self.generate_cards()

            if (now - self.last_update_cards) > 0.005:
                self.update_cards()
                self.last_update_cards = now

            self.screen.fill((240, 240, 240))
            self.draw_cards()
            self.draw_scores()

            pygame.display.flip()
            self.clock.tick(60)

    def player_entry(self):

        player_input = ""
        player_index = 0

        while player_index < 2:
            for e in pygame.event.get():

                if e.type == pygame.QUIT:
                    self.quit_game()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if not self.generate_player(player_input,player_index): continue
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

            input_text = self.small_font.render(player_input, True, (255, 0, 0))
            self.screen.blit(input_text, (self.width/2,self.height/2))

            pygame.display.flip()
            self.clock.tick(60)

    def quit_game(self):
        print("Exiting...")
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.play()