from random import shuffle
from .card import Card

class Deck:
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []

    def __init__(self):
        self.cards = []
        self.flop_cards = []
        self.shuffle()

    def shuffle(self):
        # and then shuffle
        self.cards = Deck.GetFullDeck()
        shuffle(self.cards)

    def draw_card(self, card_strs):
        card_ints = []
        for card_str in card_strs:
            card_int = Card.new(card_str)
            card_ints.append(card_int)

        # Remove given cards from desk
        for card in self.cards:
            for card_int in card_ints:
                if card == card_int:
                    self.cards.remove(card_int)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def flop(self, num=3):
        if len(self.flop_cards) > 0:
            return
        for i in range(num):
            self.flop_cards.append(self.draw())
        return self.flop_cards

    def flop_card(self, card_strs):
        if card_strs is None:
            return self.flop(3)
        self.flop_cards = self.draw_cards(card_strs)
        return self.flop_cards

    def left_card_num(self):
        return len(self.cards)

    def __str__(self):
        return Card.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck():
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)