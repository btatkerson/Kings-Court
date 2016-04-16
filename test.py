from PyQt4 import QtCore, QtGui
import gameboard
import carddeck
import game_player
import random
import sys

class AppWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AppWidget, self).__init__(parent)
        self.setWindowTitle('King\'s Court')
        self.gamemode = 1
        self.player_count = 4
        self.color_style=['color: rgb(175,0,0);', 'color: rgb( 25, 117, 209);', 'color: rgb(25, 117, 25);', 'color: rgb(153, 153, 0);']
        self.players = []
        self.setGeometry(0,0,825,768)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.player_side_widget = []
        self.sidepanel=None

        self.gameboardGraphicView = QtGui.QGraphicsView()
        self.gameboardGraphicScene = main_game(self.player_count,self) 
        #self.gameboardGraphicScene.setSceneRect(-100,-8,640,656)
        
        game_setup_dialog(self).exec_()
        if self.setup_player_widgets(self.gameboardGraphicScene.get_players()):
            for i in self.gameboardGraphicScene.get_players():
                print(i.get_name())
            self.sidepanel=player_side_panel_widget(self.player_side_widget,parent=self)
            self.sidepanel.setMaximumHeight(600)

    
        self.gameboardGraphicView.setScene(self.gameboardGraphicScene)
        self.gameboardGraphicView.setGeometry(0,0,700,656)
        self.gameboardGraphicView.setFrameRect(QtCore.QRect(0,0,700,600))
        self.gameboardGraphicView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gameboardGraphicView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

                
        #self.gameboardGraphicScene.addItem(self.testRect)
        #self.gameboardGraphicScene.addItem(self.testRect2)
        print(self.gameboardGraphicScene.get_coordinate_dictionary_for_board())

        # set style change handler
        self.horizontalLayout.addWidget(self.sidepanel)
        self.horizontalLayout.addWidget(self.gameboardGraphicView)
        self.gameboardGraphicScene.layout_board()
        self.setLayout(self.horizontalLayout)
        self.gameboardGraphicScene.reset_game()

    # handler for changing style
    def handleStyleChanged(self, style):
        QtGui.qApp.setStyle(style)

    def dragLeaveEvent(self):
        pass

    def setup_player_widgets(self,players=None):
        if self.player_count > 0:
            for i in range(self.player_count):
                self.player_side_widget.append(player_score_widget(self.players[i],self.color_style[i],self))
                self.player_side_widget[i].update_scores()
            return 1
        return 0


class player_side_panel_widget(QtGui.QWidget):
    def __init__(self,player_widgets=None,parent=None):
        QtGui.QWidget.__init__(self,parent=parent)
        self.parent=parent
        self.vlay = QtGui.QVBoxLayout()
        self.player_widgets = player_widgets
        self.reset_button = QtGui.QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        size_pol_reset_butt = QtGui.QSizePolicy()
        size_pol_reset_butt.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
        size_pol_reset_butt.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
        self.reset_button.setSizePolicy(size_pol_reset_butt)
        self.score_widgets = QtGui.QWidget(self)
        self.score_widget_layout = QtGui.QVBoxLayout(self)
        self.score_widgets.setLayout(self.score_widget_layout)
        if player_widgets:
            for i in player_widgets:
                self.score_widget_layout.addWidget(i)

        self.score_widgets.setMinimumHeight(self.parent.height()/1.5)
        self.vlay.addWidget(self.score_widgets)
        self.vlay.addWidget(self.reset_button)
        self.vlay.setAlignment(QtCore.Qt.AlignVCenter)
        size_policy = QtGui.QSizePolicy()
        size_policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
        self.score_widgets.setSizePolicy(size_policy)
        self.setLayout(self.vlay)
        self.setMaximumWidth(160)


        print('Width self/reset/scores', self.width(), self.reset_button.width(), self.score_widgets.width())
        self.show()
    
    def update_all(self):
        for i in self.player_widgets:
            i.update_scores()

    def reset_game(self,e):
        if not reset_game_verification(self.parent).exec_():
            return 0
        self.parent.gameboardGraphicScene.reset_game()
        players = self.parent.gameboardGraphicScene.player
        for x,y in enumerate(self.player_widgets):
            y.set_player(players[x])


