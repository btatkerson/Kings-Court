import gameboard
import game_player

game = gameboard.gameboard(gamemode=1)
game.reset_game()
moves_left = len(game.get_cards_not_on_board())
players = [game_player.game_player("Player " + str(i+1),1,game) for i in range(4)]
c=0

while 1:
    if not players[c%4].drawl_card_from_deck():
        break
    c+=1

print(game.get_card_deck().print_readable_deck_color())
game.print_game_board_color()

def player_gen():
    current_player = -1
    while 1:
        current_player = (current_player + 1) % len(players)
        yield current_player

pg = player_gen()
def make_moves(num=1):
    if num > 0:
        for i in range(num):
            current_player = pg.__next__()
            p(current_player).make_play_on_board(computer_determination=1)
            current_player = (current_player + 1) % len(players)



def reset_game(mode=None):
    if mode in [i for i in range(9)]:
        game.set_game_mode(mode)
    game.reset_game()
    reset_players()
    pg = player_gen()


def reset_players():
    for i in players:
        i.reset_player_hand_and_score()
        i.set_gameboard(game)
    c=0
    while 1:
        if not players[c%4].drawl_card_from_deck():
            break
        c+=1

def p(num=None):
    if num != None:
        return players[num] 
        return game_player.game_player()
    return players[0]

reset_game(3)


c=p(0).get_hand().deck[0]

c.get_info(1)
