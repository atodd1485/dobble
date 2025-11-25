import pygame,random, os
import numpy as np

CARDS_FILE = 'cards.txt'
ICONS_DIR = 'icons'

IMAGES_DICT = dict()
for i,file in enumerate(os.listdir(ICONS_DIR)):
    IMAGES_DICT[i] = ICONS_DIR + '/' + file

class Image:

    BORDER_WIDTH = 5

    def __init__(self,position,image_key,max_size):
        self.key = image_key
        self.img_path = IMAGES_DICT[self.key]
        img = pygame.image.load(self.img_path).convert_alpha()
        size = random.randrange(40,max_size)
        self.img = pygame.transform.smoothscale(img, (size,size))
        self.start_position = position.copy()
        self.position = position
        self.higlight_colour = (255,0,0)
        self.higlighted = False

        self.draw_debug = False

    def draw(self,screen):
        rect = self.img.get_rect(center=self.position)
        screen.blit(self.img,rect)

        if not self.higlighted and not self.draw_debug:
            return
        pygame.draw.rect(screen, self.highlight_colour,
                         rect.inflate(self.BORDER_WIDTH, self.BORDER_WIDTH), self.BORDER_WIDTH)

        if self.draw_debug:
            pygame.draw.circle(screen, self.higlight_colour, self.position, 4)

class CardDealer:
    def __init__(self):
        self.refresh()

    def refresh(self):
        with open(CARDS_FILE,'r') as file:
            raw = [line.strip().split(',') for line in file.readlines()]

        self.card_list = [ [int(el) for el in l] for l in raw]

    def draw(self):
        if len(self.card_list) < 1:
            self.refresh()
        draw =  self.card_list.pop(random.randrange(len(self.card_list)))
        random.shuffle(draw)
        return draw

class Card:

    PHASE_STEP = 0.1
    IMAGE_OSCILLATION_AMPLITUDE = 0.2
    SPEED = 1
    IMAGE_ROTATION_ANG_VELOCITY = 0.5
    IMAGE_BOUNCE_ANG_VELOCITY = 1.5

    def __init__(self,position,radius,dealer,no_movement=False):
        self.position = position
        self.start_position = position.copy()
        self.radius = radius
        self.images = list()
        self.dealer = dealer
        self.no_movement = no_movement
        self.phase = 0

    def fill_with_images(self):

        images = self.dealer.draw()
        num_images = len(images)
        max_image_size = int( self.radius // 2 )

        for i,img_key in enumerate(images):
            position = self.random_sector_position(i,num_images)
            self.images.append(Image(position,img_key, max_image_size))

    def update(self):
        self.phase += 0.1
        if not self.no_movement:
            self.move()
            self.rotate()
            self.bounce()

    def move(self):
        new_position = np.array([ (1 + 0.1*np.sin(self.phase)) * self.start_position[0],
                                  (1 + 0.1*np.sin(2*self.phase)) * self.start_position[1] ])
        for img in self.images:
            img.position  = img.position - self.position + new_position

        self.position = new_position

    def higlight_image(self,image_key,highlight_colour):
        for img in self.images:
            if img.key == image_key:
                img.higlighted = True
                img.highlight_colour = highlight_colour
                break

    def random_sector_position(self,sector_number,total_sectors):

        sector_size = (2 * np.pi) / total_sectors
        u = random.uniform(0.2**2, 0.8**2)
        r = self.radius * (u**0.5)
        theta = random.uniform(sector_number * sector_size,
                               (sector_number + 1) * sector_size)

        return np.array( (self.position[0] + r * np.cos(theta), self.position[1] + r * np.sin(theta)) , dtype=float )

    def rotate(self):
        theta = self.IMAGE_ROTATION_ANG_VELOCITY * self.PHASE_STEP
        rotation_matrix = np.array([ [np.cos(theta), -np.sin(theta)],
                                     [np.sin(theta),  np.cos(theta)] ])
        for img in self.images:
            relative_img_position = img.position - self.position
            relative_img_position_rotated  = rotation_matrix @ relative_img_position
            img.position = relative_img_position_rotated + self.position

    def bounce(self):

        for img in self.images:
            relative_img_start_length = np.linalg.norm( img.start_position - self.start_position )
            relative_img_position = img.position - self.position
            relative_img_position_normalised = relative_img_position / np.linalg.norm(relative_img_position)

            img.position = (1 + self.IMAGE_OSCILLATION_AMPLITUDE *np.sin(self.IMAGE_BOUNCE_ANG_VELOCITY * self.phase)) \
                           * relative_img_start_length * relative_img_position_normalised + self.position

    def draw(self,screen):

        pygame.draw.circle(screen,(200,200,200),self.position,self.radius,10)
        for img in self.images:
            img.draw(screen)
