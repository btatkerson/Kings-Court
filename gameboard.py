from carddeck import carddeck, card, random
from time import time

class gameboard():
    def __init__(self, large_board=False):
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

   

    def get_score_to_anchor_card(self, card_in_play=None, x=None, y=None, verbo=False):
        scores = []
        temp_score=0
        if self.is_legal_to_anchor_card(card_in_play, x, y):
            co,x,y = self.verify_coordinate(x,y)
            checkpoint_diff = self.get_card_checkpoint_difference(card_in_play,x,y)
            #print("Check diff", checkpoint_diff)
            if checkpoint_diff == 0:
                temp_score += (self.get_spot_sum_side_cards(x,y)+7)//7*3+1
                scores.append(temp_score)
            elif checkpoint_diff > 0:
                temp_score += -4*checkpoint_diff
                scores.append(temp_score)
            else:
                temp_score += 1
                scores.append(1)
            
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
            match_corner_suit = self.get_corner_suit_chain_total(card_in_play,x,y)

            if verbo:
                print('Place Score',temp_score,'\nMatching trumps', match_trump_suit, '\nMatch corner suit', match_corner_suit,'\nMatch corner val',match_corner_val,'\nMatch col/row val',match_card_val)

            temp_score += match_trump_suit + match_corner_suit + match_card_val*3 + match_corner_val*2

            #print(scores, match_trump_suit, match_card_val*3, match_corner_val*2, match_corner_suit)
            return temp_score
        
        return temp_score



    '''
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
                if direction:
                    if self.get_card_on_spot(spots[direction]).get_suit() == card_in_play.get_suit():
                        return 1 + self.get_corner_suit_chain_total(card_in_play,spots[direction],direction=direction)
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
    '''

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
                    card_val = card_in_play.get_value()
                    for i in self.get_spot_neighbor_cards_sides(x,y):
                        if i.get_value() == card_val:
                            return False
                    return True
        return False

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
        for i in self.game_board:
            for j in i:
                if j == self.get_card_on_spot(self.MIDDLE_GRID_WIDTH_INDEX,self.MIDDLE_GRID_HEIGHT_INDEX):
                    print(j.get_info_color(1) if j else '__', end=' ')
                else:
                    print(j.get_info_color() if j else '__', end=' ')
            print()
        return 0

    def get_card_slots_for_board_x(self):
        x_point_multipliers = [[1,-1],[1,1],[-1,1],[-1,-1]]

        coordinates=[[self.MIDDLE_GRID_WIDTH_INDEX+l[0],self.MIDDLE_GRID_HEIGHT_INDEX+l[1]] for l in [[i*k for k in j] for j in x_point_multipliers for i in range(1,self.MIDDLE_GRID_WIDTH_INDEX+1)]]

        return coordinates

    def set_initial_board(self):
        self.game_deck.shuffle_deck()
        self.set_center_king_card()
        for i in self.get_card_slots_for_board_x():
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
            return self.get_spot_neighbor_cards_corners() + self.get_spot_neighbor_cards_sides()
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

    def get_cards_not_on_board(self):
        return list(set.difference(set(self.game_deck.master_deck),set(self.get_cards_on_board())))

    def get_cards_on_board(self):
        cards_on_board = []
        for i in range(self.MAX_GRID_HEIGHT_INDEX+1):
            for j in self.get_cards_in_row(i):
                cards_on_board.append(j)
        return cards_on_board

    def get_cards_in_row(self, row=None):
        if self.verify_coordinate(y=row):
            temp = []
            for i in range(self.MAX_GRID_WIDTH_INDEX):
                if self.is_spot_occupied(i,row):
                    temp.append(self.get_card_on_spot(i,row))

            return temp

        return []

    def get_cards_in_column(self, column=None):
        if self.verify_coordinate(column):
            temp = []
            for i in range(self.MAX_GRID_HEIGHT_INDEX):
                if self.is_spot_occupied(column,i):
                    temp.append(self.get_card_on_spot(column,i))

            return temp
        return []

    def get_spot_sum_side_cards(self,x=None,y=None):
        co, x, y = self.verify_coordinate(x,y)
        temp_card_list = self.get_spot_neighbor_cards_sides(x,y)
        current_sum = 0
        if temp_card_list:
            for i in temp_card_list:
                if i.get_value()>=10:
                    current_sum += 10
                else:
                    current_sum += i.get_value()+1

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

    def verify_coordinate(self, x=None, y=None):
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



