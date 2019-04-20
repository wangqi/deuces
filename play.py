from deuces import Card, Evaluator, Deck
import os

STATUS_FILE = "round.state"


class Round:

	def __init__(self, num_player=0):
		self.num_player = num_player
		self.players = {}
		self.player_keys = []
		self.flop_card_strs = ""

	def add_player_cards(self, player_id, player_name, card_strs):
		key = str(player_id) + "|" + player_name
		if self.players.get(key) is None:
			self.player_keys.append(key)
		self.players[key] = card_strs

	def add_player_card_ints(self, player_id, player_name, card_ints):
		key = str(player_id) + "|" + player_name
		card_strs = ""
		for card_int in card_ints:
			card_strs += Card.int_to_str(card_int) + ","
		card_strs = card_strs[0:-1]
		if self.players.get(key) is None:
			self.player_keys.append(key)
		self.players[key] = card_strs

	def get_player_cards(self, player_id, player_name):
		key = str(player_id) + "|" + player_name
		return self.players.get(key, "")

	def set_flop_cards(self, flop_card_strs):
		self.flop_card_strs = flop_card_strs

	def get_flop_cards(self):
		return self.flop_card_strs

	def add_flop_card(self, card_int):
		card_str = Card.int_to_str(card_int)
		if len(self.flop_card_strs) == 0:
			self.flop_card_strs = card_str
		else:
			self.flop_card_strs += "," + card_str

	def save_status(self):
		lines = []
		lines.append(str(num_players))
		for player_key in self.player_keys:
			lines.append(player_key + "=" + self.players.get(player_key, ""))
		if self.flop_card_strs is not None and len(self.flop_card_strs) > 0:
			lines.append(self.flop_card_strs)
		with open(STATUS_FILE, 'w') as f:
			for line in lines:
				f.write(line)
				f.write("\n")

	@staticmethod
	def read_status():
		lines = []
		if not os.path.exists(STATUS_FILE):
			return
		with open(STATUS_FILE, 'r') as f:
			lines = f.readlines()
		if len(lines) > 0:
			num_players = int(lines[0])
		round = Round(num_player=num_players)
		for line_idx in range(1, num_players+1, 1):
			line = lines[line_idx]
			fields = line.split("=")
			player_key = fields[0]
			player_cards = fields[1].strip()
			player_fields = player_key.split("|")
			round.add_player_cards(player_id=player_fields[0], player_name=player_fields[1],
			                       card_strs=player_cards)
		if len(lines) > num_players+2:
			round.set_flop_cards(lines[-1])
		return round


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


round = Round.read_status()
if round is not None and round.num_player > 0:
	restore_last_round = input("Do you want to restore last round (y/n) ? \n")
	if restore_last_round == 'n':
		round = None
		num_players = 2
	else:
		num_players = round.num_player
else:
	num_players = 2

num_players = input("Number of players? (%s) \n" % num_players)
if num_players == '':
	num_players = 2
else:
	num_players = int(num_players)
if num_players > 9:
	num_players = 9
print("> total %d players" % num_players)

if round is None:
	round = Round(num_players)

players = []
deck = Deck()
for player_id in range(num_players):
	player = Player(player_id, deck=deck)
	default_init_cards = round.get_player_cards(player_id, player.name)
	init_card_str = input("Input the initial 2 cards for player: %s. Last: %s \n" %
	                      (player.name, default_init_cards))
	if len(init_card_str) == 0:
		if len(default_init_cards) == 0:
			card_ints = player.draw_cards(num=2)
			round.add_player_card_ints(player_id, player.name, card_ints)
		else:
			cards = default_init_cards.split(",")
			player.draw_cards(cards)
			round.add_player_cards(player_id=player_id, player_name=player.name, card_strs=default_init_cards)
	else:
		init_cards = init_card_str.split(",")
		player.draw_cards(init_cards)
		round.add_player_cards(player_id=player_id, player_name=player.name, card_strs=init_cards)
	players.append(player)

for player in players:
	print(player)

flop_card_input = input("Input the flop cards. Last: " + round.get_flop_cards())
flop_card_ints = []
if flop_card_input is None or len(flop_card_input) == 0:
	flop_card_input = round.get_flop_cards()
if len(flop_card_input) == 0:
	flop_card_ints = deck.flop()
	for flop_card_int in flop_card_ints:
		round.add_flop_card(flop_card_int)
else:
	flop_card_strs = flop_card_input.split(",")
	flop_card_ints = deck.flop_card(flop_card_strs)
print("Flops: " + Card.format_pretty_cards(flop_card_ints))
print("Total left cards in deck: %d" % deck.left_card_num())

round.save_status()

turn_card_int = deck.draw()
flop_card_ints.append(turn_card_int)
river_card_int = deck.draw()
flop_card_ints.append(river_card_int)
print("Turn and river cards: " + Card.format_pretty_cards(flop_card_ints))
# create an evaluator
evaluator = Evaluator()
evaluator.hand_summary(board=flop_card_ints, hands=[player.cards for player in players])

