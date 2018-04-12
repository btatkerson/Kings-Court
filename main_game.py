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
        self.showMaximized()
        self.show()
        self.mainMenuBar = QtGui.QMenuBar(self)
        self.initialSetup = True
        self.closeEarly = True
        self.closeOut = False
        print('C Early Status =', self.closeEarly)
        self.gamemode = -1
        self.player_count = 4
        self.max_card = -1
        self.max_card_ind = -1
        self.color_style=['color: rgb(175,0,0);', 'color: rgb( 25, 117, 209);', 'color: rgb(25, 117, 25);', 'color: rgb(153, 153, 0);']
        self.players = []
        self.setGeometry(0,0,825,768)
        self.setMinimumHeight(728)
        #self.setMinimumWidth(752)
        self.setMinimumWidth(968)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.player_side_widget = []
        self.sidepanel=None

        self.gameboardGraphicView = QtGui.QGraphicsView(self)
        self.gameboardGraphicView.setMinimumWidth(580)
        self.gameboardGraphicScene = main_game(self.player_count,self) 
        #self.gameboardGraphicScene.setSceneRect(-100,-8,640,656)
        
        self.game_setup_dialog_window()

        '''
        if self.setup_player_widgets(self.players):
            for i in self.gameboardGraphicScene.get_players():
                print(i.get_name())
            self.sidepanel=player_side_panel_widget(self.player_side_widget,parent=self)
            self.sidepanel.setMaximumHeight(600)
        '''

    
        self.gameboardGraphicView.setScene(self.gameboardGraphicScene)
        self.gameboardGraphicView.setGeometry(0,0,700,656)
        self.gameboardGraphicView.setFrameRect(QtCore.QRect(0,0,700,600))
        self.gameboardGraphicView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gameboardGraphicView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

                
        print(self.gameboardGraphicScene.get_coordinate_dictionary_for_board())

        # set style change handler
        self.score_board = score_table(self)
        #self.score_board.hide()


        #self.split = QtGui.QSplitter(self)
        self.horizontalLayout.addWidget(self.sidepanel)
        self.horizontalLayout.addWidget(self.score_board)
        self.horizontalLayout.addWidget(self.gameboardGraphicView)
        '''
        self.split.addWidget(self.sidepanel)
        self.split.addWidget(self.gameboardGraphicView)
        self.split.addWidget(self.score_board)
        '''



        self.gameboardGraphicScene.layout_board()
        self.gameboardGraphicScene.reset_game()
        self.setLayout(self.horizontalLayout)
        self.setFocus(QtCore.Qt.NoFocusReason)
        #self.resizeEvent()
        self.setup_menu_bar()

    def resizeEvent(self,evt=None):
        #self.gameboardGraphicView.setMinimumWidth(self.width()-148)
        #self.gameboardGraphicScene.setSceneRect(0,0,self.gameboardGraphicView.width()-64,640)
        self.gameboardGraphicScene.setSceneRect(0,0,508,640)
        #print("\n\n\n\n\nWINDOW RESIZED!\n\n\n\n\n")

    # handler for changing style
    def handleStyleChanged(self, style):
        QtGui.qApp.setStyle(style)

    def dragLeaveEvent(self):
        pass

    def side_panel_setup(self):
        if self.setup_player_widgets(self.players):
            for i in self.gameboardGraphicScene.get_players():
                print(i.get_name())
            self.sidepanel=player_side_panel_widget(self.player_side_widget,parent=self)
            self.sidepanel.setMaximumHeight(600)
            self.sidepanel.setFixedWidth(144)


    def setup_player_widgets(self,players=None):
        if self.player_count > 0:
            for i in range(self.player_count):
                self.player_side_widget.append(player_score_widget(self.players[i],self.color_style[i],self))
                self.player_side_widget[i].update_scores()
            return 1
        return 0

    def game_setup_dialog_window(self):
        game_setup_dialog(self).exec_()
        if self.closeEarly == True:
            self.destroy()
            self.close()
            print("Closing early")
            exit(0)

        '''
        if self.sidepanel:
            self.horizontalLayout.removeWidget(self.sidepanel)
        if self.gameboardGraphicView:
            self.horizontalLayout.removeWidget(self.gameboardGraphicView)
        '''

        if self.setup_player_widgets(self.players):
            for i in self.gameboardGraphicScene.get_players():
                print(i.get_name())
            if self.sidepanel:
                self.sidepanel.update_all()
            else:
                self.side_panel_setup()
            '''
            self.sidepanel=player_side_panel_widget(self.player_side_widget,parent=self)
            self.sidepanel.setMaximumHeight(600)
            '''


    def new_game_action(self):
        self.game_setup_dialog_window()

        closeOut = self.closeOut
        print("Close out=",closeOut)
        if closeOut:
            return 0
            
        self.score_board.reset_table()
        self.gameboardGraphicScene.reset_game()
        players = self.players
        while len(self.sidepanel.player_widgets) > 4:
            self.sidepanel.player_widgets.pop()
        self.sidepanel.update_all()
        
        print("Widgets",self.sidepanel.player_widgets,"Players",players)
        for x,y in enumerate(self.sidepanel.player_widgets):
            try:
                if players[x]:
                    y.set_player(players[x])
            except:
                break

    def reset_game_action(self):
        if not reset_game_verification(self).exec_():
            return 0

        self.score_board.reset_table()
        self.gameboardGraphicScene.reset_game()
        players = self.players
        while len(self.sidepanel.player_widgets) > 4:
            self.sidepanel.player_widgets.pop()
        self.sidepanel.update_all()
        print("Widgets",self.sidepanel.player_widgets,"Players",players)
        for x,y in enumerate(self.sidepanel.player_widgets):
            try:
                if players[x]:
                    y.set_player(players[x])
            except:
                break


    def about_action(self):
        print("About Action")
        a=about_game_window(self)
        a.show()

    def rule_action(self):
        print("About Action")
        a=rules_window(self)
        a.show()

        
   
    def setup_menu_bar(self):
        self.mainMenuBar.setNativeMenuBar(True)
        self.mainMenuBar.setVisible(False)

        self.new_game_button = QtGui.QAction("&New Game", self)
        self.new_game_button.setShortcut("Ctrl+N")
        self.new_game_button.setStatusTip('Start A New Game')
        self.new_game_button.triggered.connect(self.new_game_action)
        self.connect(QtGui.QShortcut("Ctrl+N", self), QtCore.SIGNAL('activated()'),self.new_game_action)

        self.resetButton = QtGui.QAction("&Reset",self)
        self.resetButton.setShortcut("Ctrl+R")
        self.resetButton.setStatusTip('Exit Application')
        self.resetButton.triggered.connect(self.reset_game_action)
        self.connect(QtGui.QShortcut("Ctrl+R", self), QtCore.SIGNAL('activated()'),self.reset_game_action)

        self.exitButton = QtGui.QAction("&Exit",self)
        #self.exitButton.setShortcut("Ctrl+Q")
        self.exitButton.setStatusTip('Exit Application')
        self.exitButton.triggered.connect(exit)
        self.connect(QtGui.QShortcut("Ctrl+Q", self), QtCore.SIGNAL('activated()'),exit)

        self.toggleMoveButton = QtGui.QAction("&Move History",self)
        self.toggleMoveButton.setShortcut("Ctrl+M")
        self.toggleMoveButton.setStatusTip('Toggle Move History Window')
        self.toggleMoveButton.triggered.connect(self.score_board.toggle_visibility)
        self.connect(QtGui.QShortcut("Ctrl+M", self), QtCore.SIGNAL('activated()'),self.score_board.toggle_visibility)


        self.ruleButton = QtGui.QAction("&Rules",self)
        self.ruleButton.setShortcut("Ctrl+H")
        self.ruleButton.setStatusTip('Rules for the Game')
        self.ruleButton.triggered.connect(self.rule_action)
        self.connect(QtGui.QShortcut("Ctrl+H", self), QtCore.SIGNAL('activated()'),self.rule_action)

        self.aboutButton = QtGui.QAction("&About",self)
        #self.aboutButton.setShortcut("Ctrl+A")
        self.aboutButton.setStatusTip('About Application')
        self.aboutButton.triggered.connect(self.about_action)
        self.connect(QtGui.QShortcut("Ctrl+A", self), QtCore.SIGNAL('activated()'),self.about_action)



        self.fileMenu = self.mainMenuBar.addMenu('&File')
        self.fileMenu.addAction(self.new_game_button)
        self.fileMenu.addAction(self.resetButton)
        self.fileMenu.addAction(self.exitButton)

        self.viewMenu = self.mainMenuBar.addMenu('&View')
        self.viewMenu.addAction(self.toggleMoveButton)

        self.aboutMenu = self.mainMenuBar.addMenu('&Help')
        self.aboutMenu.addAction(self.ruleButton)
        self.aboutMenu.addAction(self.aboutButton)


