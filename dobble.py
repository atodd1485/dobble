from modes import SimpleTwoPlayer, FullTwoPlayer
from config import Config

if __name__ == '__main__':
    config = Config()
    #game = SimpleTwoPlayer(config)
    game = FullTwoPlayer(config)
    game.play()