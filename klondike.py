"""
Code base referenced from https://api.arcade.academy/en/latest/tutorials/card_game/index.html#
Changes were added from there
"""
from typing import Optional

import random
import arcade

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Drag and Drop Cards"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
################################################################################################################### Might wanna end up making a translator for J, Q, K values to 11,12,13 so card above check works
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


# If we fan out cards stacked on each other, how far apart to fan them?
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Face down image
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

###################################################################################################################### Bottom face up pile isnt a thing in spider ######################################################
# Constants that represent "what pile is what" for the game
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value


        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        arcade.set_background_color(arcade.color.AMAZON)

        ########################################################################################################### Maybe make this list of cards that we are holding into a singleton?
        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats that the cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        ################################################################################################### Here too: Maybe make this list of cards that we are holding into a singleton?
        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats that the cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ to change for diff modes /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
            #pile.position = self.pile_mat_list[i].center_x, \
            #                     self.pile_mat_list[i].center_y - CARD_VERTICAL_OFFSET * (i)
            self.pile_mat_list.append(pile)

        ###################################################################################################################### Needs to change for diff modes ####################################################
        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        ###################################################################################################################### I think this needs to change bc spider has diff number of cards (?) 
        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

        ###################################################################################################################### Difficulty might be able to be tweaked in diff ways here, for klondike solitaire at least 
        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)

        ###################################################################################################################### Needs to change for diff modes ######################################################
        # - Pull from that pile into the middle piles, all face-down
        # Loop for each pile
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            # Deal proper number of cards for that pile
            for j in range(pile_no - PLAY_PILE_1 + 1):
                # Pop the card off the deck we are dealing from
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # Put in the proper pile
                self.piles[pile_no].append(card)
                # Move card to same position as pile we just put it in
                #card.position = self.pile_mat_list[pile_no].position
                card.position = self.pile_mat_list[pile_no].center_x, \
                                self.pile_mat_list[pile_no].center_y - CARD_VERTICAL_OFFSET * (j)
                # Put on top in draw order
                self.pull_to_top(card)
                #top_card = self.piles[pile_no][-1]
                
                                        
                

        ###################################################################################################################### Needs to change for diff modes #####################################################
        # Flip up the top cards
        for i in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            self.piles[i][-1].face_up()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    ###################################################################################################################### Needs to change for diff modes ######################################################
    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(primary_card)

            ###################################################################################################################### Inside of func needs to be diff or need another one or smth ############################
            # Are we clicking on the bottom deck, to flip three cards?
            if pile_index == BOTTOM_FACE_DOWN_PILE:
                # Flip three cards
                for i in range(3):
                    # If we ran out of cards, stop
                    if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    # Get top card
                    card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                    # Flip face up
                    card.face_up()
                    # Move card position to bottom-right face up pile
                    card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                    # Remove card from face down pile
                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)
                    # Move card to face up list
                    self.piles[BOTTOM_FACE_UP_PILE].append(card)
                    # Put on top draw-order wise
                    self.pull_to_top(card)

            elif primary_card.is_face_down: ############################################################## Change this so that cards in middle pile auto flip instead of requiring a click #############
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])

                # Is this a stack of cards? If so, grab the other cards too
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)

        else:

            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                    # Flip the deck back over so we can restart
                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[BOTTOM_FACE_UP_PILE].remove(card)
                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[BOTTOM_FACE_DOWN_PILE].position

    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index
    
    #new version of this
    def move_card_to_new_pile(self, card, pile_index): ############### This is where the logic for checking if valid card to drop on should go (?)
        ############################################################## Maybe make a seperate function to check if valid drop and call it here
        ############################################################## Function can also take in a ruleset in args in order to work with multiple gametypes
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        #self.check_valid_klondike_drop(card, pile_index)
        self.piles[pile_index].append(card)
    
    
    # def move_card_to_new_pile(self, card, pile_index): ############### This is where the logic for checking if valid card to drop on should go (?)
    #     ############################################################## Maybe make a seperate function to check if valid drop and call it here
    #     ############################################################## Function can also take in a ruleset in args in order to work with multiple gametypes
    #     """ Move the card to a new pile """
    #     self.remove_card_from_pile(card)
    #     self.piles[pile_index].append(card)
    
    def get_intvalue(self, card):
        if (card.value == "A"):
            cardvalue = 1
        elif (card.value == "J"):
            cardvalue = 11
        elif (card.value == "Q"):
            cardvalue = 12
        elif (card.value == "K"):
            cardvalue = 13
        else:
            cardvalue = int(card.value)
        return cardvalue

    def check_valid_klondike_drop(self, pile_card, hand_card):
        pilecard_val = self.get_intvalue(pile_card)
        handcard_val = self.get_intvalue(hand_card)
        #pilecard_val = 2
        #handcard_val = 1
        print("handcard_val=", handcard_val)
        print("pilecard_val=", pilecard_val)

        if ((hand_card.suit == "Hearts" or hand_card.suit == "Diamonds") and (pile_card.suit == "Hearts" or pile_card.suit == "Diamonds")):
            return False
        elif ((hand_card.suit == "Spades" or hand_card.suit == "Clubs") and (pile_card.suit == "Spades" or pile_card.suit == "Clubs")):
            return False
        elif (pilecard_val - 1 != handcard_val):
            return False
        else:
            return True 
        
    def check_valid_top_drop(self, pile_card, hand_card):
        pilecard_val = self.get_intvalue(pile_card)
        handcard_val = self.get_intvalue(hand_card)
        
        if hand_card.suit != pile_card.suit:
            return False
        elif(handcard_val - 1 != pilecard_val):
            return False
        else:
            return True

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True
        pile_index = self.pile_mat_list.index(pile)

        # See if we are in contact with the closest pile
        if(len(self.piles[pile_index]) > 0):
            tmp = self.piles[pile_index][-1]
        else:
            tmp = pile
        
        if arcade.check_for_collision(self.held_cards[0], tmp):

            # What pile is it?
            #pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a middle play pile?
            ##################################################################################### Function to check valid drop needs to be called here as well
            elif PLAY_PILE_1 <= pile_index <= PLAY_PILE_7:
                
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    #top_card is the card at the bottom of the pile we are dropping on
                    top_card = self.piles[pile_index][-1]
                    #hand_card is the card at the top of the list of cards in our hand
                    hand_card = self.held_cards[0]
                    print("pilecard_val=", self.get_intvalue(top_card))
                    print("handcard_val=", self.get_intvalue(hand_card))
                    isValid = self.check_valid_klondike_drop(top_card, hand_card)######################
                    if isValid:
                        for i, dropped_card in enumerate(self.held_cards):
                            dropped_card.position = top_card.center_x, \
                                                    top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                        for card in self.held_cards:
                            # Cards are in the right position, but we need to move them to the right list
                            self.move_card_to_new_pile(card, pile_index)
                        reset_position = False
                    else:
                        reset_position = True
                else:
                    # Are there no cards in the middle play pile?
                    check_king = self.get_intvalue(self.held_cards[0])
                    print("check_king = ", check_king)
                    if(check_king != 13):
                        reset_position = True
                    else:
                        for i, dropped_card in enumerate(self.held_cards):
                            # Move cards to proper position
                            dropped_card.position = pile.center_x, \
                                                    pile.center_y - CARD_VERTICAL_OFFSET * i
                        for card in self.held_cards:
                            # Cards are in the right position, but we need to move them to the right list
                            self.move_card_to_new_pile(card, pile_index)
                        reset_position = False

                # for card in self.held_cards:
                #     # Cards are in the right position, but we need to move them to the right list
                #     self.move_card_to_new_pile(card, pile_index)

                #Success, don't reset position of cards
                #reset_position = False

            # Release on top play pile? And only one card held?
            elif TOP_PILE_1 <= pile_index <= TOP_PILE_4 and len(self.held_cards) == 1: ######################################################### doesnt this if elif elif statement need an else?
                # Move position of card to pile
                
                if len(self.piles[pile_index]) == 0:
                    # check to make sure first card in top pile is ace
                    checkAce = self.get_intvalue(self.held_cards[0])
                    if checkAce != 1: # if not an ace, send card back
                        reset_position = True
                    else:
                        self.held_cards[0].position = pile.position
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                        reset_position = False
                else:
                    isValid = self.check_valid_top_drop(self.piles[pile_index][-1], self.held_cards[0])######################
                    if isValid:
                        self.held_cards[0].position = pile.position
                        # Move card to card list
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                        reset_position = False
                    else:
                        reset_position = True
        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
            
    def debugFunc():
        print("hi")


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()