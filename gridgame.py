from carddeck import carddeck, card
from gameboard import gameboard
from game_player import game_player

class game():
    def __init__(self,large_board=False):

        num_of_decks = 1
        self.game_board = None


        if large_board:
            num_of_decks = 2
            self.game_board = gameboard(1)
        else:
            self.game_board = gameboard()

        self.game_deck = self.game_board.game_deck
        self.game_deck.master_deck = self.game_deck.find_card(['A','K',1,2,3,4,5],all_instances=True)
        self.game_deck.reset_deck()

        self.kings_deck = carddeck(0,0)
        self.kings_deck.take_card_from_different_deck(self.game_deck,'K',all_instances=1)

        self.game_deck.shuffle_deck()


    def get_random_king(self):
        return self.kings_deck.find_random_card()[0] or card()

    def get_game_deck(self):
        return self.game_deck.get_deck(1)
    
    def shuffle_game_deck(self):
        self.game_deck.shuffle_deck()
        return 1

    def reset_game_deck(self):
        self.game_deck.reset_deck()
        return 1


        
    #def get_random_king(self):

a=game()

print(a.get_game_deck())
print(a.get_random_king().get_info())
print(a.get_game_deck())
