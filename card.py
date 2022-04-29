import arcade
import pickle
#import dill
import collections
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

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
