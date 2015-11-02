import colorama as col
from termcolor import colored
__author__ = 'benjamin'
class card():

    def __init__(self,suit=None,value=None,acesHigh=False):
        #self.SUITLIST = ["C","D","H","S"]
        self.SUITLIST = ["R","B","G","Y","V"]
        self.VALUELIST = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        self.suit = None
        self.value = None
        self.acesHigh = None
        self.set_suit(suit)
        self.set_value(value)
        self.set_aces_high(acesHigh)

    def get_info(self,readable=True):
        return [self.get_value(readable),self.get_suit(readable)]

    def get_info_color(self,background_highlight=False):
        color_list = [col.Fore.RED, col.Fore.CYAN, col.Fore.GREEN, col.Fore.YELLOW, col.Fore.MAGENTA]
        prop = {0:'1', 12:'0'}[self.get_value()] if self.get_value() in [0,12] else self.get_value(1)
        if background_highlight:
            color_list = [col.Back.RED, col.Back.CYAN, col.Back.GREEN, col.Back.YELLOW, col.Back.MAGENTA]
            
            return col.Fore.BLACK + col.Style.DIM + str(color_list[self.get_suit()] + prop + str(self.get_suit(1))) + col.Style.RESET_ALL

        return color_list[self.get_suit()] + prop + str(self.get_suit(1)) + col.Style.RESET_ALL

    def get_suit(self,readable=False):
        if readable:
            return self.SUITLIST[self.suit]
        return self.suit

    def get_suit_from_index(self,index):
        if index in self.SUITLIST:
            self.SUITLIST.index(index)
        if 0 <= index < len(self.SUITLIST):
            return self.SUITLIST[index]

    def set_suit(self,suit=None):
        if suit:
            if suit in self.SUITLIST:
                self.suit = self.SUITLIST.index(suit)
            elif 0 <= int(suit) < len(self.SUITLIST):
                self.suit = int(suit)
        else:
            self.suit = 0

    def get_value(self,readable=False):
        if readable:
            return self.VALUELIST[self.value]
        if self.acesHigh and self.value == 0:
            return 13
        return self.value

    def get_value_from_index(self, index):
        if index in self.VALUELIST:
            self.VALUELIST.index(index)
        if 0 <= index < len(self.VALUELIST):
            return self.VALUELIST[index]


    def set_value(self,value=None):
        if value:
            if value in self.VALUELIST:
                self.value = self.VALUELIST.index(value)
            elif 0 <= int(value) < len(self.VALUELIST):
                self.value = int(value)
        else:
            self.value = 0

    def is_aces_high(self):
        return self.acesHigh

    def set_aces_high(self,acesHigh=None):
        if not acesHigh:
            self.acesHigh = False
        else:
            self.acesHigh = True

    def toggle_aces_high(self):
        self.acesHigh = not self.acesHigh
