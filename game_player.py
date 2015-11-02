from carddeck import carddeck

class game_player():
    def __init__(self,name=None, human_player=None):
        self.name = None
        self.human_player = True if human_player else False 
        self.score = 0
        self.card_hand = carddeck(0,0)
        

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
                self.score = int(add)
                return 1
            self.score += int(add)
            return 1

        return 0 

    def get_hand(self):
        return self.card_hand

