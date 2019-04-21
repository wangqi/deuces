from .card import Card


class Player:

	def __init__(self, id, deck, name=None, card_strs=None):
		self.id = id
		self.name = name
		if self.name is None:
			self.name = 'player-'+str(id)
		self.deck = deck
		self.cards = []
		if card_strs is not None:
			for card_str in card_strs:
				self.cards.append(Card.new(card_str))

	def draw_cards(self, card_strs=None, num=2):
		if card_strs is not None:
			for card_str in card_strs:
				card_int = Card.new(card_str)
				self.cards.append(card_int)
			return self.deck.draw_card(card_strs)
		else:
			self.cards = self.deck.draw(num)
			return self.cards

	def get_cards(self):
		return self.cards

	def __repr__(self):
		player_text = "Player '%s' has cards" % self.name
		player_text += Card.format_pretty_cards(self.cards)
		return player_text
