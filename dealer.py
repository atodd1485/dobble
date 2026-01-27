import random

CARDS_FILE = 'cards.txt'

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