class score_table(QtGui.QTableWidget):
    def __init__(self,parent=None):
        QtGui.QTableWidget.__init__(self,parent=parent)
        self.parent=parent
        self.scores=[]
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setMaximumWidth(442)
        self.setMinimumWidth(210)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem('Player Name'))
        self.setHorizontalHeaderItem(1,QtGui.QTableWidgetItem('Card'))
        self.setHorizontalHeaderItem(2,QtGui.QTableWidgetItem('Spot Played'))
        self.setHorizontalHeaderItem(3,QtGui.QTableWidgetItem('Score Earned'))

    def reset_table(self):
        print("\n\n\n\n\nRESET TABLE!\n\n\n\n\n")
        self.scores = []
        self.setRowCount(0)
        

    def add_score_to_list(self, scoreItem=None):
        color_style=[QtGui.QColor(175,0,0), QtGui.QColor(25, 117, 209), QtGui.QColor(25, 117, 25), QtGui.QColor(153, 153, 0)]

        self.setRowCount(self.rowCount()+1)
        self.scores.append(scoreItem)

        font=QtGui.QFont('Ubuntu')
        font.setBold(True)
        
        tabWidItem=QtGui.QTableWidgetItem(scoreItem.getName())
        tabWidItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        tabWidItem.setTextColor(color_style[scoreItem.getTurn()])
        tabWidItem.setFont(font)
        self.setItem(self.rowCount()-1,0,tabWidItem)
        
        tabWidItem=QtGui.QTableWidgetItem(scoreItem.getCard())
        tabWidItem.setTextAlignment(QtCore.Qt.AlignCenter)
        tabWidItem.setTextColor(color_style[int(scoreItem.getCardColor())])
        tabWidItem.setFont(font)
        self.setItem(self.rowCount()-1,1,tabWidItem)

        tabWidItem=QtGui.QTableWidgetItem(scoreItem.getSpot())
        tabWidItem.setTextAlignment(QtCore.Qt.AlignCenter)
        tabWidItem.setFont(font)
        self.setItem(self.rowCount()-1,2,tabWidItem)
        
        tabWidItem=QtGui.QTableWidgetItem(scoreItem.getScore())
        tabWidItem.setTextAlignment(QtCore.Qt.AlignCenter)
        tabWidItem.setFont(font)
        self.setItem(self.rowCount()-1,3,tabWidItem)
        self.scrollToBottom()


    def toggle_visibility(self,evt=None):
        if self.isVisible():
            self.hide()
            self.parent.setMinimumWidth(752)
            return False
        self.show()
        self.parent.setMinimumWidth(968)
        return True



