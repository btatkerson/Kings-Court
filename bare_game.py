import gameboard
import game_player

game = gameboard.gameboard(gamemode=1)
game.reset_game()
players = [game_player.game_player("Player " + str(i+1),1,game) for i in range(4)]
c=0

while 1:
    if not players[c%4].drawl_card_from_deck():
        break
    c+=1

print(game.get_card_deck().print_readable_deck_color())
game.print_game_board_color()

def reset_game(mode=None):
    if mode in [i for i in range(9)]:
        game.set_game_mode(mode)
    game.reset_game()
    reset_players()


def reset_players():
    for i in players:
        i.reset_player_hand_and_score()
    c=0
    while 1:
        if not players[c%4].drawl_card_from_deck():
            break
        c+=1
