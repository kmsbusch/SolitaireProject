import arcade
import pickle
import collections


#Code referenced from https://api.arcade.academy/en/latest/tutorials/card_game/index.html 
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

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

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
################################################################################################################### Might wanna end up making a translator for J, Q, K values to 11,12,13 so card above check works
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

#https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html
#factory
class Card_Factory_By_Suit(arcade.Sprite):
    @staticmethod
    def create_card(card_suit):
        cards_all_one_suit = arcade.SpriteList()
        for x in range(0,13):
            temp_card = Card(card_suit, CARD_VALUES[x], 0.6)
            temp_card.position = START_X, BOTTOM_Y
            cards_all_one_suit.append(temp_card)
        return cards_all_one_suit
    # create_card = staticmethod(create_card)


class Card(arcade.Sprite):
    """ Card sprite """
    # _position = (START_X, START_Y)

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value
        

    
        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")
        # self.center_x = position[0]
        # self.center_y = position[1]
        
    def __getstate__(self):
        return [self.suit, self.value, self.image_file_name, self.is_face_up]
    
    def __setstate__(self, cardlist):
        self.suit = cardlist[0]
        self.value = cardlist[1]
        self.image_file_name = cardlist[2]
        self.is_face_up = cardlist[3]
    
    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True
        
    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    # def pickle_card(self, picklefile):
    #     pickle.dump(vars(self), picklefile)

    
    # def unpickle_card(self, picklefile):
    #     return pickle.load(picklefile)

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up
