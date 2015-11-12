import os
from gameboard import gameboard
from game_player import game_player
#from gridgame import gridgame

main_game = gameboard(0,2)
player = [game_player('Player ' + str(i),0,main_game) for i in range(1,5)]

player[0].human_player=1

main_game.game_deck.shuffle_deck()

main_game.print_game_board_color()

count = 0

while not main_game.game_deck.is_deck_empty():
    player[count % len(player)].get_hand().take_card(main_game.game_deck.deal_card())
    count+=1

for i in player:
    i.card_hand.sort_deck_by_card_suit()
    i.card_hand.sort_deck_by_card_value()
    color_deck = [str(j.get_info_color()) for j in i.card_hand.get_deck()]

    for k in color_deck:
        print(k,end=',')


    print()

while not player[3].card_hand.is_deck_empty():
    #os.system('clear')
    main_game.print_game_board_color()
    print("Scores:")

    for i in range(0,4):
        print('Player',i+1,"\b:",player[i].get_last_score(),"+",player[i].get_score()-player[i].get_last_score(),"=",player[i].get_score())

    player[0].card_hand.print_readable_deck_color()
    
    strx = None
    while not player[0].place_card_by_str(strx):
        strx = input("Card/Spot (card, pos) \'2 A4\'> ")

    for i in range(1,4):
        move_set = player[i].best_possible_move_set()
        if len(move_set) > 0:
            player[i].place_card_on_board(move_set[0][0],move_set[0][1])
        else:
            if not player[i].card_hand.is_deck_empty():
                player[i].card_hand.deal_card()


main_game.print_game_board_color()
print("Scores:")

for i in range(0,4):
    print('Player',i+1,"\b:",player[i].get_last_score(),"+",player[i].get_score()-player[i].get_last_score(),"=",player[i].get_score())

 
