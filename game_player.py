import random
import stats
from carddeck import carddeck
from gameboard import gameboard
from PyQt4 import QtGui

class game_player():
    def __init__(self,name=None, human_player=None, main_gameboard=None):
        self.name = name
        self.human_player = True if human_player else False 
        self.mercy = False
        self.set_computer_level()
        self.last_score = 0
        self.score = 0
        self.card_hand = carddeck(0,0)
        if not main_gameboard:
            self.gameboard = gameboard()
        else:
            self.gameboard = main_gameboard

    def set_gameboard(self, t_gameboard=None):
        if isinstance(t_gameboard, gameboard):
            self.gameboard = t_gameboard
            return 1
        return 0

    def reset_player_hand_and_score(self):
        self.mercy = False
        self.last_score = 0
        self.score = 0
        self.card_hand.reset_deck()

    def set_name(self,name=None):
        if type(name) in [int,float,str,chr]:
            self.name = str(name)
            return 1

        self.name = 'Player'
        return 0

    def get_name(self):
        return self.name

    def is_computer(self):
        return not self.human_player

    def is_human(self):
        return self.human_player

    def set_human(self, is_human=None):
        if is_human:
            self.human_player = True
            return 1
        self.human_player = False
        return 0

    def get_last_score(self):
        return self.last_score

    def get_score(self):
        return self.score

    def set_score(self, add=None, absolute=False):
        '''
        Sets the player's score

        add will adjust the score by a positive/negative integer value, 

        absolute will set the score to the value given to 'add'
        '''

        if type(add) in [int, float]:
            if absolute:
                self.last_score = self.score
                self.score = int(add)
                return 1
            self.last_score = self.score
            self.score += int(add)
            return 1

    def get_hand(self):
        return self.card_hand

    def get_cards_in_hand(self):
        return self.card_hand.deck

    def place_card_by_str(self, deal_str=None):
        if type(deal_str) != str:
            return 0

        temp_list = deal_str.split()
        temp_str = 'ABCDEFG'
        if len(temp_list)==2:
            print(temp_list)
            try:
                pos = [i for i in temp_list[1].upper()]
                print(pos)
                if len(pos)==2:
                    new_pos = [temp_str.index(pos[0]),int(pos[1])-1]
                    pos = new_pos
                temp_list=[int(temp_list[0])-1,pos]
                print(temp_list)
            except:
                return 0
            return self.place_card_on_board(self.card_hand.find_card_by_index(temp_list[0]),temp_list[1])
        return 0
        
    def drawl_card_from_deck(self, card_deck = None):
        if not card_deck and self.gameboard:
            if self.gameboard.get_card_deck().is_deck_empty():
                return 0
            return self.card_hand.take_card_from_different_deck(self.gameboard.get_card_deck())
        elif isinstance(card_deck,carddeck):
            return self.card_hand.take_card(card_deck.get_car_deck().deal_card())
        return 0

    def place_card_on_board(self, card_to_deal=None, position=None):
        if type(card_to_deal) == list:
            if len(card_to_deal) > 0:
                card_to_deal = card_to_deal[0]
            else:
                return 0

        if self.gameboard.is_legal_to_anchor_card(card_to_deal, position) or self.has_mercy():
            self.last_score = self.score
            self.score += self.gameboard.get_score_to_anchor_card(card_to_deal,position, mercy=self.has_mercy())
            self.card_hand.deal_card([card_to_deal])
            self.gameboard.set_card_on_board(card_to_deal,position)
            return 1
        else:
            return 0

    def list_of_possible_scores(self, above_score=None):
        '''
        Returns a list of only the score values that can be potentially made
        This is used for mathematical purposes
        
        Parameter:
        above_score = int, float. 
        
        If 0 < above_score < 1, function returns only the top (above_score)% 
        ex. list_of_possible_scores(.60) returns the top 60% of the scores.

        if above_score <= 0 or above_score >= 1, function returns all the scores above
        int(above_score).
        ex. list_of_possible_scores(2) returns all the scores above 2
        '''
        all_score_list = []
        temp_move_set = self.possible_move_set()

        for i in temp_move_set.keys():
            all_score_list+=len(temp_move_set[i])*[i]

        
        if above_score != None:
            all_score_list = sorted(all_score_list)
            if type(above_score) == float:
                if 0 < above_score < 1:
                    temp_score_list = all_score_list[int(len(all_score_list)*(1-above_score)):len(all_score_list)]
                    if len(temp_score_list) > 0:
                        return temp_score_list
                else:
                    above_score = int(above_score)
                    
            if type(above_score) == int:
                temp_score_list = []
                for i in all_score_list:
                    if i >= above_score:
                        temp_score_list.append(i)

                if len(temp_score_list) > 0:
                    return temp_score_list

        return all_score_list

    def average_of_possible_scores(self, above_score=None):
        score_list = self.list_of_possible_scores(above_score)
        if len(score_list) > 0:
            return sum(score_list)/len(score_list)

    def standard_deviation_of_possible_scores(self, above_score=None):
        average = self.average_of_possible_scores(above_score)
        score_list = self.list_of_possible_scores(above_score)
        devs = 0
        if len(score_list) > 0:
            for i in score_list:
                devs += (i-average)**2
        else:
            return 0

        return (devs/len(score_list))**.5

    def set_computer_level(self,level=3):
        if 0 <= level % 6 <= 5:
            self.computer_level = level % 6
            return 1
        else:
            self.computer_level = 3
        return 0


    def get_computer_level(self):
        return self.computer_level
            
    
    def get_computer_level_stats(self):
        levels = {0:(.254,1.28,0),
                  1:(.385,1.645,3),
                  2:(.385,1.645,4),
                  3:(.595,1.96,4),
                  4:(.675,2.05,5),
                  5:(.841,2.5,5)}

        return levels[self.computer_level]


    def make_play_on_board(self, card=None, spot=None, computer_determination=False):
        if computer_determination:
            cm = self.get_computer_move()
            self.make_play_on_board(cm[0],cm[1])
        if card in self.card_hand.get_deck() and self.gameboard.verify_coordinate(spot):
            self.set_score(self.gameboard.get_score_to_anchor_card(card, spot, mercy=self.has_mercy()))
            self.gameboard.set_card_on_board(self.card_hand.deal_card([card])[0],spot)
            return 1
        return 0

    def get_cards_not_in_hand_or_board(self):
        cards_not_on_board = self.gameboard.get_cards_not_on_board()
        temp = []
        for i in cards_not_on_board:
            if i not in self.get_cards_in_hand():
                temp.append(i)

        return temp

    def get_frequency_of_values_for_cards_in_hand(self, relative=False, printable=False):
        return stats.frequency([i.get_value() for i in self.get_cards_in_hand()], relative, printable)

    def get_frequency_of_values_for_cards_not_in_hand_or_board(self, relative=False, printable=False):
        return stats.frequency([i.get_value() for i in self.get_cards_not_in_hand_or_board()], relative, printable)

    def get_priority_of_cards(self):
        cards_in_hand = {i:0 for i in self.get_cards_in_hand()}
        non_breaks = {i.get_value():self.gameboard.get_open_non_breaking_legal_spots_for_card(i,1) for i in cards_in_hand}






    def get_computer_move(self):
        self.get_computer_move_v2()
        possible_moves = self.possible_move_set()
        if not possible_moves:
            return []
        bottom, top, bonus_chance_for_best_move = self.get_computer_level_stats()
        mean_score = self.average_of_possible_scores()
        std_dev_of_scores = self.standard_deviation_of_possible_scores()
        
        bottom_score = mean_score+std_dev_of_scores*bottom
        bot_int = int(bottom_score+.5)
        top_score = mean_score+std_dev_of_scores*top

        perc_position = sum([random.randint(0,1000) for i in range(2)])/2000
        temp_moves = self.best_possible_move_set()
        best_score = self.best_possible_move_set(1)

        if std_dev_of_scores:
            z_score = (best_score-mean_score)/std_dev_of_scores
        else:
            z_score = 0

        if perc_position-(.95-bonus_chance_for_best_move/100-.05*(z_score/2.5))>0:
            return temp_moves[random.randint(0,len(temp_moves)-1)]
        elif perc_position-.05<=0:
            if bot_int in possible_moves.keys():
                return possible_moves[bot_int][random.randint(0,len(possible_moves[bot_int])-1)]
            else:
                count=1
                temp_int = bot_int+count
                while temp_int not in possible_moves.keys():
                    count += 1
                    if count % 2==0:
                        temp_int-=count
                    else:
                        temp_int+=count

                return possible_moves[temp_int][random.randint(0,len(possible_moves[temp_int])-1)]

        else:
            base_score = int((top_score-bottom_score)*perc_position+bottom_score+.5)
            if base_score in possible_moves.keys():
                return possible_moves[base_score][random.randint(0,len(possible_moves[base_score])-1)]
            else:
                count=1
                temp_int = base_score+count
                while temp_int not in possible_moves.keys():
                    count += 1
                    if count % 2==0:
                        temp_int-=count
                    else:
                        temp_int+=count

                return possible_moves[temp_int][random.randint(0,len(possible_moves[temp_int])-1)]


    def get_computer_move_v2(self):
        '''
        Returns a move based on a newer AI algorithm that uses known probabilities and 
        other known information about the current game that is available. All information
        used is fair to the game. For instance, this algorithm knows all the cards that 
        aren't on the board or in its own hand, but it has no way of knowing which players
        have which cards.
        '''
        open_spots = self.gameboard.get_spots_open_on_board()
        open_spots_playable = self.gameboard.get_open_spots_legally_playable()
        #standard_odds = [1, 5/6, 25/36, 125/216, 625/1296]
        standard_odds = [(5**i)/(6**i) for i in range(5)]
        standard_odds_comb = [1, 5/6, 15/21, 35/56, 70/126]
        side_neighbor_counts = [self.gameboard.get_spot_number_of_side_neighbors(i) for i in open_spots]
        side_neighbor_counts_legal = [self.gameboard.get_spot_number_of_side_neighbors(i) for i in open_spots_playable]
        average = sum([standard_odds[i] for i in side_neighbor_counts])/len(side_neighbor_counts)
        average_legal = sum([standard_odds[i] for i in side_neighbor_counts_legal])/len(side_neighbor_counts_legal)
        average_comb = sum([standard_odds_comb[i] for i in side_neighbor_counts])/len(side_neighbor_counts)
        average_comb_legal = sum([standard_odds_comb[i] for i in side_neighbor_counts_legal])/len(side_neighbor_counts_legal)
        temp_deck = carddeck(1,False)
        temp_deck.deal_card(temp_deck.find_card(value=[6,7,8,9,10,11,12],all_instances=True))
        temp_deck.deal_card(temp_deck.find_card(suit=[0,1,2],all_instances=True))
        value_chain = [0 for i in range(6)]
        value_chain_future = [0 for i in range(6)]
        for i in temp_deck.get_deck():
            for j in open_spots:
                value_chain_future[i.get_value()] += 1
                for k in self.gameboard.get_spot_neighbor_cards_sides(j):
                    if k.get_value() == i.get_value():
                        value_chain_future[i.get_value()] -= 1
                        break

                if self.gameboard.get_score_to_anchor_card(i,j,legal_score=True):
                    value_chain[i.get_value()]+=1

        value_chain=[i/len(open_spots) for i in value_chain]
        value_chain_spots=[i*len(open_spots) for i in value_chain]
        value_chain_future=[i/len(open_spots) for i in value_chain_future]
        value_chain_future_spots=[i*len(open_spots) for i in value_chain_future]
        
        value_chain_legal = [0 for i in range(6)]
        for i in temp_deck.get_deck():
            for j in open_spots_playable:
                if self.gameboard.get_score_to_anchor_card(i,j,legal_score=True):
                    value_chain_legal[i.get_value()]+=1

        value_chain_legal=[i/len(open_spots_playable) for i in value_chain_legal]
        value_chain_spots_legal=[i*len(open_spots_playable) for i in value_chain_legal]



        print(len(open_spots),'\n',value_chain,'\n',value_chain_spots,sum(value_chain_spots)/len(value_chain_spots),'\n',value_chain_future,'\n',value_chain_future_spots,sum(value_chain_future_spots)/len(value_chain_future_spots),'\n',len(open_spots_playable),'\n',value_chain_legal,'\n',value_chain_spots_legal,sum(value_chain_spots_legal)/len(value_chain_spots_legal))


        moves_dict = {i:[] for i in self.card_hand.get_deck()}
        for i in moves_dict.keys():
            for j in open_spots:
                legal=self.gameboard.get_score_to_anchor_card(i,j,mercy=self.mercy,legal_score=True) 

                if legal:
                    score=self.gameboard.get_score_to_anchor_card(i,j,mercy=self.mercy) 
                    moves_dict[i].append([score,j])

            #print(i.get_info_color(), sum([k[0] for k in moves_dict[i]])/len(moves_dict[i]),sorted(moves_dict[i],key=lambda x:x[0]), sep='\n')
            move_scores = sorted([k[0] for k in moves_dict[i]])
            if moves_dict != []:
                top_score = move_scores[-1]
            else:
                top_score = 0
            #print(i.get_info_color(), stats.average(move_scores), stats.std_dev_pop(move_scores), top_score, stats.norm_cdf(top_score,lis=move_scores),sorted(moves_dict[i],key=lambda x:x[0]), sep='\n')
            print(i.get_info_color(), stats.average(move_scores), stats.std_dev_pop(move_scores), top_score, stats.norm_cdf(top_score,lis=move_scores),sorted(moves_dict[i],key=lambda x:x[0]), sep='\n')

        len(moves_dict[i])/len(open_spots)


            

        possible_moves = self.possible_move_set()
        print("side_neigh_count=",side_neighbor_counts)
        print("average=",average,average*len(open_spots))
        print("average legal=",average_legal,average_legal*len(open_spots))
        print("average comb=",average_comb,average_comb*len(open_spots))
        print("average comb legal=",average_comb_legal,average_comb_legal*len(open_spots))

        print("Spread of Red")
        print('Count',len(self.gameboard.get_cards_on_board_of_suit('R')))
        print('Distance from midpoint - Avrg/Std Dev', self.gameboard.get_spread_of_cards_by_suit('R',vector=0))
        print('Midpoint and vector - Avrg/Std dev', self.gameboard.get_spread_of_cards_by_suit('R',vector=1))

        print("Spread of Blue")
        print('Count',len(self.gameboard.get_cards_on_board_of_suit('B')))
        print('Distance from midpoint - Avrg/Std Dev', self.gameboard.get_spread_of_cards_by_suit('B',vector=0))
        print('Midpoint and vector - Avrg/Std dev', self.gameboard.get_spread_of_cards_by_suit('B',vector=1))

        print("Spread of Green")
        print('Count',len(self.gameboard.get_cards_on_board_of_suit('G')))
        print('Distance from midpoint - Avrg/Std Dev', self.gameboard.get_spread_of_cards_by_suit('G',vector=0))
        print('Midpoint and vector - Avrg/Std dev', self.gameboard.get_spread_of_cards_by_suit('G',vector=1))

        print("Spread of Yellow")
        print('Count',len(self.gameboard.get_cards_on_board_of_suit('Y')))
        print('Distance from midpoint - Avrg/Std Dev', self.gameboard.get_spread_of_cards_by_suit('Y',vector=0))
        print('Midpoint and vector - Avrg/Std dev', self.gameboard.get_spread_of_cards_by_suit('Y',vector=1))


    def get_computer_move_v3(self):
        open_spots_on_board = self.gameboard.get_open_spots_legally_playable()
        cards_on_board = self.gameboard.get_cards_on_board()
        cards_not_on_board = self.gameboard.get_cards_not_on_board()
        cards_in_hand = self.get_cards_in_hand()
        cards_not_in_hand = [i for i in cards_not_on_board if i not in self.card_hand.deck]
        affected_spaces_by_card = {i:{self.gameboard.get_index_by_coordinates(j):self.gameboard.get_spots_affected_by_card_play(i,j) for j in open_spots_on_board} for i in cards_in_hand}
        
        return affected_spaces_by_card




            
    def possible_move_set(self):
        '''
        Returns a dictionary of lists in the form of [card,position] where the keys are
        the score that will be earned with the placement of the var card in var position
        '''
        temp_dict = {}
        temp_deck = carddeck(0,0)
        temp_deck.deck = self.card_hand.get_deck()
        for i in temp_deck.get_unique_cards_in_deck():
            for j in self.gameboard.get_spots_open_on_board():
                potential_score = self.gameboard.get_score_to_anchor_card(i,j)
                if potential_score in list(temp_dict.keys()):
                    temp_dict[potential_score].append([i,j])
                elif potential_score:
                    temp_dict[potential_score]=[[i,j]]

        if not temp_dict and self.card_hand.get_number_of_cards_in_deck() == 1:
            for j in self.gameboard.get_spots_open_on_board():
                potential_score = self.gameboard.get_score_to_anchor_card(i,j,mercy=True)
                if potential_score in list(temp_dict.keys()):
                    temp_dict[potential_score].append([i,j])
                elif potential_score:
                    temp_dict[potential_score]=[[i,j]]
            if temp_dict:
                self.mercy = True

        


        return temp_dict

    def has_legal_move_left(self):
        if self.possible_move_set():
            print(self.name,"has legal move!")
            return True
        return False

    def has_mercy(self):
        return self.mercy

    def get_all_possible_moves_and_scores_for_cards_not_in_hand(self, by_coordinate=False):
        if by_coordinate:
            temp = {self.gameboard.get_index_by_coordinates(i):None for i in self.gameboard.get_open_spots_legally_playable()}
            for i in temp:
                temp[i] = self.gameboard.get_all_possible_scores_for_open_spot(self.gameboard.get_coordinates_by_index(i),None,self.mercy)
                h=[]
                for j in temp[i]:
                    if j in self.card_hand.deck:
                        h.append(j)
                for k in h:
                    temp[i].pop(k)
            return temp

        temp = {i:None for i in self.gameboard.get_cards_not_on_board()}
        for i in self.card_hand.deck:
            if i in temp:
                temp.pop(i)
        
        for i in temp:
            temp[i] = self.gameboard.get_all_possible_scores_for_card(i,self.mercy)
        return temp





    def get_all_possible_moves_and_scores(self, by_coordinate=False):
        '''
        Returns dict with card object keys and dictionary values. The dictionary keys use an coordinate index and values are the score.
        Essentially, {<card object>: {int coordinate index: int score}}

        If by_coordinate is True:
        {int coordinate index: {<card object>: int score}}
        '''
        
        if by_coordinate:
            temp = {self.gameboard.get_index_by_coordinates(i):None for i in self.gameboard.get_open_spots_legally_playable()}
            for i in temp:
                temp[i] = self.gameboard.get_all_possible_scores_for_open_spot(self.gameboard.get_coordinates_by_index(i),None,self.mercy)
                h=[]
                for j in temp[i]:
                    if j not in self.card_hand.deck:
                        h.append(j)
                for k in h:
                    temp[i].pop(k)
            return temp

        temp = {i:None for i in self.card_hand.deck}
        for i in temp:
            temp[i] = self.gameboard.get_all_possible_scores_for_card(i,self.mercy)
        return temp

    def read_all_moves(self):
        move_set = self.possible_move_set()
        for i in sorted(list(move_set.keys())):
            print(i)
            for j in move_set[i]:
                card = j[0].get_info_color()
                print(card,':',j[1])

    def best_possible_move_set(self,return_score=0):
        '''
        Returns a list of lists in the form of [card, position] for the moves with the
        highest possible score that can be made at that given time.
        '''
        temp_score = 0
        temp_holdings = []
        for i in self.card_hand.get_deck():
            for j in self.gameboard.get_spots_open_on_board():
                check = self.gameboard.get_score_to_anchor_card(i,j) 
                if check > temp_score:
                    temp_score = check
                    temp_holdings=[[i,j]]
                elif check == temp_score:
                    temp_holdings.append([i,j])

        if return_score:
            return temp_score
                    
        return temp_holdings