class tableScore():
    def __init__(self,player=None,turn=None,card=None,spot=None,score=None,board=None,parent=None):
        self.parent = parent

        self.player = player
        self.turn = turn
        self.card = card
        self.spot = spot
        self.score = score
        self.board = board

    def getName(self):
        return self.player.get_name()

    def printAll(self):
        print("Table Score: ", self.getTurn(), self.getName(), self.getCard(), self.getCardColor(), self.getSpot(), self.getScore(), self.getBoard(),'\n')
        return 0

    def getTurn(self):
        return self.turn

    def getCard(self):
        return str(self.card.get_info(1)[0]+self.card.get_info(1)[1])

    def getCardColor(self):
        return str(self.card.get_info(0)[1])

    def getSpot(self):
        return str((self.spot[0]+1,self.spot[1]+1))

    def getScore(self):
        return str(self.score)

    def getBoard(self):
        return self.board

        


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
        self.score_widgets.setFixedWidth(128)
        self.vlay.addWidget(self.score_widgets)
        self.vlay.addWidget(self.reset_button)
        self.vlay.setAlignment(QtCore.Qt.AlignVCenter)
        size_policy = QtGui.QSizePolicy()
        size_policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
        self.score_widgets.setSizePolicy(size_policy)
        self.setLayout(self.vlay)
        self.setFixedWidth(160)


        print('Width self/reset/scores', self.width(), self.reset_button.width(), self.score_widgets.width())
        self.show()
    
    def update_all(self):
        for i in self.player_widgets:
            i.hide()
            i.update_scores()
        for i in range(len(self.player_widgets)):
            if i < self.parent.player_count:
                self.player_widgets[i].show()
                self.player_widgets[i].set_color_style(self.parent.color_style[i])


    def reset_game(self,e):
        if not reset_game_verification(self.parent).exec_():
            return 0

        self.parent.score_board.reset_table()
        self.parent.gameboardGraphicScene.reset_game()
        players = self.parent.players
        while len(self.player_widgets) > 4:
            self.player_widgets.pop()
        print("Widgets",self.player_widgets,"Players",players)
        for x,y in enumerate(self.player_widgets):
            try:
                if players[x]:
                    y.set_player(players[x])
            except KeyError:
                break
 

    def new_game(self,e):
        print("E:",e)
        self.parent.game_setup_dialog_window()
        closeOut = self.parent.closeOut
        print("Close out=",closeOut)
        if closeOut:
            return 0
            
        self.parent.gameboardGraphicScene.reset_game()
        players = self.parent.players
        while len(self.player_widgets) > 4:
            self.player_widgets.pop()
        print("Widgets",self.player_widgets,"Players",players)
        for x,y in enumerate(self.player_widgets):
            try:
                if players[x]:
                    y.set_player(players[x])
            except KeyError:
                break

        self.parent.score_board.reset_table()
            
    '''
    def reset_game(self,e):
        if not reset_game_verification(self.parent).exec_():
            return 0
        self.parent.game_setup_dialog_window()
        closeOut = self.parent.closeOut
        print("Close out=",closeOut)
        if closeOut:
            return 0
            
        self.parent.gameboardGraphicScene.reset_game()
        players = self.parent.players
        while len(self.player_widgets) > 4:
            self.player_widgets.pop()
        print("Widgets",self.player_widgets,"Players",players)
        for x,y in enumerate(self.player_widgets):
            try:
                if players[x]:
                    y.set_player(players[x])
            except KeyError:
                break
    '''
            

