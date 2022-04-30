from typing import Optional
import card_elements
import board
import game

import random
import arcade

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Drag and Drop Cards"


def debugFunc():
        print("hi")


def main():
    """ Main function """
    
    window = game.Game()
    game_board = window.get_board()
    #game_board.setup()
    
    # game_board.create_memento()
    arcade.run()


if __name__ == "__main__":
    main()