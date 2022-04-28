import arcade
import random
import pickle

from typing import Optional

from sympy import N
import cardsprite
import board

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Drag and Drop Cards"


class Game(arcade.Window):
    """ Main application class. """
    game_board = None

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.game_board = board.Board("klondike")
        self.game_board.setup()
        print(self.game_board)
        
    
    def get_board(self):
        print(self.game_board)
        return self.game_board
    
    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.game_board.pile_mat_list.draw()

        # Draw the cards
        self.game_board.card_list.draw()
    

    

        
"""
Capture and externalize an object's internal state so that the object
can be restored to this state later, without violating encapsulation.
"""

"""
class Originator:
  
    Create a memento containing a snapshot of its current internal
    state.
    Use the memento to restore its internal state.
   

    def __init__(self):
  """       

    


# def main():
#     originator = Originator()
#     memento = originator.create_memento()
#     originator._state = True
#     originator.set_memento(memento)