class game_setup_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent=parent)

        if parent:
            self.parent = parent
            self.player_count = 4 
        else:
            self.player_count = 2

        try:
            if self.parent.gameboardGraphicScene.player:
                self.players = self.parent.gameboardGraphicScene.player
            else:
                self.players = self.parent.players
        except:
            self.players = self.parent.players
        self.setWindowTitle("Game Setup")

        print(self.players)
        if len(self.players) == 4:
            print("PC:",self.player_count)
            self.players = [player_setup_options(0,i,self) for i in self.players]
            '''
            elif len(self.players) > self.player_count:
                while len(self.players) != self.player_count:
                    self.players.pop()
                self.players = [player_setup_options(0,i,self) for i in self.players]
            '''
        else:
            if len(self.players) < 4:
                self.players = [player_setup_options(0,i,self) for i in self.players]
                while len(self.players) != 4:
                    self.players.append(player_setup_options(player=game_player.game_player(name='Player',human_player=False, main_gameboard=self.parent.gameboardGraphicScene.main_board)))
            elif len(self.players)>4:
                while len(self.players) > 4:
                    self.players.pop()
                

        '''
        self.generic_names = ['Lynette', 'Bree', 'Susan', 'Bear', 'Dodd', 'Rye','Hanzee','Lou','Homer','Bart','Lisa','Marge', 'Oscar', 'Mr. Blue', 'Vito', 'Ace', 'Darla', 'Dicky', 'Harvey', 'Marcellus', 'Vincent','Jules','Mia','Jimmy','Decker']
        random.shuffle(self.generic_names)
        '''

        self.generic_names = open('./names.csv','r')
        self.generic_names = self.generic_names.read().split('\n')
        self.generic_names.pop(-1)
        random.shuffle(self.generic_names)

        for i in range(1,len(self.players)):
            if self.players[i].player.get_name() == 'Player':
                self.players[i].player.set_name(self.generic_names[i])
            self.players[i].player.set_human(False)
            self.players[i].update_widget_to_player_stats()


            

        self.players[0].update_widget_to_player_stats()
        self.players[0].human_or_computer_combo.setCurrentIndex(0)
        self.players[0].human_or_computer_combo.setDisabled(True)


        self.vbox = QtGui.QVBoxLayout(self)


        '''
        self.player_count_widget_layout = QtGui.QHBoxLayout(self)
        self.player_count_widget = QtGui.QWidget(self)
        self.player_count_label = QtGui.QLabel("Player Count:",self)
        self.player_count_spin = QtGui.QSpinBox(self)
        self.player_count_spin.setMinimum(2)
        self.player_count_spin.setMaximum(4)
        self.player_count_spin.setValue(4)
        self.player_count_spin.setWrapping(True)
        self.player_count_widget_layout.addWidget(self.player_count_label)
        self.player_count_widget_layout.addWidget(self.player_count_spin)
        self.player_count_spin.valueChanged.connect(self.spinChangeEvent)
        self.player_count_widget.setLayout(self.player_count_widget_layout)

        '''

        self.parent.closeOut = True
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
        self.game_mode_spinner.addItem("7: Diamond Sharper")
        self.game_mode_spinner.addItem("8: Corners")
        self.game_mode_spinner.addItem("9: Inverse Corners")

        if 0<= self.parent.gamemode <= 8:
            self.game_mode_spinner.setCurrentIndex(self.parent.gamemode)
        else:
            self.game_mode_spinner.setCurrentIndex(3)
        self.game_mode_widget_layout.addWidget(self.game_mode_label)
        self.game_mode_widget_layout.addWidget(self.game_mode_spinner)

        self.max_cards_widget_layout = QtGui.QHBoxLayout(self)
        self.max_cards_widget = QtGui.QWidget(self)
        self.max_cards_widget.setLayout(self.max_cards_widget_layout)
        self.max_cards_label = QtGui.QLabel("Cards in Hand:",self)
        self.max_cards_combo = QtGui.QComboBox(self)
        self.max_cards_combo.addItem("1: All Cards")
        self.max_cards_combo.addItem("2: 1 Cards")
        self.max_cards_combo.addItem("3: 3 Cards")
        self.max_cards_combo.addItem("4: 5 Cards")
        self.max_cards_combo.addItem("5: 6 Cards")
        self.max_cards_combo.addItem("6: 7 Cards")
        if self.parent.max_card_ind >= 0:
            self.max_cards_combo.setCurrentIndex(self.parent.max_card_ind)
        else:
            self.max_cards_combo.setCurrentIndex(4)
        self.max_cards_widget_layout.addWidget(self.max_cards_label)
        self.max_cards_widget_layout.addWidget(self.max_cards_combo)


        self.player_count_widget_layout = QtGui.QHBoxLayout(self)
        self.player_count_widget = QtGui.QWidget(self)
        self.player_count_label = QtGui.QLabel("Player Count:",self)
        self.player_count_spin = QtGui.QSpinBox(self)
        self.player_count_spin.setMinimum(2)
        self.player_count_spin.setMaximum(4)
        self.player_count_spin.setValue(self.parent.player_count or 4)
        self.spinChangeEvent(self.parent.player_count or 4)
        #self.player_count_spin.setWrapping(True)
        self.player_count_widget_layout.addWidget(self.player_count_label)
        self.player_count_widget_layout.addWidget(self.player_count_spin)
        self.player_count_spin.valueChanged.connect(self.spinChangeEvent)
        self.player_count_widget.setLayout(self.player_count_widget_layout)



        self.vbox.addWidget(self.game_mode_widget)
        self.vbox.addWidget(self.max_cards_widget)
        self.vbox.addWidget(self.player_count_widget)

        for i in self.players:
            self.vbox.addWidget(i)

        self.confirm_button = QtGui.QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirmEvent)
        self.vbox.addWidget(self.confirm_button)

        self.update_players()

    def spinChangeEvent(self,e=None):
        if e:
            print(e)
            self.player_count=e

            for i in range(1,self.player_count):
                self.players[i].enable()

            for i in range(self.player_count,4):
                self.players[i].disable()

    def keyPressEvent(self, e=None):
        if e.key() == QtCore.Qt.Key_Escape:
            self.closeEvent()
            
        
    def closeEvent(self,e=None):
        '''
        self.update_players()
        self.parent.gamemode = self.game_mode_spinner.currentIndex()
        print('interp:',self.interpretMaxCardCombo())
        self.parent.max_card = self.interpretMaxCardCombo()
        self.parent.max_card_ind = self.max_cards_combo.currentIndex()
        '''
        if self.parent.initialSetup:
            print('CLOSED EARLY!')
            self.parent.closeEarly = True
        self.close()

    def confirmEvent(self,e=None):
        print('Confirmed!')
        self.parent.initialSetup = False
        self.parent.closeEarly = False
        self.parent.closeOut = False
        self.update_players()
        self.parent.gamemode = self.game_mode_spinner.currentIndex()
        print('interp:',self.interpretMaxCardCombo())
        self.parent.max_card = self.interpretMaxCardCombo()
        self.parent.max_card_ind = self.max_cards_combo.currentIndex()
        self.close()



    def interpretMaxCardCombo(self):
        temp = self.max_cards_combo.currentIndex()
        if temp == 1:
            return 1
        elif temp == 2:
            return 3
        elif temp == 3:
            return 5
        elif temp == 4:
            return 6
        elif temp == 5:
            return 7
        return 0
        

    def update_players(self,e=None):
        for i in self.players:
            i.update_player()

        player_list = [self.players[i].get_player() for i in range(self.player_count)]
        
        print('players update',player_list[0].get_name())

        self.parent.player_count = self.player_count
        self.parent.players=player_list


