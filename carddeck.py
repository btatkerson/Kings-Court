#!/usr/bin/python3

import time 
import random

from card import card

class cardWithID(card):
    def __init__(self,suit,value,acesHigh):
        card.__init__(self,suit,value,acesHigh)
        self.identity = None
        self.reset_ID()


    def reset_ID(self):
        self.identity = int((time.time()*10**8) % 10**7)

    def get_ID(self):
            return self.identity
    


class carddeck():

    
    def __init__(self,number_of_decks=1, acesHigh=True, five_suits=False):
        self.master_deck = []
        self.acesHigh = acesHigh

        if five_suits:
            self.suitcount = 5
        else:
            self.suitcount = 4

        for k in range(number_of_decks):
            for i in range(self.suitcount):
                for j in range(13):
                    self.master_deck.append(cardWithID(i,j,acesHigh))

        self.deck = []
        self.reset_deck()

    def set_aces_high(self,acesHigh=None):
        if acesHigh == None:
            return None
        elif acesHigh:
            self.acesHigh = True
        else:
            self.acesHigh = False

        for i in self.master_deck:
            i.set_aces_high(self.acesHigh)


    def get_master_deck(self):
        return self.master_deck or []

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def find_card_by_ID(self,ID=None):
        if not ID:
            return None
        else:
            for i in self.deck:
                if i.get_ID() == ID:
                    return i or card()
        return None

    def find_card(self,value=None,suit=None,all_instances=True,list_of_cards=None):
        temp = []
        if suit and value:
            temp = self.find_card_by_suit(suit,list_of_cards=self.find_card_by_value(value,list_of_cards=list_of_cards))

        elif suit and not value:
            temp = self.find_card_by_suit(suit,list_of_cards=list_of_cards)
        
        elif value and not suit:
            temp = self.find_card_by_value(value,list_of_cards=list_of_cards)
        else:
            return []

        if all_instances:
            return temp or []
        elif not all_instances and len(temp) > 0:
            return [temp[0]] or []
        return []

    def find_random_card(self,amount_of_cards=None):
        '''
        Returns a random card, or list of cards, from the deck without removing them
        '''
        if len(self.deck) <= 0:
            return None

        leng = list(range(len(self.deck)))

        random.shuffle(leng)
        temp = []
        if amount_of_cards == None:
            amount_of_cards = 1

        if type(amount_of_cards) == int:
            if amount_of_cards > 1 and len(leng) >= amount_of_cards:
                for i in range(amount_of_cards):
                    temp.append(self.deck[leng[i]])
                return temp or []

        return [self.deck[leng[0]]] or []



                

    def find_card_by_index(self,index=None,list_of_indices=None):
        if not index and not list_of_indices:
            return []

        elif type(list_of_indices) == list or type(index) == list:
            if type(index) == list:
                list_of_indices = index
            index_list = list(set(list_of_indices))
            hold =[]
            for i in index_list:
                if 0 <= i < len(self.deck):
                    hold.append(i)

                    
            return [self.deck[i] for i in hold] or []

        elif 0 <= index < len(self.deck):
            return [self.deck[index]] or []

        return []


        
 
    def find_card_by_value(self,value=None,all_instances=True,list_of_cards=None):
        '''
        value = card value
        all_instances - True returns all cards that match
                    False returns only the first instance
        list_of_cards - When a list is given, this method only searches the 
                        given list instead of the deck (this allows nesting of searches)
        '''

        deck_in_use = None
        if type(list_of_cards) == list:
            deck_in_use = list_of_cards
        else:
            deck_in_use = self.deck


        if value == None:
            return None
        elif type(value) != list:
            value = [value]
        elif type(value) == list:
            value = [str(i).upper() if type(i) == str else i for i in value]
        else:
            return []
        
        
        temp = []
        if all_instances:
            for i in deck_in_use:
                if i.get_value() in value or i.get_value(1) in value:
                    temp.append(i)
            return temp or []
        else:
            for i in deck_in_use:
                if i.get_value() in value or i.get_value(1) in value:
                    return [i] or []

        return temp 

    def find_card_by_suit(self,suit=None,all_instances=True,list_of_cards=None):
        '''
        suit = card suit
        all_instances - True returns all cards that match
                    False returns only the first instance
        list_of_cards - When a list is given, this method only searches the 
                        given list instead of the deck (this allows nesting of searches)
        '''

        deck_in_use = None
        if type(list_of_cards) == list:
            deck_in_use = list_of_cards
        else:
            deck_in_use = self.deck


        if suit == None:
            return None
        elif type(suit) != list:
            suit = [suit]
        elif type(suit) == list:
            suit = [str(i).upper() if type(i) == str else i for i in suit]
        else:
            return []
        
        
        temp = []
        if all_instances:
            for i in deck_in_use:
                if i.get_suit() in suit or i.get_suit(1) in suit:
                    temp.append(i)
            return temp or []
        else:
            for i in deck_in_use:
                if i.get_suit() in suit or i.get_suit(1) in suit:
                    return [i] or []


        return temp

    def reset_deck(self):
        self.deck = list(self.master_deck)

    def get_deck(self,readable=False):
        if readable:
            return [i.get_info(1) for i in self.deck]
        return self.deck

    def print_readable_deck(self):
        '''
        Prints a list to the screen of all the cards in the order they are in the deck
        '''
        for i,j in enumerate(self.get_deck()):
            print(i+1,"\b:",j.get_info(1))


    def deal_card_by_index(self,index=None):
        if self.is_deck_empty():
            return None 

        if type(index) == list:
            hold = []

            for i in sorted(index)[::-1]:
                if 0 <= i < len(self.deck):
                    hold.append(self.deck.pop(i))

            return hold or []

        if 0 <= index < len(self.deck):
            return self.deck.pop(index) or card()

        else:
            return None

    def deal_card(self,list_of_cards=None,number_of_cards=1):
        '''
        deals a card from the deck. This returns a card or list of cards.

        list_of_cards is built to work with self.find_card() in mind. 
        self.find_card returns a list of cards based on input given. 

        Example:

        a = carddeck()
        a.deal_card(a.find_card("A","S")) would return the Ace of Spades
        '''
        if type(list_of_cards) == list:
            temp = []
            index_holder = []

            for i in list_of_cards:
                index_holder.append(self.deck.index(i))

            for i in sorted(index_holder)[::-1]:
                temp.append(self.deck.pop(i))

            
            return temp or [card()]
            

        if self.is_deck_empty():
            return []

        if number_of_cards <= 1:
            return [self.deck.pop()] or []
        else:
            return [self.deck.pop() for i in range(number_of_cards)] or []

    def deal_card_to_different_deck(self, deck=None, value=None, suit=None, list_of_cards=None, all_instances=None):
        '''
        This method is used for dealing a card directly to another deck. This cuts out having
        to write out a.take_card(b.deal_card()) and has built in card-finding if necessary

        Example

        house_deck = carddeck(1)
        player = carddeck(0) # Empty deck

        house_deck.deal_card_to_different_deck(player,"A","S") # passes the Ace of Spades to the player deck
        '''
        if all_instances == None:
            all_instances = False

        if isinstance(deck,carddeck):
            if not self.is_deck_empty():
                if value is not None or suit is not None or type(list_of_cards) is list:
                    if list_of_cards:
                        hold = self.deal_card(list_of_cards)
                    else:
                        hold = self.deal_card(self.find_card(value,suit,all_instances))

                    if list_of_cards:
                        deck.take_card(hold)
                        return 1

                    if len(hold) > 0 and not all_instances:
                        deck.take_card(hold.pop(0))
                        self.take_card(hold)
                        return 1
                    
                    elif hold != []:
                        deck.take_card(hold)
                        return 1
                    else:
                        return 0
                else:
                    deck.take_card(self.deal_card())
                    return 1

        return 0



    def take_card_from_different_deck(self, deck=None, value=None, suit=None, list_of_cards=None, all_instances=None):
        if all_instances == None:
            all_instances = False


        if isinstance(deck,carddeck):
            if not deck.is_deck_empty():
                if value is not None or suit is not None or type(list_of_cards) is list:
                    if list_of_cards:
                        hold = deck.deal_card(list_of_cards)
                    else:
                        hold = deck.deal_card(deck.find_card(value,suit,all_instances))

                    if list_of_cards:
                        self.take_card(hold)
                        return 1


                    if len(hold) > 0 and not all_instances:
                        self.take_card(hold.pop(0))
                        deck.take_card(hold)
                        return 1
                    
                    elif hold != []:
                        self.take_card(hold)
                        return 1
                    else:
                        return 0
                else:
                    self.take_card(deck.deal_card())
                    return 1

        return 0

    def take_card(self,card=None):
        if type(card) == list:
            for i in card:
                self.deck.append(i)
            return 1
        else:
            self.deck.append(card)
            return 1
        0

    def is_deck_empty(self):
        return False if len(self.deck) > 0 else True 

    def card_count_of_deck(self):
        return len(self.deck)

    get_number_of_cards_in_deck=card_count_of_deck

    def sort_deck_by_card_value(self):
        self.deck = sorted(self.deck,key=lambda x: x.get_info(False)[0])

    def sort_deck_by_card_suit(self):
        self.deck = sorted(self.deck,key=lambda x: x.get_info(False)[1])

    def sort_deck_by_card_ID(self):
        self.deck = sorted(self.deck,key=lambda x: x.get_ID())