d=carddeck(0,0)
test_deck = carddeck(2,0)
kings_deck = carddeck(0,0)
test_deck.reset_deck()
test_deck.deal_card(test_deck.find_card([6,7,8,9,10,11]))
test_deck.deal_card_to_different_deck(kings_deck,'K',all_instances=1)
test_deck.shuffle_deck()
kings_deck.print_readable_deck()
kings_deck.master_deck=kings_deck.deck
kings_deck.reset_deck()
print('King card',kings_deck.find_random_card()[0].get_info(1))

test_deck.master_deck=test_deck.deck
test_deck.reset_deck()

a = gameboard(0)
print(a.get_dictionary_of_slot_occupants())
a.print_game_board_color()
print()

#a.set_card_on_board(a.game_kings_deck.find_random_card()[0],a.MIDDLE_GRID_WIDTH_INDEX,a.MIDDLE_GRID_HEIGHT_INDEX)

'''
for i in range(a.MAX_GRID_WIDTH_INDEX):
    for j in range(a.MAX_GRID_HEIGHT_INDEX):
        if j == i == a.MIDDLE_GRID_HEIGHT_INDEX:
            pass
        elif a.is_spot_open(i,j):
            temp_card = test_deck.deal_card()[0]
            if a.is_legal_to_anchor_card(temp_card,i,j):
                a.set_card_on_board(temp_card,i,j)
            elif (i,j) == (a.MAX_GRID_WIDTH_INDEX-1,a.MAX_GRID_HEIGHT_INDEX-1):
                break
            else:
                test_deck.take_card(temp_card)
'''

games = 0
timer = time()
tally = {0:0,
         1:0,
         2:0,
         3:0,
         4:0}

while games < 20000:
    games += 1
    while len(a.get_spots_open_on_board())>0:
        spot = a.get_spots_open_on_board()
        dealt = False
        high_score = [-100,None,None]
        temp_hold = None
        breaker = False
        for i in [a.game_deck.deal_card()]:
            temp_hold = i
            for j in spot:
                if i == []:
                    breaker = 1
                    break
                if a.is_legal_to_anchor_card(i[0],j):
                    if a.get_score_to_anchor_card(i[0],j) > high_score[0]:
                        high_score = [a.get_score_to_anchor_card(i[0],j),i[0],j]
        if breaker:
            break
        if high_score == [-100,None,None]:
            pass
        else:
            #a.get_score_to_anchor_card(high_score[1],high_score[2],verbo=True)
            a.set_card_on_board(high_score[1],high_score[2])
            #a.print_game_board_color()
            #print(high_score, high_score[1].get_info(1),high_score[0])
            #input()
    
    tally[len(a.get_spots_open_on_board())] += 1
    #print('spots',a.get_spots_open_on_board())
    #a.print_game_board_color()
    #print('No place:', [k.get_info(1) for k in a.get_cards_not_on_board()])
    #break

    a.reset_game()

timer = time()-timer

print([[a.is_legal_to_anchor_card(i,j) for j in a.get_spots_open_on_board()] for i in a.get_cards_not_on_board()])

print("Games:",games)
print(" Time:",timer)
print("Average game time (games/sec):",games/timer)
print("Tally:", tally)


    

a.print_game_board(1)
print()

a.print_game_board_color()
print() 

print([i.get_info(1) for i in a.get_cards_in_row(0)])
print()

print(a.verify_coordinate(0),[i.get_info(1) for i in a.get_cards_in_column(0)])
print()

print([i.get_info(1) for i in list(set.intersection(set(a.get_cards_in_row(4)),set(a.get_cards_in_column(4))))])
print()

d.master_deck = a.get_cards_in_column(0)
d.reset_deck()

print([i.get_info(1) for i in d.find_card_by_suit(a.get_card_on_spot(4,4).get_suit(),1)])
print('Trump suit', a.get_trump_suit())

for i in range(a.MAX_GRID_HEIGHT_INDEX):
    #print([a.is_spot_with_neighbor(j,i) for j in range(a.MAX_GRID_WIDTH_INDEX)])
    print([1 if a.is_spot_occupied(j,i) else 0 for j in range(a.MAX_GRID_WIDTH_INDEX)],[a.get_spot_number_of_neighbors(j,i) for j in range(a.MAX_GRID_WIDTH_INDEX)],[a.get_spot_anchor_sum(j,i) for j in range(a.MAX_GRID_WIDTH_INDEX)])
    #print([a.is_spot_with_neighbor(j,i) for j in range(a.MAX_GRID_WIDTH_INDEX)])
#print(a.game_board)
print(a.get_card_slots_for_board_x())