class about_game_window(QtGui.QDialog):
    def __init__(self, parent=None):
        print("About Game Window Init")
        QtGui.QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(400,300)
        self.setWindowTitle("About King's Court")
        self.v_lay = QtGui.QVBoxLayout()
        self.setLayout(self.v_lay)
        self.closeButton = QtGui.QPushButton("Close")
        self.texWindow=QtGui.QTextBrowser()
        self.texWindow.setReadOnly(True)
        f = open('./about/about.html','r')
        html = f.read()
        f.close()
        self.texWindow.setHtml(html)
        self.texWindow.setOpenExternalLinks(True)
        self.texWindow.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.v_lay.addWidget(self.texWindow)
        self.v_lay.addWidget(self.closeButton)
        self.closeButton.clicked.connect(self.destroy_window)
        self.closeButton.hide()
        self.show()

    def destroy_window(self):
        self.destroy()

class rules_window(QtGui.QDialog):
    def __init__(self, parent=None):
        print("About Game Window Init")
        QtGui.QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(QtCore.Qt.Window)
        #self.setFixedSize(400,320)
        self.setMinimumSize(1248,700)
        self.setWindowTitle("Game Rules")
        self.v_lay = QtGui.QVBoxLayout()
        self.setLayout(self.v_lay)
        self.closeButton = QtGui.QPushButton("Close")
        self.texWindow=QtGui.QTextBrowser()
        self.texWindow.setReadOnly(True)
        f = open('./rules/rules2.html','r')
        html = f.read()
        f.close()
        self.texWindow.setHtml(html)
        self.texWindow.setOpenExternalLinks(True)
        self.v_lay.addWidget(self.texWindow)
        self.v_lay.addWidget(self.closeButton)
        self.closeButton.clicked.connect(self.destroy_window)
        self.closeButton.hide()
        self.show()

    def destroy_window(self):
        self.destroy()

        


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
        self.human_or_computer_combo.addItem("Human")
        self.human_or_computer_combo.addItem("Computer")
        self.human_or_computer_combo.setCurrentIndex(0)
        self.human_or_computer_combo.currentIndexChanged.connect(self.human_comp_change)


        self.player_name_text_edit = QtGui.QLineEdit(self.player.get_name() if self.player else "Player", self)
        self.player_level_label = QtGui.QLabel("AI Level:")
        self.player_level_spin = QtGui.QSpinBox(self)
        self.player_level_spin.setMinimum(1)
        self.player_level_spin.setMaximum(6)
        self.player_level_spin.setWrapping(False)
        self.player_level_spin.setValue(player.get_computer_level() if player else 2)

        if self.player.is_human():
            self.human_or_computer_combo.setCurrentIndex(0)
            self.human_or_computer_combo.setEnabled(True)
            self.player_level_spin.setDisabled(True)
        else:
            self.human_or_computer_combo.setCurrentIndex(1)
            self.player_level_spin.setEnabled(True)



        self.hbox.addWidget(self.human_or_computer_combo)
        self.hbox.addWidget(self.player_name_text_edit)
        self.hbox.addWidget(self.player_level_label)
        self.hbox.addWidget(self.player_level_spin)

        self.setLayout(self.hbox)



        self.update_player()

    def human_comp_change(self,e=None):
        if e == 0:
            self.disable_ai()
        else:
            self.enable()

    def disable_ai(self):
        self.player_level_spin.setDisabled(True)

    def disable(self):
        self.human_or_computer_combo.setDisabled(True)
        self.player_name_text_edit.setDisabled(True)
        self.player_level_spin.setDisabled(True)

    def enable(self):
        self.human_or_computer_combo.setEnabled(True)
        self.player_name_text_edit.setEnabled(True)
        self.player_level_spin.setEnabled(True)


    def update_widget_to_player_stats(self):
        self.player_name_text_edit.setText(self.player.get_name())
        self.player_level_spin.setValue(self.player.get_computer_level())
        if self.player.is_human():
            self.player_level_spin.setDisabled(True)
        self.human_or_computer_combo.setCurrentIndex(0 if self.player.is_human() else 1)


    def update_player(self):
        self.player.set_name(self.player_name_text_edit.text())
        self.player.set_computer_level(self.player_level_spin.value())
        self.player.set_human(True if self.human_or_computer_combo.currentIndex() == 0 else False)

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
        self.message.setWordWrap(True)
        self.message.setMinimumWidth(256)

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
        self.setFixedSize(300,128)
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
        self.player_name_label.setFixedHeight(30)
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
        self.setMaximumHeight(64)

    def set_color_style(self, colorStyle):
        if colorStyle:
            self.player_name_label.setStyleSheet(colorStyle)

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
        self.bott_y = 52

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
                    i.setScale(.85)
                    i.setY(self.top_y)
                i.setZValue(count)
            else:
                i.setScale(.85)
                i.setX(self.bott_row[count % 9])
                i.setY(self.bott_y)
                i.setZValue(count)
        
            count += 1
            self.addToGroup(i)

    def hide_cards(self):
        for i in self.player_deck:
            i.hide()

    def show_cards(self):
        for i in self.player_deck:
            i.show()

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
        self.max_cards = self.parent.max_card
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

    def get_human_players(self):
        c = []
        for i in self.player:
            if i.is_human():
                c.append(i)
        return c

    def get_human_player_count(self):
        return len(self.get_human_players())

    def get_players(self):
        return self.player

    def computer_turns(self):
        self.player_turn=self.player_turn % self.player_count
        if self.is_game_over():
            temp=game_over_screen(self.player,scene=self)
            temp.setX(0)
            temp.setY(0)
            temp.setZValue(200)
            self.addItem(temp)
            print("Screen Added!")
            return 0

        if self.player[self.player_turn].is_human():
            self.card_dock.set_player(self.player[self.player_turn])
            self.card_dock.update_dock()

            if self.get_human_player_count()>1:
                self.card_dock.hide_cards()
                temp=human_player_turn_dialog(self.player,self.player_turn,scene=self)
                temp.setX(0)
                temp.setY(0)
                temp.setZValue(200)
                self.addItem(temp)
                print("Screen Added!")



            return 0
        else:
            while self.player[self.player_turn].is_computer():
                comp_move=self.player[self.player_turn].get_computer_move()
                print('comp_move',comp_move)
                if not comp_move: 
                    self.player_turn=(self.player_turn+1) % self.player_count
                else:
                    anchor_score=self.main_board.get_score_to_anchor_card(comp_move[0],comp_move[1],mercy=self.player[self.player_turn].has_mercy())
                    self.player[self.player_turn].set_score(anchor_score)

                    self.parent.score_board.add_score_to_list(tableScore(self.player[self.player_turn],self.player_turn,comp_move[0],comp_move[1],anchor_score))
                    

                    self.main_board.set_card_on_board(comp_move[0],comp_move[1])
                    self.player[self.player_turn].card_hand.deal_card([comp_move[0]])
                    self.player[self.player_turn].drawl_card_from_deck()
                    self.player_turn=(self.player_turn+1) % self.player_count
                    self.player_turn=self.player_turn % self.player_count
                    if self.player_turn == 0:
                        self.player[self.player_turn].read_all_moves()
                    self.layout_board()

                for i in range(5):
                    QtGui.QApplication.processEvents()

            if self.is_game_over():
                temp=game_over_screen(self.player,scene=self)
                temp.setX(0)
                temp.setY(0)
                temp.setZValue(200)
                self.addItem(temp)
                print("Screen Added!")


            for i in self.player:
                sorter=carddeck.carddeck(0)
                sorter.deck=i.card_hand.get_deck()
                sorter.sort_deck_by_card_suit()
                sorter.sort_deck_by_card_value()
                print(i.get_name(),"hand:",sorter.get_deck(1))

            if self.player[self.player_turn].is_human():

                self.card_dock.set_player(self.player[self.player_turn])
                self.card_dock.update_dock()

                
                if self.get_human_player_count()>1 and not self.is_game_over():
                    self.card_dock.hide_cards()
                    temp=human_player_turn_dialog(self.player,self.player_turn,scene=self)
                    temp.setX(0)
                    temp.setY(0)
                    temp.setZValue(200)
                    self.addItem(temp)
                    print("Screen Added!")

                   
                #self.player[self.player_turn].get_computer_move_v2()
                '''
                temp=game_over_screen(self.player,scene=self)
                temp.setX(0)
                temp.setY(0)
                temp.setZValue(200)
                self.addItem(temp)
                print("Screen Added!")
                '''
                if self.is_human_game_over():
                    self.player_turn=(self.player_turn+1) % self.player_count
                    self.player_turn=self.player_turn % self.player_count
                return 0


    def is_game_over(self):
        for i in self.player:
            if i.has_legal_move_left(): 
                print(i.get_name(),"has legal move left, game not over")
                return False
        return True


    def is_human_game_over(self):
        for i in self.player:
            if i.is_human():
                if i.has_legal_move_left(): 
                    return False
        return True

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
        #self.player_turn=0
        self.player_turn=random.randint(0,len(self.player))
        self.player_count = len(self.player)
        try:
            if self.player[self.player_turn].is_human():
                self.card_dock.set_player(self.player[self.player_turn])
        except:
            self.card_dock.set_player(self.player[0])

        count = 0
        print('full deck',self.main_board.game_deck.get_deck(1))
        print('len full deck',len(self.main_board.game_deck.get_deck(1)))
        
        if self.max_cards == 0:
            while not self.main_board.game_deck.is_deck_empty():
                dealt=self.main_board.game_deck.deal_card()[0]
                print("dealt",dealt)
                self.player[count % self.player_count].card_hand.take_card(dealt)
                count += 1
        else:
            while count < self.player_count * self.max_cards:
                if self.main_board.game_deck.is_deck_empty():
                    break
                dealt=self.main_board.game_deck.deal_card()[0]
                print("dealt",dealt)
                self.player[count % self.player_count].card_hand.take_card(dealt)
                count += 1
        self.computer_turns()


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
                #anchor_score=self.main_board.get_score_to_anchor_card(comp_move[0],comp_move[1],mercy=self.player[self.player_turn].has_mercy())
                anchor_score=self.main_board.get_score_to_anchor_card(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1]),mercy=player.has_mercy(),verbo=1)
                coords = self.main_board.get_coordinates_by_index(smallest[1])
                #self.player[self.player_turn].set_score(anchor_score)
                self.parent.score_board.add_score_to_list(tableScore(self.player[self.player_turn],self.player_turn,card.get_card_class(),coords,anchor_score))
                
                player.set_score(anchor_score)

                print("Player Score: ",player.get_score())
            print(self.main_board.set_card_on_board(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1])))
            card.set_click_off()
            player.get_hand().deal_card([card.get_card_class()])
            player.drawl_card_from_deck()
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


    def close_game_over_screens(self):
        for i in self.items():
            if isinstance(i,game_over_screen):
                self.removeItem(i)

    def close_human_player_screen(self):
        for i in self.items():
            if isinstance(i,human_player_turn_dialog):
                self.removeItem(i)
        self.card_dock.show_cards()

    def keyPressEvent(self, e=None):
        if e.key() == QtCore.Qt.Key_Space:
            print("Space pressed!")
            if isinstance(self.focusItem(),human_player_turn_dialog):
                self.close_human_player_screen()
                self.clearFocus()


    def reset_game(self):
        print("------------------------------------------\n",self.cards_on_board_dictionary.items())

        self.main_board.set_game_mode(self.parent.gamemode)
        self.max_cards = self.parent.max_card

        self.main_board.reset_game()

        for i in self.items():
            if isinstance(i,playing_card_graphic) or isinstance(i,human_player_turn_dialog) or isinstance(i,game_over_screen):
                self.removeItem(i)
            
        print("Turn: ------------- ",self.player_turn)
        self.setup_players(4) 

        if self.player[self.player_turn].is_human():
            self.card_dock.set_player(self.player[self.player_turn])
        self.card_dock.update_dock()
        self.layout_board()

