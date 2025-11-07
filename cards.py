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
        self.position = position
        self.higlighted = False

    def draw(self,screen):
        rect = self.img.get_rect(center=self.position)
        screen.blit(self.img,rect)

        if self.higlighted:
            border_color = (255, 0, 0)
            border_width = 5
            pygame.draw.rect(screen, border_color, rect.inflate(border_width, border_width), border_width)

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
    def __init__(self,x,y,radius,dealer):
        self.x = x
        self.y = y
        self.radius = radius
        self.images = list()
        self.dealer = dealer

    def fill_with_images(self):

        images = self.dealer.draw()
        num_images = len(images)

        for i,img_key in enumerate(images):
            position = self.random_sector_position(i,num_images)
            self.images.append(Image(position,img_key))

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

        return (self.x + r * np.cos(theta), self.y + r * np.sin(theta))

    def draw(self,screen):
        pygame.draw.circle(screen,(200,200,200),(self.x,self.y),self.radius,10)
        for img in self.images:
            img.draw(screen)
