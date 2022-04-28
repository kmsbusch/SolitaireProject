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
    
    
    
    
    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.game_board.setup()
            
    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.game_board.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, cardsprite.CardSprite)

            # Figure out what pile the card is in
            pile_index = self.game_board.get_pile_for_card(primary_card)

            ###################################################################################################################### Inside of func needs to be diff or need another one or smth ############################
            # Are we clicking on the bottom deck, to flip three cards?
            if pile_index == board.BOTTOM_FACE_DOWN_PILE:
                # Flip three cards
                for i in range(3):
                    # If we ran out of cards, stop
                    if len(self.game_board.piles[board.BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    # Get top card
                    card = self.game_board.piles[board.BOTTOM_FACE_DOWN_PILE][-1]
                    # Flip face up
                    card.face_up()
                    # Move card position to bottom-right face up pile
                    card.position = self.game_board.pile_mat_list[board.BOTTOM_FACE_UP_PILE].position
                    # Remove card from face down pile
                    self.game_board.piles[board.BOTTOM_FACE_DOWN_PILE].remove(card)
                    # Move card to face up list
                    self.game_board.piles[board.BOTTOM_FACE_UP_PILE].append(card)
                    # Put on top draw-order wise
                    self.game_board.pull_to_top(card)

            elif primary_card.is_face_down: ############################################################## Change this so that cards in middle pile auto flip instead of requiring a click #############
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.game_board.held_cards = [primary_card]
                # Save the position
                self.game_board.held_cards_original_position = [self.game_board.held_cards[0].position]
                # Put on top in drawing order
                self.game_board.pull_to_top(self.game_board.held_cards[0])

                # Is this a stack of cards? If so, grab the other cards too
                card_index = self.game_board.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.game_board.piles[pile_index])):
                    card = self.game_board.piles[pile_index][i]
                    self.game_board.held_cards.append(card)
                    self.game_board.held_cards_original_position.append(card.position)
                    self.game_board.pull_to_top(card)

        else:

            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.game_board.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.game_board.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == board.BOTTOM_FACE_DOWN_PILE and len(self.game_board.piles[board.BOTTOM_FACE_DOWN_PILE]) == 0:
                    # Flip the deck back over so we can restart
                    temp_list = self.game_board.piles[board.BOTTOM_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.game_board.piles[board.BOTTOM_FACE_UP_PILE].remove(card)
                        self.game_board.piles[board.BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.game_board.pile_mat_list[board.BOTTOM_FACE_DOWN_PILE].position
    
    
    
    
    
    
    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.game_board.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.game_board.held_cards[0], self.game_board.pile_mat_list)
        reset_position = True
        pile_index = self.game_board.pile_mat_list.index(pile)

        # See if we are in contact with the closest pile
        if(len(self.game_board.piles[pile_index]) > 0): ############### if there are cards on the pile, the hitbox should be at the bottom of the pile, where players will drop cards
            tmp = self.game_board.piles[pile_index][-1]
        else:
            tmp = pile ########## if nothing is in the pile, the hitbox for card detection is on the pile
        
        if arcade.check_for_collision(self.game_board.held_cards[0], tmp): ######### determine where card hitbox is based on above

            # What pile is it?
            #pile_index = self.game_board.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.game_board.get_pile_for_card(self.game_board.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a middle play pile?
            ##################################################################################### Function to check valid drop needs to be called here as well
            elif board.PLAY_PILE_1 <= pile_index <= board.PLAY_PILE_7:
                
                # Are there already cards there?
                if len(self.game_board.piles[pile_index]) > 0:
                    # Move cards to proper position
                    #top_card is the card at the bottom of the pile we are dropping on
                    top_card = self.game_board.piles[pile_index][-1]
                    #hand_card is the card at the top of the list of cards in our hand
                    hand_card = self.game_board.held_cards[0]
                    print("pilecard_val=", self.game_board.get_intvalue(top_card))
                    print("handcard_val=", self.game_board.get_intvalue(hand_card))
                    isValid = self.game_board.check_valid_klondike_drop(top_card, hand_card)######################
                    if isValid:
                        for i, dropped_card in enumerate(self.game_board.held_cards):
                            dropped_card.position = top_card.center_x, \
                                                    top_card.center_y - board.CARD_VERTICAL_OFFSET * (i + 1)
                        for card in self.game_board.held_cards:
                            # Cards are in the right position, but we need to move them to the right list
                            self.game_board.move_card_to_new_pile(card, pile_index)
                        reset_position = False
                    else:
                        reset_position = True
                else:
                    # Are there no cards in the middle play pile?
                    check_king = self.game_board.get_intvalue(self.game_board.held_cards[0])
                    print("check_king = ", check_king)
                    if(check_king != 13):
                        reset_position = True
                    else:
                        for i, dropped_card in enumerate(self.game_board.held_cards):
                            # Move cards to proper position
                            dropped_card.position = pile.center_x, \
                                                    pile.center_y - board.CARD_VERTICAL_OFFSET * i
                        for card in self.game_board.held_cards:
                            # Cards are in the right position, but we need to move them to the right list
                            self.game_board.move_card_to_new_pile(card, pile_index)
                        reset_position = False

                # for card in self.game_board.held_cards:
                #     # Cards are in the right position, but we need to move them to the right list
                #     self.game_board.move_card_to_new_pile(card, pile_index)

                #Success, don't reset position of cards
                #reset_position = False

            # Release on top play pile? And only one card held?
            elif board.TOP_PILE_1 <= pile_index <= board.TOP_PILE_4 and len(self.game_board.held_cards) == 1: ######################################################### doesnt this if elif elif statement need an else?
                # Move position of card to pile
                
                if len(self.game_board.piles[pile_index]) == 0:
                    # check to make sure first card in top pile is ace
                    checkAce = self.game_board.get_intvalue(self.game_board.held_cards[0])
                    if checkAce != 1: # if not an ace, send card back
                        reset_position = True
                    else:
                        self.game_board.held_cards[0].position = pile.position
                        for card in self.game_board.held_cards:
                            self.game_board.move_card_to_new_pile(card, pile_index)
                        reset_position = False
                else:
                    isValid = self.game_board.check_valid_top_drop(self.game_board.piles[pile_index][-1], self.game_board.held_cards[0])######################
                    if isValid:
                        self.game_board.held_cards[0].position = pile.position
                        # Move card to card list
                        for card in self.game_board.held_cards:
                            self.game_board.move_card_to_new_pile(card, pile_index)
                        reset_position = False
                    else:
                        reset_position = True
        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.game_board.held_cards):
                card.position = self.game_board.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.game_board.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.game_board.held_cards:
            card.center_x += dx
            card.center_y += dy

    

        
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