class human_player_turn_dialog(QtGui.QGraphicsItemGroup):
    def __init__(self, players=None, current_player=None,parent=None,scene=None):
        self.parent = parent
        self.scene = scene
        if players:
            self.players = players
            print(self.players,"These are the players!")
            self.curplay = self.players[current_player]
            self.curplay_pos = 0
            for i in range(len(self.players)):
                if self.players[i] == self.curplay:
                    self.curplay_pos = i
                    break
            self.curplay_name = self.curplay.get_name()
                    
            print(self.curplay_name,"is up next!")
        else:
            self.players = []

        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        self.setHandlesChildEvents(False)

        self.graphicRectangle = QtGui.QGraphicsRectItem(0,0,512,512,self)
        self.graphicRectangle.setBrush(QtGui.QBrush(QtGui.QColor(255,255,255,196)))
        self.graphicRectangle.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.curplayFont = QtGui.QFont()
        self.curplayFont.setPointSize(72)
        self.curplayFont.setBold(True)
        self.addToGroup(self.graphicRectangle)

        self.curplayText = QtGui.QGraphicsTextItem(self.curplay_name, parent=self,scene=scene)
        self.curplayText.setTextWidth(512)
        self.curplayText.setFont(self.curplayFont)
        #self.curplayText.setHtml("<center><font size = 108><b>"+self.curplay_name+" Wins!</b></font></center>")
        self.curplayText.setHtml("<center>"+self.curplay_name+"<br> is up next.</center>")

        self.color_style=[QtGui.QColor(175, 0, 0), QtGui.QColor(25, 117, 209), QtGui.QColor(25, 117, 25), QtGui.QColor(153, 153, 0)]
        self.curplayText.setDefaultTextColor(self.color_style[self.curplay_pos])

        self.curplayText.setY(220-144)
        self.addToGroup(self.curplayText)

        self.close_graphic_button = game_over_close_button(scene=self.scene)
        self.close_graphic_button.setX(472)
        self.close_graphic_button.setY(10)

        
        self.addToGroup(self.close_graphic_button)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable,True)
        scene.setFocusItem(self)
        print("Focus on me:", scene.focusItem())

        #self.graphicRectangle.setVisible(True)

       

