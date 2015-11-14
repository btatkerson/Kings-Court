import os
from gameboard import gameboard
from game_player import game_player
#from gridgame import gridgame

gamemode = int(input("0: X\n1: Snowflake\n2: Circle\nPick initial board setup >"))

main_game = gameboard(0,gamemode)
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

print([[i[0].get_info(),i[1]] for i in player[0].best_possible_move_set()])


player[1].set_computer_level(3)
player[2].set_computer_level(4)
player[3].set_computer_level(5)

while main_game.is_move_possible():
    #os.system('clear')
    player[0].read_all_moves()
    #print('Average:',player[0].list_of_possible_scores())
    print('Average:',player[0].average_of_possible_scores())
    print('Standard Dev:',player[0].standard_deviation_of_possible_scores())
    temp_move =player[0].get_computer_move()
    print('Computer Move:',temp_move[0].get_info_color(),temp_move[1])
    #print(player[0].card_hand.get_unique_cards_in_deck())
    main_game.print_game_board_color()
    print("Scores:")

    for i in range(0,4):
        print('Player',i+1,"\b:",player[i].get_last_score(),"+",player[i].get_score()-player[i].get_last_score(),"=",player[i].get_score())
    
    player[0].card_hand.print_readable_deck_color()
    
    strx = None
    while not player[0].place_card_by_str(strx):
        strx = input("Card/Spot (card, pos) \'2 A4\'> ")

    for i in range(1,4):
        move_set = player[i].get_computer_move()

        if len(move_set) > 0:
            player[i].place_card_on_board(move_set[0],move_set[1])
        else:
            if not player[i].card_hand.is_deck_empty():
                player[i].card_hand.deal_card()
    main_game.get_cards_not_on_board()


main_game.print_game_board_color()
print("Final Scores:")

for i in range(0,4):
    print('Player',i+1,"\b:",player[i].get_score())

 