class game_setup_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent=parent)

        if parent:
            self.parent = parent
            self.player_count = self.parent.player_count
        else:
            self.player_count = 2

        self.players = self.parent.players

        if len(self.players) == self.player_count:
            self.players = [player_setup_options(i,self) for i in self.players]
        elif len(self.players) > self.player_count:
            while len(self.players) != self.player_count:
                self.players.pop()
            self.players = [player_setup_options(i,self) for i in self.players]
        else:
            self.players = [player_setup_options(i,self) for i in self.players]
            while len(self.players) != self.player_count:
                self.players.append(player_setup_options(player=game_player.game_player(name='Player',human_player = False, main_gameboard=self.parent.gameboardGraphicScene.main_board)))
            

        self.generic_names = ['Harland', 'Cool Pat', 'Nancy', 'Dr. Spaceman', 'Oscar', 'Rex', 'La Porsha']
        self.generic_names = ['Lynette', 'Gabby', 'Bree', 'Susan', 'Bear', 'Dodd', 'Rye','Hanzee','Lou','Homer','Bart','Lisa','Marge']
        random.shuffle(self.generic_names)
        for i in range(1,len(self.players)):
            self.players[i].player.set_name(self.generic_names[i])
            self.players[i].player.set_human(False)
            self.players[i].update_widget_to_player_stats()
            

        self.players[0].update_widget_to_player_stats()
        self.players[0].human_or_computer_combo.setCurrentIndex(1)
        self.players[0].human_or_computer_combo.setDisabled(True)


        self.vbox = QtGui.QVBoxLayout(self)

        self.game_mode_widget_layout = QtGui.QHBoxLayout(self)
        self.game_mode_widget=QtGui.QWidget(self)
        self.game_mode_widget.setLayout(self.game_mode_widget_layout)
        self.game_mode_label = QtGui.QLabel("Initial Board:",self)
        self.game_mode_spinner = QtGui.QComboBox(self)
        self.game_mode_spinner.addItem("1: X-Board")
        self.game_mode_spinner.addItem("2: Snowflake")
        self.game_mode_spinner.addItem("3: Round Square")
        self.game_mode_spinner.addItem("4: Outside Border")
        self.game_mode_spinner.addItem("5: Sides")
        self.game_mode_spinner.addItem("6: Diamond")
        self.game_mode_spinner.addItem("7: Corners")
        self.game_mode_spinner.addItem("8: Inverse Corners")
        self.game_mode_spinner.setCurrentIndex(1)

        self.game_mode_widget_layout.addWidget(self.game_mode_label)
        self.game_mode_widget_layout.addWidget(self.game_mode_spinner)

        self.vbox.addWidget(self.game_mode_widget)

        for i in self.players:
            self.vbox.addWidget(i)

        self.update_players()
        
    def closeEvent(self,e=None):
        self.update_players()
        self.parent.gamemode = self.game_mode_spinner.currentIndex()


        

    def update_players(self,e=None):
        for i in self.players:
            i.update_player()

        player_list = [i.get_player() for i in self.players]
        
        print('players update',player_list[0].get_name())

        self.parent.players=player_list





    

