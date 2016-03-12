from PyQt4 import QtCore, QtGui
import gameboard
import random
import sys

class AppWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AppWidget, self).__init__(parent)
        self.setGeometry(0,0,825,625)
        horizontalLayout = QtGui.QHBoxLayout()
        self.gameboardGraphicView = QtGui.QGraphicsView()
        self.gameboardGraphicScene = game_board(self.gameboardGraphicView)
        self.gameboardGraphicView.setScene(self.gameboardGraphicScene)
        self.gameboardGraphicView.setSceneRect(0,0,800,600)
        self.gameboardGraphicView.setSceneRect(self.gameboardGraphicScene.sceneRect())

        '''
        self.testRect = QtGui.QGraphicsRectItem(20,20,20,20)
        self.testRect.setBrush(QtGui.QBrush(QtCore.Qt.darkCyan))
        '''

        '''
        self.testRect = playing_card_graphic(3,6)
        self.testRect2 = playing_card_graphic(1,0)
        print(self.testRect.x(),self.testRect.y())
        self.testRect2.setX(64)
        self.testRect2.setY(64)
        
        self.color_balance = [i%5 for i in range(48)]+[random.randint(0,4)]
        self.color_balance = [i//12 for i in range(48)]+[random.randint(0,3)]
        self.num_bal = [i%6+1 for i in range(48)]+[0]
        self.cards = []
        for i in range(49):
            self.cards.append([self.color_balance.pop(),self.num_bal.pop()])
        print(self.cards)

        random.shuffle(self.cards)


        

        self.all_cards = [playing_card_graphic(i[0],i[1]) for i in self.cards]

        for i,j in enumerate(self.all_cards):
            spacer = 8
            j.setX(i%7*(64+spacer)+spacer)
            j.setY(i//7*(64+spacer)+spacer)
            self.gameboardGraphicScene.addItem(j)

        '''
        #self.gameboardGraphicScene.addItem(self.testRect)
        #self.gameboardGraphicScene.addItem(self.testRect2)
        print(self.gameboardGraphicScene.get_coordinate_dictionary_for_board())

        # set style change handler
        horizontalLayout.addWidget(self.gameboardGraphicView)
        self.setLayout(horizontalLayout)

    # handler for changing style
    def handleStyleChanged(self, style):
        QtGui.qApp.setStyle(style)

class game_board_background(QtGui.QGraphicsItemGroup):
    def __init__(self, parent=None, scene=None):
        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        background_rect = QtGui.QGraphicsRectItem()
        background_rect.setBrush(QtGui.QBrush(QtGui.QColor(80,60,0)))
        background_rect.setRect(0,0,64*7+8*8,64*7+8*8)

        self.addToGroup(background_rect)

class player_card_dock(QtGui.QGraphicsItemGroup):
    def __init__(self, parent=None, scene=None):
        QtGui.QGraphicsItemGroup.__init__(self,parent,scene)
        self.card_dock_back = QtGui.QGraphicsRectItem()
        self.card_dock_back.setBrush(QtGui.QBrush(QtGui.QColor(60,45,0)))

        self.card_dock_back.setRect(0,0,64*8,64*2)

        self.addToGroup(self.card_dock_back)

class game_board(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self,parent)
        self.main_board = gameboard.gameboard(0,1)
        self.main_board.set_initial_board()
        self.cards_on_board_dictionary={i:None for i in range(self.main_board.get_board_side_length())}
        self.setSceneRect(QtCore.QRectF())
        background = game_board_background()
        background.setX(0)
        background.setY(0)

        card_dock = player_card_dock()
        card_dock.setY(64*8+8)

        self.addItem(background)
        self.addItem(card_dock)
        self.layout_board()

    def get_coordinate_dictionary_for_board(self):
        board_length = self.main_board.get_board_side_length()
        piece_width = 64
        spacer = 8
        coordinates = {}
        for i in range(0,int(board_length**2)):
            coordinates[i]=[i % board_length*(piece_width+spacer)+spacer, i//board_length*(piece_width+spacer)+spacer]
        return coordinates

    def drop_card_on_board(self, card):
        x=card.x()
        y=card.y()
        coord_dict = self.get_coordinate_dictionary_for_board()
        temp_dict = {}
        for i in coord_dict.keys():
            temp_dict[i] = ((coord_dict[i][0]-x)**2+(coord_dict[i][1]-y)**2)**.5

        smallest = [temp_dict[0],0]
        for i in temp_dict.keys():
            if temp_dict[i] < smallest[0]:
                smallest = [temp_dict[i],i]
        if self.main_board.is_legal_to_anchor_card(card.get_card_class(),self.main_board.get_coordinates_by_index(smallest[1])):
            card.setX(coord_dict[smallest[1]][0])
            card.setY(coord_dict[smallest[1]][1])
        else:
            old_pos = card.old_position
            card.setX(old_pos[0])
            card.setY(old_pos[1])
        card.set_click_off()

            

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
                #if i % 2 == 0:
                self.cards_on_board_dictionary[i].set_click_off()
                self.addItem(self.cards_on_board_dictionary[i])


        
class playing_card_graphic(QtGui.QGraphicsItem):
    def __init__(self, suit=0, value=0,card=None,parent=None,scene=None):
        if card:
            self.card = card
            card_info = self.card.get_info(0)
            if card_info[0] == 12:
                value = 0
            else:
                value = card_info[0]+1
            suit = card_info[1]

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
        self.back_pix_maps=[QtGui.QPixmap('./cards/card_template_red_square.png'),
                            QtGui.QPixmap('./cards/card_template_blue_square.png'),
                            QtGui.QPixmap('./cards/card_template_green_square.png'),
                            QtGui.QPixmap('./cards/card_template_yellow_square.png'),
                            QtGui.QPixmap('./cards/card_template_violet_square.png')]



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
        self.old_position = [self.x(),self.y()]

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
        self.setY(new_position.y()-32)

    def mousePressEvent(self, event): 
        if self.click_disabled:
            return
        self.old_position = [self.x(),self.y()]
        self.setZValue(1)
        new_position = event.scenePos()
        self.setX(new_position.x()-32)
        self.setY(new_position.y()-32)

    def mouseReleaseEvent(self, event): 
        if self.click_disabled:
            return
        self.setZValue(1)
        if self.top_scene:
            print(self.top_scene.drop_card_on_board(self))
        print(self.x(),self.y())

    def get_card(self):
        return self
        


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    widgetApp = AppWidget()
    widgetApp.show()
    sys.exit(app.exec_())
