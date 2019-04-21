from .card import Card
from .deck import Deck
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
		lines.append(str(self.num_player))
		for player_key in self.player_keys:
			lines.append(player_key + "=" + self.players.get(player_key, ""))
		if self.flop_card_strs is not None and len(self.flop_card_strs) > 0:
			lines.append(self.flop_card_strs)
		with open(STATUS_FILE, 'w') as f:
			for line in lines:
				if len(line) > 0:
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
		if len(lines) > num_players+1:
			round.set_flop_cards(lines[-1].strip())
		return round