class player_setup_options(QtGui.QWidget):
    def __init__(self, is_human=None, player=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if parent:
            self.parent = parent

        if player:
            self.player = player
        else:
            self.player = game_player.game_player("Player",0)

        self.hbox = QtGui.QHBoxLayout(self)
        
        self.human_or_computer_combo = QtGui.QComboBox(self)
        self.human_or_computer_combo.addItem("None")
        self.human_or_computer_combo.addItem("Human")
        self.human_or_computer_combo.addItem("Computer")
        self.human_or_computer_combo.setCurrentIndex(1)


        self.player_name_text_edit = QtGui.QLineEdit(player.get_name() if player else "Player", self)
        self.player_level_label = QtGui.QLabel("AI Level:")
        self.player_level_spin = QtGui.QSpinBox(self)
        self.player_level_spin.setMinimum(1)
        self.player_level_spin.setMaximum(5)
        self.player_level_spin.setWrapping(True)
        self.player_level_spin.setValue(player.get_computer_level() if player else 3)

        if self.player.is_human():
            self.human_or_computer_combo.setCurrentIndex(2)
            self.human_or_computer_combo.setEnabled(True)
            self.player_level_spin.setDisabled(True)
        else:
            self.human_or_computer_combo.setCurrentIndex(3)
            self.player_level_spin.setEnabled(True)



        self.hbox.addWidget(self.human_or_computer_combo)
        self.hbox.addWidget(self.player_name_text_edit)
        self.hbox.addWidget(self.player_level_label)
        self.hbox.addWidget(self.player_level_spin)

        self.setLayout(self.hbox)



        self.update_player()

    def update_widget_to_player_stats(self):
        self.player_name_text_edit.setText(self.player.get_name())
        self.player_level_spin.setValue(self.player.get_computer_level())
        if self.player.is_human():
            self.player_level_spin.setDisabled(True)
        self.human_or_computer_combo.setCurrentIndex(2 if self.player.is_computer() else 1)


    def update_player(self):
        self.player.set_name(self.player_name_text_edit.text())
        self.player.set_computer_level(self.player_level_spin.value())
        self.player.set_human(True if self.human_or_computer_combo.currentIndex() == 1 else False)

    def get_player(self):
        return self.player




        



        
        


class reset_game_verification(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent=parent)

        if parent:
            self.parent = parent

        self.veri_layout = QtGui.QVBoxLayout(self)
        self.veri_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.button_layout = QtGui.QHBoxLayout(self)
        self.button_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.setWindowTitle('Reset Game?')

        self.message = QtGui.QLabel("Do you really want to reset the game?",self)
        self.message_style = QtGui.QFont()
        self.message_style.setPointSize(14)
        self.message.setFont(self.message_style)
        self.message.setAlignment(QtCore.Qt.AlignCenter)

        self.button_widget = QtGui.QWidget(self)
        #self.button_widget.setMaximumWidth(250)
        self.button_widget.setLayout(self.button_layout)
        self.confirm_button = QtGui.QPushButton('Yes',self)
        self.confirm_button.clicked.connect(self.confirm_reset)
        self.deny_button = QtGui.QPushButton('No',self)
        self.deny_button.clicked.connect(self.deny_reset)


        self.button_layout.addWidget(self.confirm_button)
        self.button_layout.addWidget(self.deny_button)

        self.veri_layout.addWidget(self.message)
        self.veri_layout.addWidget(self.button_widget)
        self.setFixedSize(300,125)
        self.setLayout(self.veri_layout)


    def confirm_reset(self,e=None):
        self.done(1)

    def deny_reset(self, e=None):
        self.done(0)


class player_score_widget(QtGui.QWidget):
    def __init__(self,player=None,colorStyle=None,parent=None):
        QtGui.QWidget.__init__(self,parent=parent)
        self.setWindowTitle("Reset the game?")
        self.vbox=QtGui.QVBoxLayout()
        self.player=player
        self.player_name_label = QtGui.QLabel(parent=self)
        self.player_name_label.setMaximumHeight(30)
        if colorStyle:
            self.player_name_label.setStyleSheet(colorStyle)
        else:
            self.player_name_label.setStyleSheet('color: rgb(0,120,100);')
        self.player_name_label_font = QtGui.QFont()
        self.player_name_label_font.setPointSize(14)
        self.player_name_label_font.setBold(True)
        self.player_name_label.setFont(self.player_name_label_font)

        self.player_score = QtGui.QLabel(parent=self)
        self.player_score_font = QtGui.QFont()
        self.player_score_font.setPointSize(12)
        self.player_score_font.setBold(True)
        #self.player_score.setStyleSheet('color: rgb(0,120,100);')
        self.player_score.setFont(self.player_score_font)

        self.vbox.addWidget(self.player_name_label)
        self.vbox.addWidget(self.player_score)
        self.setLayout(self.vbox)
        self.update_scores()
        self.setMaximumHeight(60)


    def set_player(self,player=None):
        if player:
            self.player=player
            self.player_name_label.setText(self.player.get_name())
            self.update_scores()

    def update_scores(self):
        self.player_name_label.setText("<center>"+str(self.player.get_name())+"</center>")
        self.player_score.setText("<center>"+str(self.player.get_score())+"</center>")    
        



class game_board_background(QtGui.QGraphicsItemGroup):
    def __init__(self, parent=None, scene=None):
        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        '''
        background_rect = QtGui.QGraphicsRectItem()
        background_rect.setBrush(QtGui.QBrush(QtGui.QColor(80,45,0)))
        background_rect.setRect(0,0,64*7+8*8,64*7+8*8)
        '''
        background_pix = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('./cards/gameboard.png'),scene)
        background_pix = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('./cards/gameboard_colored_bigger.png'),scene)
        background_pix.setX(-16)
        background_pix.setY(-16)
        self.addToGroup(background_pix)

        #self.addToGroup(background_rect)

