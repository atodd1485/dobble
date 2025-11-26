from modes import SimpleTwoPlayer, FullTwoPlayer, SimpleOnline
from config import Config

if __name__ == '__main__':
    config = Config()
    #game = SimpleTwoPlayer(config)
    #game = FullTwoPlayer(config,multiplayer=True)
    game = SimpleOnline(config)
    game.play()