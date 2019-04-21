from deuces import Card, Evaluator, Deck, Round, Player
import os


round = Round.read_status()

PRIORITIES = [
	"Straight Flush",
    "Four of a Kind",
    "Full House",
    "Flush",
    "Straight",
    "Three of a Kind",
    "Two Pair",
    "Pair",
    "High Card"
]

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

deck = Deck()
first_player = Player(0, deck=deck)
default_init_cards = round.get_player_cards(0, first_player.name)
init_card_str = input("Input the initial 2 cards for player: %s. Last: %s \n" %
                      (first_player.name, default_init_cards))
cards = default_init_cards.split(",")
first_player.draw_cards(cards)
print(first_player)

print("\n=== Begin Simulation ===")
result = {}
# create an evaluator
evaluator = Evaluator()
winner_methods = {}
winner_players = {}
deck.save()

for i in range(0, 10000):
	deck.reset()
	players = []
	players.append(first_player)
	for player_id in range(1, num_players, 1):
		player = Player(player_id, deck=deck)
		card_ints = player.draw_cards(num=2)
		players.append(player)
	flop_card_ints = deck.flop()
	# print("Flops: " + Card.format_pretty_cards(flop_card_ints))
	# print("Total left cards in deck: %d" % deck.left_card_num())

	flop_card_ints = deck.get_flop_card_ints()
	turn_card_int = deck.draw()
	flop_card_ints.append(turn_card_int)
	river_card_int = deck.draw()
	flop_card_ints.append(river_card_int)
	# evaluator.hand_summary(board=flop_card_ints, hands=[player.cards for player in players])
	hands = [player.cards for player in players]
	winner_method, winner_player = evaluator.hand_evaluate(board=flop_card_ints, players=players, debug=False)
	method_count = winner_methods.get(winner_method, 0)
	winner_methods[winner_method] = method_count+1
	player_count = winner_players.get(winner_player.name, 0)
	winner_players[winner_player.name] = player_count+1

print("\n=== End Simulation ===")
# print(winner_methods)
# print(winner_players)

print("\n------------------------------\n")
print("{:<20} {:<10} {:<10}".format('Method','Count','Percent'))
for key in PRIORITIES:
	k = key
	v = winner_methods.get(key, 0)
	print("{:<20} {:<10} {:<10}".format(k, v, str(v/100.0)+"%"))
print("\n------------------------------\n")
print("{:<20} {:<10} {:<10}".format('Player','Count','Percent'))
for i in range(num_players):
	k = "player-" + str(i)
	v = winner_players.get(k, 0)
	print("{:<20} {:<10} {:<10}".format(k, v, str(v / 100.0) + "%"))