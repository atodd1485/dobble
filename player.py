COLOUR_DICT = { 'red'  : (255, 0, 0),
                'green': (0, 255, 0),
                'blue' : (0, 0, 255) }
class Player:
    def __init__(self,name,colour):
        self.name = name
        self.score = 0
        self.colour = colour
        self.colour_rgb = COLOUR_DICT.get(colour)

        if self.colour_rgb == None:
            raise KeyError

