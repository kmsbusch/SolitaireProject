import collections

'''
Card and PokerDeck (originally named FrenchDeck) borrowed from "Fluent Python" by 
Luciano Ramalho.

'''


Card = collections.namedtuple('Card', ['rank', 'suit'])
'''
Card is a "named tuple" data type. Named tuples are like classes with no functions -
in other words they are bundles of attributes. In this case, a Card has a rank and suit.
'''


class Deck(collections.MutableSequence):

    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):  # <1>
        self._cards[position] = value

    def __delitem__(self, position):  # <2>
        del self._cards[position]

    def insert(self, position, value):  # <3>
        self._cards.insert(position, value)
        
    def sub_face_cards(ranks):
        '''
        >>> hand1 = [Card(rank='J', suit='♦'), Card(rank='10', suit='♦'), Card(rank='A', suit='♦'), Card(rank='Q', suit='♦'), Card(rank='K', suit='♦')]
        >>> ranks = find_ranks(hand1)
        >>> sub_face_cards(ranks)
        ['11', '10', '14', '12', '13']
        '''
        for card in ranks:
            if card == 'J':
                i = ranks.index('J')
                ranks[i] = '11'
            elif card == 'Q':
                i = ranks.index('Q')
                ranks[i] = '12'            
            elif card == 'K':
                i = ranks.index('K')
                ranks[i] = '13'
        if 'A' in ranks:
            i = ranks.index('A')
            if 'A' in ranks and '2' in ranks:  # check for pair before straight      
                ranks[i] = '1'
            else:
                ranks[i]= '14'
        return ranks