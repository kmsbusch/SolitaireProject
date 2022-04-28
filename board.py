import arcade
import random
import pickle

from typing import Optional

from sympy import N
from cardsprite import CardSprite
import game


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
TOP_Y = game.SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

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



class Board(object):
    #Singleton Private 
    _instance = None
    
    #Singleton Implementation
    def __new__(cls, ruleset):
        if cls._instance is None:
            cls._instance = super(Board, cls).__new__(cls)
            if ruleset == "klondike":
                # Sprite list with all the cards, no matter what pile they are in.
                cls.card_list: Optional[arcade.SpriteList] = None
                
                cls._state = []

                cls.observers = []

                # arcade.set_background_color(arcade.color.AMAZON)

                # List of cards we are dragging with the mouse
                cls.held_cards = None

                # Original location of cards we are dragging with the mouse in case
                # they have to go back.
                cls.held_cards_original_position = None

                # Sprite list with all the mats that the cards lay on.
                cls.pile_mat_list = None

                # Create a list of lists, each holds a pile of cards.
                cls.piles = None
                #cls.setup()
        return cls._instance
    
    def subscribe(self, observer):
        self.observers.append(observer)
        print("subscribed " + observer.name)
        
    def unsubscribe(self, observer):
        self.observers.remove(observer)
        print("unsubscribed " + observer.name)

    def notify_observers(self, value):
        for observer in self.observers:
            observer.up(value)    
    
    #ave func for cards for pickle?
    def set_memento(cls, memento):
        previous_state = pickle.load(memento)
        #vars(cls).clear()
        #vars(cls).update(previous_state)
        cls.piles = previous_state
        cls.pile_mat_list.draw()
        cls.card_list.draw()
        # pass
        # for i, pile in enumerate(previous_state):
        #     cls.piles[i] = pile
        # return cls.piles

    def create_memento(cls):
        picklefile = open('card_state','wb')
        temp_pile = []
        pickle.dump(cls.piles, picklefile)
        # for x in cls.piles:
        #     print(x)
        #     if len(x) > 0:
        #         for card in x:
        #             temp = card.pickle_card(picklefile = open('card_pickle','wb'))
        #             temp.close()
        #             pickle.dump(temp, picklefile)
        #         # pickle.dump(x, picklefile)
        picklefile.close()

    # def pickle_board(self):
    #     return pickle.dump(self)
    
    # def unpickle_board(self):
    #     return pickle.load(self)

    def setup(cls):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        cls.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        cls.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats that the cards lay on.
        #cls.pile_mat_list: arcade.SpriteList = arcade.SpriteList()
        cls.pile_mat_list = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        cls.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        cls.pile_mat_list.append(pile)

        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
            #pile.position = cls.pile_mat_list[i].center_x, \
            #                     cls.pile_mat_list[i].center_y - CARD_VERTICAL_OFFSET * (i)
            cls.pile_mat_list.append(pile)

        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            cls.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

        # Sprite list with all the cards, no matter what pile they are in.
        cls.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = CardSprite(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                cls.card_list.append(card)

        # Shuffle the cards
        for pos1 in range(len(cls.card_list)):
            pos2 = random.randrange(len(cls.card_list))
            cls.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        cls.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in cls.card_list:
            cls.piles[BOTTOM_FACE_DOWN_PILE].append(card)

        # - Pull from that pile into the middle piles, all face-down
        # Loop for each pile
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            # Deal proper number of cards for that pile
            for j in range(pile_no - PLAY_PILE_1 + 1):
                # Pop the card off the deck we are dealing from
                card = cls.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # Put in the proper pile
                cls.piles[pile_no].append(card)
                # Move card to same position as pile we just put it in
                #card.position = cls.pile_mat_list[pile_no].position
                card.position = cls.pile_mat_list[pile_no].center_x, \
                                cls.pile_mat_list[pile_no].center_y - CARD_VERTICAL_OFFSET * (j)
                # Put on top in draw order
                cls.pull_to_top(card)
                #top_card = cls.piles[pile_no][-1]
                
                                        
                

        # Flip up the top cards
        for i in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            cls.piles[i][-1].face_up()
    
    def check_win(cls):
        won = False
        for x in range(2, 9):
            if len(cls.piles[x]) == 0:
                won = True
            else:
                won = False
        return won

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    
    
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
        self.create_memento()
        self.remove_card_from_pile(card)
        #self.check_valid_klondike_drop(card, pile_index)
        self.piles[pile_index].append(card)
        if self.check_win():
            self.notify_observers(self.check_win())
        
    
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
        
    
    