class player_card_dock(QtGui.QGraphicsItemGroup):
    def __init__(self, player=None, parent=None, scene=None):
        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        self.scene = scene
        self.parent = parent
        self.setHandlesChildEvents(False)

        self.set_player(player)
        self.player_deck = []

        self.card_dock_back = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('./cards/small_dock.png'),self,self.scene)
        self.card_dock_back.setX(-16)
        self.addToGroup(self.card_dock_back)

        '''
        self.card_dock_back = QtGui.QGraphicsRectItem()
        self.card_dock_back.setBrush(QtGui.QBrush(QtGui.QColor(100,75,0,0)))

        self.card_dock_back.setRect(0,0,64*8,64*2)

        self.addToGroup(self.card_dock_back)
        '''

        self.top_row = [(64*7-8)/9*i+24 for i in range(9)]
        self.bott_row = [(64*7-8)/9*i+32 for i in range(9)]
        self.top_y = 8 
        self.mid_y = 40
        self.bott_y = 56

        self.update_dock()

    '''
        if player:
            player_deck = self.player.card_hand.get_deck() or game_player.game_player()
            sorter=carddeck.carddeck(0)
            sorter.deck=player_deck
            sorter.sort_deck_by_card_suit()
            sorter.sort_deck_by_card_value()
            player_deck=sorter.deck
            player_deck = [playing_card_graphic(card=i, dock=self, scene=scene) for i in player_deck]
            

            count = 0
            for i in player_deck:
                i.set_click_on()
                if count < 9:
                    i.setX(self.top_row[count])
                    i.setY(self.top_y)
                    i.setZValue(count)
                else:
                    i.setX(self.bott_row[count%9])
                    i.setY(self.bott_y)
                    i.setZValue(count)

                print(i.get_card_class().get_info(1),i.zValue())
                count += 1
                self.addToGroup(i)

    '''
    def update_dock(self):
        if self.player:
            for i in self.player_deck:
                self.scene.removeItem(i)
            
        player_deck = self.player.card_hand.get_deck() 
        if not len(player_deck):
            return 1
        sorter=carddeck.carddeck(0)
        sorter.deck=player_deck
        sorter.sort_deck_by_card_suit()
        sorter.sort_deck_by_card_value()
        player_deck=sorter.deck
        player_deck = [playing_card_graphic(card=i, dock=self, parent=self.card_dock_back,scene=self.scene) for i in player_deck]
        self.player_deck = player_deck
        length_deck = len(player_deck)
        
        
        count = 0
        for i in player_deck:
            i.set_click_on()
            if count < 9:
                i.setX(self.top_row[count])
                if length_deck <= 9:
                    i.setY(self.mid_y)
                else:
                    i.setY(self.top_y)
                i.setZValue(count)
            else:
                i.setX(self.bott_row[count % 9])
                i.setY(self.bott_y)
                i.setZValue(count)
        
            count += 1
            self.addToGroup(i)

    def set_player(self,player=None):
        if player:
            self.player = player
        else:
            self.player = game_player.game_player()
        

                


