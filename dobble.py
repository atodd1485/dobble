from modes import SimpleTwoPlayer, FullTwoPlayer, SimpleOnline
from config import Config

GAME_MODE_DICT = {1:SimpleTwoPlayer,2:FullTwoPlayer,3:SimpleOnline}

if __name__ == '__main__':
    config = Config()

    mode = GAME_MODE_DICT[config.game_mode]
    game = mode(config)
    game.play()