class game_over_screen(QtGui.QGraphicsItemGroup):
    def __init__(self, players=None, parent=None, scene=None):
        self.parent = parent
        self.scene = scene
        if players:
            self.players = players
            print(self.players,"These are the players!")
            self.winner = sorted(self.players, key=lambda x: x.get_score(),reverse=True)[0]
            self.winner_pos = 0
            for i in range(len(self.players)):
                if self.players[i] == self.winner:
                    self.winner_pos = i
                    self.winner_name = self.winner.get_name()
                    break
                    
            print(self.winner_name,"wins!")
        else:
            self.players = []

        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        self.setHandlesChildEvents(False)

        self.graphicRectangle = QtGui.QGraphicsRectItem(0,0,512,512,self)
        self.graphicRectangle.setBrush(QtGui.QBrush(QtGui.QColor(255,255,255,196)))
        self.graphicRectangle.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.winnerFont = QtGui.QFont()
        self.winnerFont.setPointSize(72)
        self.winnerFont.setBold(True)
        self.addToGroup(self.graphicRectangle)

        self.winnerText = QtGui.QGraphicsTextItem(self.winner_name, parent=self,scene=scene)
        self.winnerText.setTextWidth(512)
        self.winnerText.setFont(self.winnerFont)
        #self.winnerText.setHtml("<center><font size = 108><b>"+self.winner_name+" Wins!</b></font></center>")
        self.winnerText.setHtml("<center>"+self.winner_name+" Wins!</center>")

        self.color_style=[QtGui.QColor(175, 0, 0), QtGui.QColor(25, 117, 209), QtGui.QColor(25, 117, 25), QtGui.QColor(153, 153, 0)]
        self.winnerText.setDefaultTextColor(self.color_style[self.winner_pos])

        self.winnerText.setY(220-144)
        self.addToGroup(self.winnerText)

        self.close_graphic_button = game_over_close_button(scene=self.scene)
        self.close_graphic_button.setX(472)
        self.close_graphic_button.setY(10)
        self.addToGroup(self.close_graphic_button)
        #self.graphicRectangle.setVisible(True)