class main_game(QtGui.QGraphicsScene):
    def __init__(self, player_count=None, parent=None):
        QtGui.QGraphicsScene.__init__(self,parent)
        self.parent=parent
        
        self.background_image = QtGui.QImage('./cards/green_background.png')
        self.background_image_brush = QtGui.QBrush(self.background_image)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0,90,20)))
        self.setBackgroundBrush(self.background_image_brush)
        self.main_board = gameboard.gameboard(0,2)
        self.main_board.game_deck.get_deck(1)
        self.player = []
        self.player_turn = 0
        #self.setup_players(player_count)
        self.player_count = len(self.player)


        self.cards_on_board_dictionary={i:None for i in range(self.main_board.get_board_side_length())}
        self.background = game_board_background()
        self.background.setX(0)
        self.background.setY(0)
        self.background.setZValue(100)

        self.card_dock = player_card_dock(scene=self)
        self.card_dock.setY(64*8+8*3)
        self.card_dock.setZValue(200)
        self.setSceneRect(QtCore.QRectF(0,0,512,650))

        self.addItem(self.background)
        self.addItem(self.card_dock)

    def dragLeaveEvent(self):
        pass


    def get_players(self):
        return self.player

    def computer_turns(self):
        self.player_turn=self.player_turn%self.player_count
        if self.player[self.player_turn].is_human():
            self.card_dock.set_player(self.player[self.player_turn])
            self.card_dock.update_dock()
            return 0
        else:
            while self.player[self.player_turn].is_computer():
                comp_move=self.player[self.player_turn].get_computer_move()
                print('comp_move',comp_move)
                if not comp_move: 
                    self.player_turn=(self.player_turn+1) % self.player_count
                else:
                    self.player[self.player_turn].set_score(self.main_board.get_score_to_anchor_card(comp_move[0],comp_move[1],mercy=self.player[self.player_turn].has_mercy()))
                    self.main_board.set_card_on_board(comp_move[0],comp_move[1])
                    self.player[self.player_turn].card_hand.deal_card([comp_move[0]])
                    self.player_turn=(self.player_turn+1) % self.player_count
                    self.player_turn=self.player_turn % self.player_count
                    if self.player_turn == 0:
                        self.player[self.player_turn].read_all_moves()
                    self.layout_board()

                for i in range(5):
                    QtGui.QApplication.processEvents()

            for i in self.player:
                sorter=carddeck.carddeck(0)
                sorter.deck=i.card_hand.get_deck()
                sorter.sort_deck_by_card_suit()
                sorter.sort_deck_by_card_value()
                print(i.get_name(),"hand:",sorter.get_deck(1))

            if self.player[self.player_turn].is_human():
                self.card_dock.set_player(self.player[self.player_turn])
                self.card_dock.update_dock()
                return 0



    def print_player_scores(self):
        for i in range(self.player_count):
            print('Player',i+1,'\b:',self.player[i].get_score())
            

    def setup_players(self,player_count=None):
        '''
        if player_count != None:
            self.player = [game_player.game_player("Player "+str(i+1),0,self.main_board) for i in range(player_count)]
        else:
            self.player = [game_player.game_player("Player "+str(i+1),0,self.main_board) for i in range(2)]
        '''
        self.player = self.parent.players
        print("Player_count!", len(self.player))
        for i in self.player:
            i.reset_player_hand_and_score()
        self.player_turn=0
        self.player_count = len(self.player)
        self.card_dock.set_player(self.player[0])

        count = 0
        print('full deck',self.main_board.game_deck.get_deck(1))
        print('len full deck',len(self.main_board.game_deck.get_deck(1)))
        while not self.main_board.game_deck.is_deck_empty():
            dealt=self.main_board.game_deck.deal_card()[0]
            print("dealt",dealt)
            self.player[count % self.player_count].card_hand.take_card(dealt)
            count += 1
        print('Player count', len(self.player))
        for i in self.player:                
            sorter=carddeck.carddeck(0)
            sorter.deck=i.card_hand.get_deck()
            sorter.sort_deck_by_card_suit()
            sorter.sort_deck_by_card_value()
            print(i.get_name(),"hand:",sorter.get_deck(1))



        self.player[0].set_human(1)

    def get_coordinate_dictionary_for_board(self):
        board_length = self.main_board.get_board_side_length()
        piece_width = 64
        spacer = 8
        coordinates = {}
        for i in range(0,int(board_length**2)):
            coordinates[i]=[i % board_length*(piece_width+spacer)+spacer, i//board_length*(piece_width+spacer)+spacer]
        return coordinates

    def drop_card_on_board(self, card, player=None):
        x=card.x()
        y=card.y()
        print("final x,y location",x,y)
        coord_dict = self.get_coordinate_dictionary_for_board()
        temp_dict = {}
        if self.player[self.player_turn] != player:
            return 0

        for i in coord_dict.keys():
            temp_dict[i] = ((coord_dict[i][0]-x)**2+(coord_dict[i][1]-y)**2)**.5

        smallest = [temp_dict[0],0]
        for i in temp_dict.keys():
            if temp_dict[i] < smallest[0]:
                smallest = [temp_dict[i],i]

        player.possible_move_set()
                
        if (self.main_board.is_legal_to_anchor_card(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1])) or player.has_mercy()) and smallest[0] < 20:
            print('Card set!')
            card.setX(coord_dict[smallest[1]][0])
            card.setY(coord_dict[smallest[1]][1])
            print('smallest',smallest[1])
            print('coords:',self.main_board.get_coordinates_by_index(smallest[1]))
            print("Score of drop",self.main_board.get_score_to_anchor_card(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1])))
            if player:
                player.set_score(self.main_board.get_score_to_anchor_card(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1]),mercy=player.has_mercy(),verbo=1))
                print("Player Score: ",player.get_score())
            print(self.main_board.set_card_on_board(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1])))
            card.set_click_off()
            player.get_hand().deal_card([card.get_card_class()])
            self.card_dock.update_dock()
            self.player_turn+=1
            self.layout_board()
            return 1
        else:
            old_pos = card.old_position
            card.setX(old_pos[0])
            card.setY(old_pos[1])
            return 0


    def layout_board(self):
        cards_on_table = self.main_board.get_dictionary_of_slot_occupants()
        coordinates = self.get_coordinate_dictionary_for_board()
        for i in cards_on_table:
            if cards_on_table[i]:
                card_info = cards_on_table[i].get_info(0)
                if card_info[0] == 12:
                    card_info[0] = -1
                #self.cards_on_board_dictionary[i] = playing_card_graphic(card_info[1],card_info[0]+1,scene=self)
                self.cards_on_board_dictionary[i] = playing_card_graphic(card=cards_on_table[i],scene=self)
                self.cards_on_board_dictionary[i].setX(coordinates[i][0])
                self.cards_on_board_dictionary[i].setY(coordinates[i][1])
                self.cards_on_board_dictionary[i].setZValue(i+100)
                #if i % 2 == 0:
                self.cards_on_board_dictionary[i].set_click_off()
                self.addItem(self.cards_on_board_dictionary[i])
        self.parent.sidepanel.update_all()

    def reset_game(self):
        print("------------------------------------------\n",self.cards_on_board_dictionary.items())

        '''                                                                                Add option to set the gamemode!!      ##########'''
        self.main_board.set_game_mode(self.parent.gamemode)

        self.main_board.reset_game()

        for i in self.items():
            if isinstance(i,playing_card_graphic):
                self.removeItem(i)
            
        self.setup_players(self.player_count)
        self.card_dock.player=self.player[0]
        self.card_dock.update_dock()
        self.layout_board()


        
