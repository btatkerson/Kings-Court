import stats
from carddeck import carddeck, card, random
from time import time

class gameboard():
    def __init__(self, large_board=False, gamemode=0):
        self.game_board = []
        self.GRID_SIZE_LARGE = 7
        self.GRID_SIZE_SMALL = 4
        self.EXTRA_SUIT = False

        self.MAX_GRID_HEIGHT_INDEX = None
        self.MIN_GRID_HEIGHT_INDEX = None
        self.MIDDLE_GRID_HEIGHT_INDEX = None

        self.MAX_GRID_WIDTH_INDEX = None
        self.MIN_GRID_WIDTH_INDEX = None
        self.MIDDLE_GRID_WIDTH_INDEX = None

        self.grid_size = self.GRID_SIZE_SMALL
        self.GAMEMODE = gamemode
        
        self.game_deck = carddeck(2,0,self.EXTRA_SUIT)
        self.game_deck.deal_card(self.game_deck.find_card([6,7,8,9,10,11]))
        self.game_kings_deck = carddeck(0,0,self.EXTRA_SUIT)
        self.game_kings_deck.take_card_from_different_deck(self.game_deck,'K',all_instances=1)

        self.game_deck.master_deck = self.game_deck.deck
        self.game_deck.reset_deck()
        self.game_deck.print_readable_deck()

        self.game_kings_deck.master_deck = self.game_kings_deck.deck
        self.game_kings_deck.reset_deck()

        self.trump_suit = 0

        if large_board:
            self.grid_size = self.GRID_SIZE_LARGE

        self.initialize_game_board()

    def set_game_mode(self,gamemode=None):
        if not gamemode:
            self.GAMEMODE = 0
        else:
            self.GAMEMODE = gamemode


    def set_grid_boundaries(self):
        self.MIN_GRID_HEIGHT_INDEX = self.MIN_GRID_WIDTH_INDEX = 0
        self.MAX_GRID_HEIGHT_INDEX = self.MAX_GRID_WIDTH_INDEX = 2*self.grid_size-1
        self.MIDDLE_GRID_HEIGHT_INDEX = self.MIDDLE_GRID_WIDTH_INDEX = int(self.MAX_GRID_HEIGHT_INDEX/2)
    
    def reset_game(self):
        self.game_deck.reset_deck()
        self.initialize_game_board()

        return 1

    def initialize_game_board(self):
        self.set_grid_boundaries()
        self.game_board = []
        for i in range(self.MAX_GRID_HEIGHT_INDEX):
            self.game_board.append([])
            for j in range(self.MAX_GRID_HEIGHT_INDEX):
                self.game_board[i].append(None)

        self.set_initial_board()
        return 1

    def set_card_on_board(self,card_in_play=None,x=None,y=None):
        co, x, y = self.verify_coordinate(x,y)
        if isinstance(card_in_play, card) and co:
            if (x,y) == (self.MIDDLE_GRID_WIDTH_INDEX, self.MIDDLE_GRID_HEIGHT_INDEX):
                self.trump_suit = card_in_play.get_suit()
            self.game_board[y][x] = card_in_play
            return 1

        return 0

   

    def get_score_to_anchor_card(self, card_in_play=None, x=None, y=None, mercy=False, legal_score=False, verbo=False):
        scores = []
        temp_score=0
        if self.is_legal_to_anchor_card(card_in_play, x, y) or mercy:
            if legal_score:
                return True
            co,x,y = self.verify_coordinate(x,y)
            checkpoint_diff = self.get_card_checkpoint_difference(card_in_play,x,y)
            #print("Check diff", checkpoint_diff)
            if checkpoint_diff == 0:
                temp_score += (self.get_spot_sum_side_cards(x,y)+7)//7*7
                scores.append(temp_score)
            elif checkpoint_diff > 0:
                temp_score = -10
                scores.append(temp_score)
            '''
            else:
                temp_score += 1
                scores.append(1)
            '''
            
            card_suit = card_in_play.get_suit()
            card_value = card_in_play.get_value()

            cards_in_col = self.get_cards_in_column(x)
            cards_in_row = self.get_cards_in_row(y)
            cards_on_corner = self.get_spot_neighbor_cards_corners(x,y)

            match_trump_suit = 0
            match_card_val = 0
            match_corner_val = 0
            match_corner_suit = 0

            for i in cards_in_col:
                if i.get_suit() == self.trump_suit:
                    match_trump_suit += 1

                if i.get_value() == card_value:
                    match_card_val += 1

            for i in cards_in_row:
                if i.get_suit() == self.trump_suit:
                    match_trump_suit += 1

                if i.get_value() == card_value:
                    match_card_val += 1

            '''
            for i in cards_on_corner:
                if i.get_suit() == card_suit:
                    match_corner_suit += 1

                if i.get_value() == card_value:
                    match_corner_val += 1
            '''

            match_corner_val = self.get_corner_value_chain_total(card_in_play,x,y)
            match_corner_suit = self.get_corner_suit_chain_total_card_classes(card_in_play,x,y)

            if verbo:
                print('Place Score',temp_score,'\nMatching trumps', match_trump_suit, '\nMatch corner suit', match_corner_suit,'\nMatch corner val',match_corner_val*(card_value+1),'\nMatch col/row val',match_card_val)

            temp_score += match_trump_suit + match_corner_suit + match_card_val*(card_value+1) + match_corner_val*(card_value+1)

            #print(scores, match_trump_suit, match_card_val*3, match_corner_val*2, match_corner_suit)
            '''
            if mercy:
                return temp_score//2
            '''
            return temp_score
        
        if legal_score:
            return False
        return temp_score



    def get_corner_suit_chain_total_card_classes(self, card_in_play=None, x=None, y=None, direction=None):
        co, x, y = self.verify_coordinate(x,y)
        if type(direction) in [int]:
            direction = direction%4
        else:
            direction = None

        if co:
            if self.get_spot_number_of_corner_neighbors(x,y) > 0:
                spots = [[x-1,y-1],
                         [x+1,y-1],
                         [x+1,y+1],
                         [x-1,y+1]]
                
                spots = [self.verify_coordinate(i) for i in spots]
                count = 0
                if direction in [0,1,2,3]:
                    if spots[direction]:
                        temp_card = self.get_card_on_spot(spots[direction][1:3])
                    else:
                        return 0
                    if temp_card:
                        if temp_card.get_suit() == card_in_play.get_suit():
                            if temp_card.get_value() == 12:
                                return 10 + self.get_corner_suit_chain_total_card_classes(card_in_play,spots[direction][1:3],direction=direction)
                            return temp_card.get_value()+1 + self.get_corner_suit_chain_total_card_classes(card_in_play,spots[direction][1:3],direction=direction)
                        else:
                            return 0
                else:
                    for i,j in enumerate(spots):
                        if j != False:
                            temp_card = self.get_card_on_spot(j[1],j[2])
                            if temp_card:
                                if temp_card.get_suit() == card_in_play.get_suit():
                                    if temp_card.get_value() == 12:
                                        count += 10 + self.get_corner_suit_chain_total_card_classes(card_in_play,[j[1],j[2]],direction=i)
                                    else:
                                        count += temp_card.get_value()+1 + self.get_corner_suit_chain_total_card_classes(card_in_play,[j[1],j[2]],direction=i)
                return count

        return 0
 
    def get_corner_suit_chain_total(self, card_in_play=None, x=None, y=None, direction=None):
        co, x, y = self.verify_coordinate(x,y)
        if type(direction) in [int]:
            direction = direction%4
        else:
            direction = None

        if co:
            if self.get_spot_number_of_corner_neighbors(x,y) > 0:
                spots = [[x-1,y-1],
                         [x+1,y-1],
                         [x+1,y+1],
                         [x-1,y+1]]
                
                spots = [self.verify_coordinate(i) for i in spots]
                count = 0
                if direction in [0,1,2,3]:
                    if spots[direction]:
                        temp_card = self.get_card_on_spot(spots[direction][1:3])
                    else:
                        return 0
                    if temp_card:
                        if temp_card.get_suit() == card_in_play.get_suit():
                            return 1 + self.get_corner_suit_chain_total(card_in_play,spots[direction][1:3],direction=direction)
                        else:
                            return 0
                else:
                    for i,j in enumerate(spots):
                        if j != False:
                            temp_card = self.get_card_on_spot(j[1],j[2])
                            if temp_card:
                                if temp_card.get_suit() == card_in_play.get_suit():
                                    count += 1 + self.get_corner_suit_chain_total(card_in_play,[j[1],j[2]],direction=i)
                return count

        return 0
 
                            
    def get_corner_value_chain_total(self, card_in_play=None, x=None, y=None, direction=None):
        co, x, y = self.verify_coordinate(x,y)
        if type(direction) in [int]:
            direction = direction%4
        else:
            direction = None

        if co:
            if self.get_spot_number_of_corner_neighbors(x,y) > 0:
                spots = [[x-1,y-1],
                         [x+1,y-1],
                         [x+1,y+1],
                         [x-1,y+1]]
                
                spots = [self.verify_coordinate(i) for i in spots]
                count = 0
                if direction in [0,1,2,3]:
                    if spots[direction]:
                        temp_card = self.get_card_on_spot(spots[direction][1:3])
                    else:
                        return 0
                    if temp_card:
                        if temp_card.get_value() == card_in_play.get_value():
                            return 1 + self.get_corner_value_chain_total(card_in_play,spots[direction][1:3],direction=direction)
                        else:
                            return 0
                else:
                    for i,j in enumerate(spots):
                        if j != False:
                            temp_card = self.get_card_on_spot(j[1],j[2])
                            if temp_card:
                                if temp_card.get_value() == card_in_play.get_value():
                                    count += 1 + self.get_corner_value_chain_total(card_in_play,[j[1],j[2]],direction=i)
                return count

        return 0
 
            

            

    def is_legal_to_anchor_card(self, card_in_play=None, x=None, y=None):
        co, x, y = self.verify_coordinate(x,y)
        if co:
            if self.is_spot_open(x,y) and self.get_spot_number_of_neighbors(x,y) >= 1:
                if isinstance(card_in_play, card):
                    if self.get_spot_number_of_neighbors(x,y) == 1:
                        for i in self.get_spot_neighbor_cards_all(x,y):
                            if i.get_value() == 12:
                                return False
                    if [x,y] in [[3,4],[4,3],[2,3],[3,2]]:
                        if self.get_spot_number_of_side_neighbors(x,y) != 4:
                            return False

                    card_val = card_in_play.get_value()
                    for i in self.get_spot_neighbor_cards_sides(x,y):
                        if i.get_value() == card_val:
                            return False
                    return True
        return False

    def get_open_spots_legally_playable(self):
        open_spots = self.get_spots_open_on_board()
        legal_spots_to_play = []
        for i in open_spots:
            if i in [[3,4],[4,3],[2,3],[3,2]]:
                if self.get_spot_number_of_side_neighbors(i) == 4:
                    legal_spots_to_play.append(i)
            else:
                neighs = self.get_spot_neighbor_cards_all(i)
                if len(neighs) == 1:
                    if neighs[0].get_value(1) != 'K':
                        legal_spots_to_play.append(i)
                elif len(neighs) > 0:
                    legal_spots_to_play.append(i)


        return legal_spots_to_play

            

    def get_card_checkpoint_difference(self, card_in_play=None, x=None, y=None):
        co, x, y = self.verify_coordinate(x,y)
        if co and self.get_spot_number_of_side_neighbors(x,y) >= 1:
            spot_sum = self.get_spot_sum_side_cards(x,y)%7
            card_val = card_in_play.get_value()+1
            #print("Spot sum/card val", self.get_spot_sum_side_cards(x,y)%7, card_val)
            if spot_sum + card_val > 7:
                return spot_sum + card_val - 7
            elif spot_sum + card_val == 7:
                return 0
        return -1
            

    def get_card_on_spot(self,x=None, y=None):
        co, x, y = self.verify_coordinate(x,y)
        if co:
            if self.game_board[y][x]:
                return self.game_board[y][x]

        return None

    def get_dictionary_of_slot_occupants(self):
        temp_dict = {}
        for i,j in enumerate(self.game_board):
            for k,l in enumerate(j):
                temp_dict[i*7+k]=l
        return temp_dict


    def print_game_board(self, readable=False):
        for i in self.game_board:
            if readable:
                print([j.get_info(1) if j else j for j in i]) 
            else:
                print(i)
        return self.game_board

    def print_game_board_color(self):
        count = 0
        print('  A  B  C  D  E  F  G')
        for i in self.game_board:
            count+=1
            print(count,end=' ')
            for j in i:
                if j == self.get_card_on_spot(self.MIDDLE_GRID_WIDTH_INDEX,self.MIDDLE_GRID_HEIGHT_INDEX):
                    print(j.get_info_color(1) if j else '__', end=' ')
                else:
                    print(j.get_info_color() if j else '__', end=' ')
            print()
        return 0

    def get_card_slots_for_board_x_broken(self):
        '''
        Returns the slots for the board x, but instead of the cards leading from the corners to the king,
        the cards touching the king are in the far cardinal directions.
        '''
        x_point_multipliers = [[1,-1],[1,1],[-1,1],[-1,-1]]

        coordinates=[[0,3],[3,0],[6,3],[3,6]]
        coordinates+=[[self.MIDDLE_GRID_WIDTH_INDEX+l[0],self.MIDDLE_GRID_HEIGHT_INDEX+l[1]] for l in [[i*k for k in j] for j in x_point_multipliers for i in range(2,self.MIDDLE_GRID_WIDTH_INDEX+1)]]

        return coordinates


    def get_card_slots_for_board_x(self):
        x_point_multipliers = [[1,-1],[1,1],[-1,1],[-1,-1]]

        coordinates=[[self.MIDDLE_GRID_WIDTH_INDEX+l[0],self.MIDDLE_GRID_HEIGHT_INDEX+l[1]] for l in [[i*k for k in j] for j in x_point_multipliers for i in range(1,self.MIDDLE_GRID_WIDTH_INDEX+1)]]

        return coordinates

    def get_card_slots_for_board_circle(self):
        coordinates=[[0,3],[3,0],[6,3],[3,6],[0,1],[1,0],[0,5],[1,6],[5,0],[6,1],[6,5],[5,6]]

        return coordinates

    def get_card_slots_for_board_outline(self):
        coordinates=[[0,0],[2,0],[4,0],[6,0],[0, 2],[6, 2],[0,4],[6,4],[0,6],[2,6],[4,6],[6,6]]

        return coordinates

    def get_card_slots_for_board_sides(self):
        coordinates=[[3,0],[2,0],[4,0],[6,3],[0, 2],[6, 2],[0,4],[6,4],[0,3],[2,6],[4,6],[3,6]]

        return coordinates

    def get_card_slots_for_board_diamond(self):
        coordinates=[[1,1],[2,0],[4,0],[5,1],[0, 2],[6, 2],[0,4],[6,4],[1,5],[2,6],[4,6],[5,5]]

        return coordinates

    def get_card_slots_for_board_diamond2(self):
        coordinates=[[3,0],[4,1],[5,2],[6,3],[5,4],[4,5],[3,6],[2,5],[1,4],[0,3],[1,2],[2,1]]

        return coordinates

    def get_card_slots_for_board_corners(self):
        coordinates=[[0,0],[6,0],[6,6],[0,6],[0,1],[1,0],[0,5],[1,6],[5,0],[6,1],[6,5],[5,6]]

        return coordinates

    def get_card_slots_for_board_corners_inverse(self):
        coordinates=[[1,1],[5,1],[5,5],[1,5],[0,1],[1,0],[0,5],[1,6],[5,0],[6,1],[6,5],[5,6]]

        return coordinates


    def set_initial_board(self):
        board_cards = [self.get_card_slots_for_board_x, self.get_card_slots_for_board_x_broken, self.get_card_slots_for_board_circle, self.get_card_slots_for_board_outline, self.get_card_slots_for_board_sides, self.get_card_slots_for_board_diamond, self.get_card_slots_for_board_diamond2, self.get_card_slots_for_board_corners, self.get_card_slots_for_board_corners_inverse][self.GAMEMODE]
        self.game_deck.shuffle_deck()
        self.set_center_king_card()
        for i in board_cards():
            self.set_card_on_board(self.game_deck.deal_card()[0],i)

    def set_center_king_card(self):
        self.set_card_on_board(self.game_kings_deck.find_random_card()[0], self.MIDDLE_GRID_WIDTH_INDEX, self.MIDDLE_GRID_HEIGHT_INDEX)
        return 1

    def get_trump_suit(self):
        return self.trump_suit

    def set_trump_suit(self, suit=None):
        if not suit:
            temp_card = self.get_card_on_spot(self.MIDDLE_GRID_WIDTH_INDEX, self.MIDDLE_GRID_HEIGHT_INDEX)
            if temp_card:
                self.trump_suit = temp_card.get_suit()
                return 1
        elif type(suit) == int:
            self.trump_suit = suit%5 if self.EXTRA_SUIT else suit%4
            return 1
        else:
            self.trump_suit = 0
        return 0

    def get_spot_neighbor_cards_all(self, x=None, y=None):
        if self.verify_coordinate(x,y):
            return self.get_spot_neighbor_cards_corners(x,y) + self.get_spot_neighbor_cards_sides(x,y)
        return None

    def get_spot_number_of_neighbors(self, x=None, y=None):
        if self.verify_coordinate(x,y):
            return 0 + self.get_spot_number_of_corner_neighbors(x,y) + self.get_spot_number_of_side_neighbors(x,y)
        return 0

    def get_spot_number_of_side_neighbors(self, x=None, y=None):
        if self.verify_coordinate(x,y):
            return len(self.get_spot_neighbor_cards_sides(x,y))
        return 0

    def get_spot_number_of_corner_neighbors(self,x=None, y=None):
        if self.verify_coordinate(x,y):
            return len(self.get_spot_neighbor_cards_corners(x,y))
        return 0

    def get_spot_neighbor_cards_sides(self, x=None, y=None):
        if self.verify_coordinate(x,y):
            t,x,y=self.verify_coordinate(x,y)
            min_x = x-1
            max_x = x+1

            min_y = y-1
            max_y = y+1

            spots = [[min_x, y],
                     [max_x, y],
                     [x, min_y],
                     [x, max_y]]

            temp_cards = []

            for i in spots:
                if self.verify_coordinate(i[0],i[1]):
                    if self.is_spot_occupied(i[0],i[1]):
                        temp_cards.append(self.game_board[i[1]][i[0]])

            temp_cards = list(set(temp_cards))
            return temp_cards

        return []

    def get_spot_neighbor_cards_corners(self, x=None, y=None):
        if self.verify_coordinate(x,y):
            t,x,y=self.verify_coordinate(x,y)
            min_x = x-1
            max_x = x+1

            min_y = y-1
            max_y = y+1

            spots = [[min_x, min_y],
                     [max_x, min_y],
                     [min_x, max_y],
                     [max_x, max_y]]

            temp_cards = []

            for i in spots:
                if self.verify_coordinate(i[0],i[1]):
                    if self.is_spot_occupied(i[0],i[1]):
                        temp_cards.append(self.game_board[i[1]][i[0]])

            temp_cards = list(set(temp_cards))
            return temp_cards

        return []

    def is_move_possible(self):
        for i in self.get_cards_not_on_board():
            for j in self.get_spots_open_on_board():
                if self.is_legal_to_anchor_card(i,j):
                    return True
        return False

    def get_card_deck(self):
        return self.game_deck

    def get_cards_not_on_board(self):
        temp_deck = carddeck(0,0,0)
        temp_deck.deck = list(set.difference(set(self.game_deck.master_deck),set(self.get_cards_on_board())))
        temp_deck.sort_deck_by_card_suit()
        temp_deck.sort_deck_by_card_value()
        #temp_deck.print_readable_deck_color()
        return temp_deck.deck

    def get_cards_on_board(self):
        cards_on_board = []
        for i in range(self.MAX_GRID_HEIGHT_INDEX+1):
            for j in self.get_cards_in_row(i):
                cards_on_board.append(j)
        return cards_on_board

    def get_cards_on_board_of_suit(self, suit=None, temp_card=None):
        temp_list=[]

        if isinstance(temp_card, card):
            suit = temp_card.get_suit()

        suit = card().verify_suit(suit)

        if suit is not False:
            for i in self.get_cards_on_board():
                if i.get_suit() == suit:
                    temp_list.append(i)

        return temp_list


    def get_all_possible_scores_for_card(self, card=None, mercy=None):
        if card in self.get_cards_not_on_board():
            return {self.get_index_by_coordinates(i):self.get_score_to_anchor_card(card,i,mercy=mercy) for i in self.get_open_spots_legally_playable() if self.get_score_to_anchor_card(card,i,mercy=mercy,legal_score=1)}

        return {}

    def get_top_scores_for_card(self, card=None, mercy=None, perc=50, by_combination_probability=False):
        if by_combination_probability:
            perc= (7-card.get_info()[0])/7

        all_scores=self.get_all_possible_scores_for_card(card,mercy)
        top_scores = stats.top_percent_of_list(list(all_scores.values()),perc)
        
        scores={}
        for i in top_scores[::-1]:
            for j in all_scores.keys():
                if all_scores[j] == i:
                    scores[j]=i
                    all_scores.pop(j)
                    top_scores.pop()
                    break
            
        return scores


    def get_all_possible_scores_for_open_spot(self, x=None, y=None, mercy=None):
        co, x, y = self.verify_coordinate(x,y)

        if co:
            if [x,y] in self.get_open_spots_legally_playable():
                cards_not_on_board = self.get_cards_not_on_board()
                return {i:self.get_score_to_anchor_card(i,x,y,mercy) for i in cards_not_on_board if self.get_score_to_anchor_card(i,x,y,mercy,1)}
                
        return {}

    def get_top_scores_for_open_spot(self, x=None, y=None, mercy=None, perc=50, by_combination_probability=False):
        if by_combination_probability:
            perc= (7-card.get_info()[0])/7

        all_scores = self.get_all_possible_scores_for_open_spot(x,y,mercy)
        top_scores = stats.top_percent_of_list(list(all_scores.values()),perc)
        
        scores={}
        for i in top_scores[::-1]:
            for j in all_scores.keys():
                if all_scores[j] == i:
                    scores[j]=i
                    all_scores.pop(j)
                    top_scores.pop()
                    break
            
        return scores

       
    def get_average_of_all_possible_scores_for_open_spot(self,x=None, y=None, mercy=None):
        scores = self.get_all_possible_scores_for_open_spot(x,y,mercy)
        if scores:
            return stats.average(scores.values()),scores
        return None,scores

    def get_std_dev_of_all_possible_scores_for_open_spot(self, x=None, y=None, mercy=None):
        average, scores = self.get_average_of_all_possible_scores_for_open_spot(x,y,mercy)
        if scores:
            return stats.std_dev(scores.values(),average), scores
        return None, scores
        
    def get_dict_of_legal_open_spot_side_sums(self, mod=False):
        return {self.get_index_by_coordinates(i):self.get_spot_sum_side_cards(i,mod=mod) for i in self.get_open_spots_legally_playable()}

    def get_average_value_of_cards_on_board_of_suit(self, suit = None, temp_card = None):
        return stats.average([i.get_value()+1 for i in self.get_cards_on_board_of_suit(suit,temp_card)])

    def get_simple_stack_of_cards(self):
        '''
        Returns a single suit stack of every card value possible. This is used for statistical purposes.
        '''
        t_hold = []
        temp_deck = carddeck(0)
        temp_deck.deck = self.get_cards_not_on_board()
        for i in range(6):
            t_card = temp_deck.find_card_by_value(i,0)
            if t_card:
                t_hold.append(t_card[0])


        return t_hold


    def get_open_non_breaking_legal_spots_for_card(self, temp_card=None, scores_included = False):
        if temp_card != None:
            try:
                card_val = temp_card.get_value()
            except AttributeError:
                print("temp_card must be a card class")

        if temp_card in self.get_card_deck().master_deck:
            temp_spots = [self.get_index_by_coordinates(i) for i in self.get_open_spots_legally_playable()]
            mods_dict = {i:self.get_spot_sum_side_cards(self.get_coordinates_by_index(i),mod=True) for i in temp_spots}
            if not scores_included:
                spots = [self.get_coordinates_by_index(i) for i in temp_spots if mods_dict[i] < 7-card_val and self.is_legal_to_anchor_card(temp_card,self.get_coordinates_by_index(i))]
            else:
                spots = {i:self.get_score_to_anchor_card(temp_card,self.get_coordinates_by_index(i)) for i in temp_spots if mods_dict[i] < 7-card_val and self.is_legal_to_anchor_card(temp_card,self.get_coordinates_by_index(i))}

            return spots

    def get_open_checkpoint_legal_spots_for_card(self, temp_card=None, scores_included = False):
        if temp_card != None:
            try:
                card_val = temp_card.get_value()
            except AttributeError:
                print("temp_card must be a card class")

        if temp_card in self.get_card_deck().master_deck: 
            temp_spots = [self.get_index_by_coordinates(i) for i in self.get_open_spots_legally_playable()]
            mods_dict = {i:self.get_spot_sum_side_cards(self.get_coordinates_by_index(i),mod=True) for i in temp_spots}
            if not scores_included:
                spots = [self.get_coordinates_by_index(i) for i in temp_spots if card_val == 6-mods_dict[i] and self.is_legal_to_anchor_card(temp_card,self.get_coordinates_by_index(i))]
            else:
                spots = {i:self.get_score_to_anchor_card(temp_card,self.get_coordinates_by_index(i)) for i in temp_spots if card_val == 6-mods_dict[i] and self.is_legal_to_anchor_card(temp_card,self.get_coordinates_by_index(i))}

            return spots




    def get_spread_of_cards_by_suit(self, suit=None, temp_card=None, vector=False):
        temp_list = self.get_cards_on_board_of_suit(suit,temp_card)
        coords=[]
        for i in temp_list:
            coords.append(self.get_coordinates_by_index(self.get_index_for_card_on_board(i)))

        x_lis = [i[0] for i in coords]
        y_lis = [i[1] for i in coords]

        midpoint = [stats.mean(x_lis), stats.mean(y_lis)]
        std_dev_dir= [stats.std_dev(x_lis), stats.std_dev(y_lis)]
        
        if not vector:
            dis_from_midpoint = [((i[0]-midpoint[0])**2+(i[1]-midpoint[1])**2)**.5 for i in coords]
            mean_distance = stats.mean(dis_from_midpoint)
            std_distance = stats.std_dev(dis_from_midpoint)
            return (mean_distance, std_distance)

        return (midpoint, std_dev_dir)


    def get_cards_on_board_of_value(self, value=None, temp_card=None):
        temp_list=[]

        if isinstance(temp_card, card):
            print("IS INSTANCE")
            value = temp_card.get_value()

        value = card().verify_value(value)

        if value is not False:
            for i in self.get_cards_on_board():
                if i.get_value() == value:
                    temp_list.append(i)

        return temp_list

    def get_spread_of_cards_by_value(self, value=None, temp_card=None, vector=False):
        temp_list = self.get_cards_on_board_of_value(value,temp_card)
        coords=[]
        for i in temp_list:
            coords.append(self.get_coordinates_by_index(self.get_index_for_card_on_board(i)))

        x_lis = [i[0] for i in coords]
        y_lis = [i[1] for i in coords]

        midpoint = [stats.mean(x_lis), stats.mean(y_lis)]
        std_dev_dir= [stats.std_dev(x_lis), stats.std_dev(y_lis)]
        
        if not vector:
            dis_from_midpoint = [((i[0]-midpoint[0])**2+(i[1]-midpoint[1])**2)**.5 for i in coords]
            mean_distance = stats.mean(dis_from_midpoint)
            std_distance = stats.std_dev(dis_from_midpoint)
            return (mean_distance, std_distance)

        return (midpoint, std_dev_dir)

    def get_spots_affected_by_card_play(self, card=None, spot=None, mercy=False):
        co, x, y = self.verify_coordinate(spot)
        if co:
            if self.is_legal_to_anchor_card(card,x,y) or mercy:
                row_spots = self.get_spots_open_in_row(y)
                col_spots = self.get_spots_open_in_column(x)
                cor_suit_spots = []
                cor_value_spots= []

                dir_consts = {0:[-1,-1],1:[1,-1],2:[1,1],3:[-1,1]}
                direction_chains_suit = {i:self.get_corner_suit_chain_total(card,x,y,i) for i in range(4)}

                for i in range(4):
                    shifted = [(direction_chains_suit[i]+1)*dir_consts[i][0]+x, (direction_chains_suit[i]+1)*dir_consts[i][1]+y]
                    if self.verify_coordinate(shifted):
                        if self.is_spot_open(shifted):
                            cor_suit_spots.append(shifted)


                direction_chains_value = {i:self.get_corner_value_chain_total(card, x, y, i) for i in range(4)}
                for i in range(4):
                    shifted = [(direction_chains_value[i]+1)*dir_consts[i][0]+x, (direction_chains_value[i]+1)*dir_consts[i][1]+y]
                    if self.verify_coordinate(shifted):
                        if self.is_spot_open(shifted):
                            cor_value_spots.append(shifted)

                

                # Open spots in the column/row excluding the spot being played
                spots_xy = [k for k in sorted([list(j) for j in list(set([tuple(i) for i in row_spots + col_spots + cor_suit_spots + cor_value_spots]))]) if k != [x,y]]

                return spots_xy

        return []

    def get_cards_in_row(self, row=None):
        if self.verify_coordinate(y=row):
            temp = []
            for i in range(self.MAX_GRID_WIDTH_INDEX):
                if self.is_spot_occupied(i,row):
                    temp.append(self.get_card_on_spot(i,row))

            return temp

        return []

    def get_spots_open_in_row(self, row=None):
        if self.verify_coordinate(row):
            open_spots = self.get_spots_open_on_board()
            row_spots  = []
            for i in open_spots:
                if i[1] == row:
                    row_spots.append(i)

            return row_spots
        return []

    def get_cards_in_column(self, column=None):
        if self.verify_coordinate(column):
            temp = []
            for i in range(self.MAX_GRID_HEIGHT_INDEX):
                if self.is_spot_occupied(column,i):
                    temp.append(self.get_card_on_spot(column,i))

            return temp
        return []

    def get_spots_open_in_column(self, column=None):
        if self.verify_coordinate(column):
            open_spots = self.get_spots_open_on_board()
            column_spots  = []
            for i in open_spots:
                if i[0] == column:
                    column_spots.append(i)

            return column_spots
        return []

    def get_spot_sum_side_cards(self,x=None,y=None, mod=False):
        '''
        Returns the sum of the side cards around any spot.

        mod - Enable if you want the sum returned in mod 7
        '''
        co, x, y = self.verify_coordinate(x,y)
        temp_card_list = self.get_spot_neighbor_cards_sides(x,y)
        current_sum = 0
        if temp_card_list:
            for i in temp_card_list:
                if i.get_value()>=10:
                    current_sum += 10
                else:
                    current_sum += i.get_value()+1

        if mod:
            return current_sum%7

        return current_sum

    def get_spot_anchor_sum(self,x=None,y=None):
        current_sum = self.get_spot_sum_side_cards(x,y)
        co, x, y = self.verify_coordinate(x,y)
        if self.is_spot_occupied(x,y):
            temp = self.game_board[y][x].get_value()
            if temp >= 10:
                temp = 9 
            return current_sum + temp + 1
        return current_sum

    def get_spots_open_on_board(self):
        open_spots = []
        for i in range(self.MAX_GRID_WIDTH_INDEX):
            for j in range(self.MAX_GRID_HEIGHT_INDEX):
                if self.is_spot_open(i,j):
                    open_spots.append([i,j])

        return open_spots

    def get_board_side_length(self):
        return self.GRID_SIZE_LARGE ######################################## FIX THIS SHIT

    def is_spot_with_neighbor(self, x=None, y=None):
        co, x, y = self.verify_coordinate(x,y)
        if co:
            min_x = x-1
            max_x = x+2

            min_y = y-1
            max_y = y+2

            for i in range(min_y,max_y):
                for j in range(min_x,max_x):
                    if (i,j) != (y,x):
                        if self.verify_coordinate(j,i):
                            if self.is_spot_occupied(j,i):
                                return True

        return False

    def is_spot_open(self, x=None, y=None):
        return not self.is_spot_occupied(x,y)

    def is_spot_occupied(self, x=None, y=None):
        co, x, y = self.verify_coordinate(x,y)
        if co:
            if self.game_board[y][x] != None:
                return True
        return False

    def get_index_for_card_on_board(self,card=None):
        if card in self.get_dictionary_of_slot_occupants().values():
            for i in self.get_dictionary_of_slot_occupants().keys():
                if self.get_dictionary_of_slot_occupants()[i] == card:
                    return i
        return None

    def get_index_by_coordinates(self, x=None, y=None):
        co, x, y = self.verify_coordinate(x,y)
        if co:
            return self.MAX_GRID_HEIGHT_INDEX*y+x

    def get_coordinates_by_index(self, index=None):
        if type(index) == int: 
            return [index%self.MAX_GRID_WIDTH_INDEX, index//self.MAX_GRID_HEIGHT_INDEX]
        else:
            return [None, None]


    def verify_coordinate(self, x=None, y=None, index=None):
        if index:
            coords = self.get_coordinates_by_index(index)
            x,y = coords[0], coords[1]
        if x != None and y == None:
            if type(x) == int:
                if self.MIN_GRID_WIDTH_INDEX <= x <= self.MAX_GRID_WIDTH_INDEX-1:
                 return True, int(x)
            elif type(x) in [list,tuple]:
                if [type(i) in [int, float] for i in x] == [True, True]:
                    if self.MIN_GRID_WIDTH_INDEX <= x[0] <= self.MAX_GRID_WIDTH_INDEX-1 and self.MIN_GRID_HEIGHT_INDEX <= x[1] <= self.MAX_GRID_HEIGHT_INDEX-1:
                        return True, int(x[0]), int(x[1])
                    else:
                        return False
            
        elif y != None and x == None:
            if type(y) in [int, float]:
                if self.MIN_GRID_HEIGHT_INDEX <= y <= self.MAX_GRID_HEIGHT_INDEX-1:
                    return True, int(y)

        if not (x or y) and (x != 0 and y != 0):
            return False

        if type(x) in [int, float]:
            if self.MIN_GRID_WIDTH_INDEX <= x and x <= self.MAX_GRID_WIDTH_INDEX-1:
                pass
            else:
                return False
            
        if type(y) in [int, float]:
            if self.MIN_GRID_HEIGHT_INDEX <= y and y <= self.MAX_GRID_HEIGHT_INDEX-1:
                return True, int(x), int(y)

        return False


   
