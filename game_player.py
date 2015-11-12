from carddeck import carddeck
from gameboard import gameboard

class game_player():
    def __init__(self,name=None, human_player=None, main_gameboard=None):
        self.name = None
        self.human_player = True if human_player else False 
        self.last_score = 0
        self.score = 0
        self.card_hand = carddeck(0,0)
        self.gameboard = main_gameboard or gameboard()
        

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
        

    def place_card_on_board(self, card_to_deal=None, position=None):
        if type(card_to_deal) == list:
            card_to_deal = card_to_deal[0]

        if self.gameboard.is_legal_to_anchor_card(card_to_deal, position):
            self.last_score = self.score
            self.score += self.gameboard.get_score_to_anchor_card(card_to_deal,position)
            self.card_hand.deal_card([card_to_deal])
            self.gameboard.set_card_on_board(card_to_deal,position)
            return 1
        else:
            return 0


    def best_possible_move_set(self):
        '''
        Returns a list of lists in the form of [card, position]
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
                    
        return temp_holdings

