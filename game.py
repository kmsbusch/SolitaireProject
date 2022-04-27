import arcade
import random
import pickle

from typing import Optional

from sympy import N
import card
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
        self.game_board = board.Board("klondike")
        self.game_board.setup()
    
    def get_board(self):
        return self.game_board
    
    
    

        
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