class playing_card_graphic(QtGui.QGraphicsItem):
    def __init__(self, suit=0, value=0,card=None, dock=None,parent=None,scene=None):
        if card:
            self.card = card
            card_info = self.card.get_info(0)
            if card_info[0] == 12:
                value = 0
            else:
                value = card_info[0]+1
            suit = card_info[1]
        
        if dock:
            self.dock = dock or player_card_dock()
            self.player = self.dock.player
        else:
            self.dock = None

        QtGui.QGraphicsItem.__init__(self,parent,scene)
        self.top_scene = scene
        self.click_disabled = False
        self.suit = suit % 5
        red = QtGui.QColor(175,0,0)
        blue = QtGui.QColor(48,89,214)
        blue = QtGui.QColor(25,117,209)
        green = QtGui.QColor(0,164,0)
        green = QtGui.QColor(25,117,25)
        #green = QtGui.QColor(48,131,48)
        #green = QtGui.QColor(0,255,0)
        yellow = QtGui.QColor(192,200,0)
        yellow = QtGui.QColor(153,153,0)
        violet = QtGui.QColor(92,0,230)
        self.suit_color=[QtCore.Qt.red, QtCore.Qt.darkCyan, QtCore.Qt.green, QtCore.Qt.yellow]

        '''
        self.back_pix_maps=[QtGui.QPixmap('./cards/card_template_red_square.png'),
                            QtGui.QPixmap('./cards/card_template_blue_square.png'),
                            QtGui.QPixmap('./cards/card_template_green_square.png'),
                            QtGui.QPixmap('./cards/card_template_yellow_square.png'),
                            QtGui.QPixmap('./cards/card_template_violet_square.png')]
        '''

        self.back_pix_maps=[QtGui.QPixmap('./cards/card_template_red_square_round2.png'),
                            QtGui.QPixmap('./cards/card_template_blue_square_round2.png'),
                            QtGui.QPixmap('./cards/card_template_green_square_round2.png'),
                            QtGui.QPixmap('./cards/card_template_yellow_square_round2.png'),
                            QtGui.QPixmap('./cards/card_template_violet_square_round2.png')]



        self.suit_color=[red,blue,green,yellow,violet]
        '''
        self.background = QtGui.QGraphicsRectItem(0,0,64,64,self)
        self.background.setBrush(QtGui.QBrush(self.suit_color[self.suit]))
        '''
        self.background = QtGui.QGraphicsPixmapItem(self)
        self.background.setPixmap(self.back_pix_maps[self.suit])

        #self.whiteLayerBackground = QtGui.QGraphicsRectItem(8,8,48,48,self)
        #self.whiteLayerBackground.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.number = QtGui.QGraphicsTextItem(str(value),self)
        self.number.setDefaultTextColor(self.suit_color[self.suit])
        self.number.setX(17)
        self.number.setY(5)
        self.font = QtGui.QFont('Ubuntu Mono',36,1)
        self.number.setFont(self.font)
        self.setAcceptHoverEvents(True)
        self.old_position = [self.x(),self.y(),self.zValue()]

    def get_card_class(self):
        return self.card

    def set_click_off(self):
        self.click_disabled = True

    def set_click_on(self):
        self.click_disabled = False

    def boundingRect(self):
        return QtCore.QRectF(0,0,64,64)

    def hoverEnterEvent(self, event):
        if self.click_disabled:
            return
        cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)
        QtGui.QApplication.instance().setOverrideCursor(cursor)

    def hoverLeaveEvent(self,event):
        QtGui.QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self,event):
        if self.click_disabled:
            return
        new_position = event.scenePos()

        #old_position = self.scenePos()
        #new_position.setY(old_position.y())
        self.setX(new_position.x()-32)
        self.setY(new_position.y()-568)
        self.setZValue(200)
        self.show()

    def mousePressEvent(self, event): 
        if self.click_disabled:
            return
        self.old_position = [self.x(),self.y(),self.zValue()]
        self.setZValue(200)
        new_position = event.scenePos()
        print(new_position)
        self.setX(new_position.x()-32)
        self.setY(new_position.y()-568)
        self.show()

    def mouseReleaseEvent(self, event): 
        if self.click_disabled:
            return
        self.setZValue(200)
        pos = event.scenePos()
        self.setX(pos.x()-32)
        self.setY(pos.y()-32)
        
        if self.top_scene:
            print('top_scene')
            if self.top_scene.drop_card_on_board(self,self.player) == 1:
                self.hide()
                for i in range(5):
                    QtGui.QApplication.processEvents()

                self.top_scene.computer_turns()
                self.top_scene.print_player_scores()
            else:
                self.setX(self.old_position[0])
                self.setY(self.old_position[1])
                self.setZValue(self.old_position[2])

        print('final_pos',pos.x(),pos.y())

    def get_card(self):
        return self
        


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    widgetApp = AppWidget()
    widgetApp.show()
    sys.exit(app.exec_())