class game_over_close_button(QtGui.QGraphicsItemGroup):
    def __init__(self,parent=None, scene=None):
        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        self.parent= parent
        self.scene = scene
        self.mouse_state_colors = [QtGui.QColor(0,0,0), QtGui.QColor(255,0,0), QtGui.QColor(128,0,0)]
        self.backrect = QtGui.QGraphicsRectItem(0,0,26,36,parent)
        self.backrect.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0,0)))
        self.backrect.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.addToGroup(self.backrect)

        font = QtGui.QFont()
        font.setPointSize(20)
        self.topText = QtGui.QGraphicsTextItem('',self)
        self.topText.setHtml('<center>X</center>')
        self.topText.setFont(font)
        self.topText.setTextWidth(20)
        self.addToGroup(self.topText)
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QtCore.QRectF(0,0,20,20)

    def mouseReleaseEvent(self, event): 
        print("Released!")
        self.topText.setDefaultTextColor(self.mouse_state_colors[1])
        self.scene.close_game_over_screens()
        self.scene.close_human_player_screen()

    def mousePressEvent(self, event): 
        print("Pressed!")
        self.topText.setDefaultTextColor(self.mouse_state_colors[2])

    def hoverEnterEvent(self,event):
        self.topText.setDefaultTextColor(self.mouse_state_colors[1])

    def hoverLeaveEvent(self,event):
        self.topText.setDefaultTextColor(self.mouse_state_colors[0])


     

                
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
        self.temp_scale = self.scale()
        self.setScale(1)
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
            print('top_scene player',self.player.get_name())
            if self.top_scene.drop_card_on_board(self,self.player) == 1:
                self.setScale(1)
                self.hide()
                for i in range(5):
                    QtGui.QApplication.processEvents()

                self.top_scene.computer_turns()
                self.top_scene.print_player_scores()
            else:
                self.setScale(self.temp_scale)
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
