import pygame,random, os
import numpy as np

CARDS_FILE = 'cards.txt'
ICONS_DIR = 'icons'

IMAGES_DICT = dict()
for i,file in enumerate(os.listdir(ICONS_DIR)):
    IMAGES_DICT[i] = ICONS_DIR + '/' + file

class Image:
    def __init__(self,position,image_key):
        self.key = image_key
        self.img_path = IMAGES_DICT[self.key]
        img = pygame.image.load(self.img_path).convert_alpha()
        size = random.randrange(40,120)
        self.img = pygame.transform.smoothscale(img, (size,size))
        self.start_position = position
        self.position = position
        self.higlighted = False

        self.draw_debug = False

    def draw(self,screen):
        rect = self.img.get_rect(center=self.position)
        screen.blit(self.img,rect)

        if self.higlighted or self.draw_debug:
            border_color = (255, 0, 0)
            border_width = 5
            pygame.draw.rect(screen, border_color, rect.inflate(border_width, border_width), border_width)
            pygame.draw.circle(screen, border_color, self.position, 4)

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
    def __init__(self,position,radius,dealer):
        self.position = position
        self.start_position = position
        self.radius = radius
        self.images = list()
        self.dealer = dealer
        self.phase = 0

    def fill_with_images(self):

        images = self.dealer.draw()
        num_images = len(images)

        for i,img_key in enumerate(images):
            position = self.random_sector_position(i,num_images)
            self.images.append(Image(position,img_key))

    def update(self):
        self.phase += 0.1
        self.move()
        #self.rotate(1)
        self.bounce()

    def move(self):
        self.position += np.array([1,0])
        for img in self.images:
            img.position = img.position + np.array([1,0])

    def higlight_image(self,image_key):
        for img in self.images:
            if img.key == image_key:
                img.higlighted = True
                break

    def random_sector_position(self,sector_number,total_sectors):

        sector_size = (2 * np.pi) / total_sectors
        u = random.uniform(0.2**2, 0.8**2)
        r = self.radius * (u**0.5)
        theta = random.uniform(sector_number * sector_size,
                               (sector_number + 1) * sector_size)

        return np.array( (self.position[0] + r * np.cos(theta), self.position[1] + r * np.sin(theta)) )

    def rotate(self,angle_degrees):
        theta = angle_degrees * (np.pi/180)
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

            img.position = (1 + 0*np.sin(self.phase)) * relative_img_start_length * relative_img_position_normalised + self.position

    def draw(self,screen):

        pygame.draw.circle(screen,(200,200,200),self.position,self.radius,10)
        for img in self.images:
            img.draw(screen)
