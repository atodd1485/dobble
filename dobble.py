from cards import Card, CardDealer
import pygame, sys, time

WIDTH = 1200
HEIGHT = 800
class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Dobble")
        self.font = pygame.font.SysFont("Arial", 150) 
        self.width,self.height = WIDTH,HEIGHT
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.dealer = CardDealer()
        self.generate_cards()
        
        score_height = int(self.height/4 - self.card_radius/2 )
        self.left_score_pos = (self.width//4,score_height)
        self.right_score_pos = (self.width - self.width//4,score_height)

        self.last_click = 0
        self.last_key = 0
        self.left_score = 0
        self.right_score = 0
        
    def generate_cards(self):
        self.card_radius = int( (self.width / 8) * 1.8 ) 
        self.card1 = Card(self.width//4, self.height//2,self.card_radius,self.dealer)
        self.card1.fill_with_images()
        self.card2 = Card(3 * self.width//4, self.height//2,self.card_radius,self.dealer)
        self.card2.fill_with_images()

    def draw_scores(self):
        left_score = self.font.render(str(self.left_score), True, (255, 0, 0))
        right_score = self.font.render(str(self.right_score), True, (255, 0, 0))
        
        left_pos = (self.width//4,int(self.height/4 - self.card_radius/2 ))
        left_score_rect = left_score.get_rect(center=self.left_score_pos)
        right_score_rect = right_score.get_rect(center=self.right_score_pos)
        self.screen.blit(left_score, left_score_rect)
        self.screen.blit(right_score, right_score_rect)

    def run(self):
        while True:
            now = time.time() 
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and (now - self.last_click) > 0.2:
                self.right_score += 1
                self.generate_cards()
                self.last_click = now

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL and (now - self.last_key) > 0.2:
                self.left_score += 1
                self.generate_cards()
                self.last_key = now

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RCTRL:
                self.left_score = 0
                self.right_score = 0
                
            self.screen.fill((240, 240, 240))

            self.card1.draw(self.screen)
            self.card2.draw(self.screen)
            self.draw_scores()
            pygame.display.flip()

            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()