from cards import Card, CardDealer
import pygame, sys, time

class Game:
    def __init__(self):

        pygame.init()
        self.width,self.height = 1200,675
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()

        self.dealer = CardDealer()
        self.generate_cards()

        self.last_click = 0

    def generate_cards(self):
        self.card1 = Card(self.width//4, self.height//2,240,self.dealer)
        self.card1.fill_with_images()
        self.card2 = Card(3 * self.width//4, self.height//2,240,self.dealer)
        self.card2.fill_with_images()

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                now = time.time()
                if now - self.last_click > 0.2:    # 200 ms debounce
                    self.generate_cards()
                    self.last_click = now
            self.screen.fill((240, 240, 240))

            self.card1.draw(self.screen)
            self.card2.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()