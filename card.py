import arcade
import pickle
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

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
        
        def pull_to_top(self, card: arcade.Sprite):
            """ Pull card to top of rendering order (last to render, looks on-top) """

            # Remove, and append to the end
            self.card_list.remove(card)
            self.card_list.append(card)

    def pickle_card(self):
        return pickle.dump(self)
    
    def unpickle_card(self):
        return pickle.load(self)

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up
