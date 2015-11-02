from PyQt4 import QtCore, QtGui
import random
import sys

class AppWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AppWidget, self).__init__(parent)
        self.setGeometry(0,0,825,625)
        horizontalLayout = QtGui.QHBoxLayout()
        self.gameboardGraphicView = QtGui.QGraphicsView()
        self.gameboardGraphicScene = QtGui.QGraphicsScene(self.gameboardGraphicView)
        self.gameboardGraphicScene.setSceneRect(QtCore.QRectF())
        self.gameboardGraphicView.setScene(self.gameboardGraphicScene)
        self.gameboardGraphicView.setSceneRect(0,0,800,600)

        '''
        self.testRect = QtGui.QGraphicsRectItem(20,20,20,20)
        self.testRect.setBrush(QtGui.QBrush(QtCore.Qt.darkCyan))
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
            j.setX(i%7*(64+spacer))
            j.setY(i//7*(64+spacer))
            self.gameboardGraphicScene.addItem(j)

        print(self.all_cards[24].x(),self.all_cards[24].y())
        self.gameboardGraphicView.setSceneRect(self.all_cards[0].x()-152,self.all_cards[0].y()-52,800,600)
        #self.gameboardGraphicScene.addItem(self.testRect)
        #self.gameboardGraphicScene.addItem(self.testRect2)
        print(self.gameboardGraphicScene.children())

        # set style change handler
        horizontalLayout.addWidget(self.gameboardGraphicView)
        self.setLayout(horizontalLayout)

    # handler for changing style
    def handleStyleChanged(self, style):
        QtGui.qApp.setStyle(style)


class playing_card_graphic(QtGui.QGraphicsItem):
    def __init__(self, suit=0, value=0,parent=None,scene=None):
        QtGui.QGraphicsItem.__init__(self,parent,scene)
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
        self.suit_color=[red,blue,green,yellow,violet]
        self.pix_maps=[QtGui.QPixmap('./cards/card_template_red_square.png'),QtGui.QPixmap('./cards/card_template_blue_square.png'),QtGui.QPixmap('./cards/card_template_green_square.png'),QtGui.QPixmap('./cards/card_template_yellow_square.png'),QtGui.QPixmap('./cards/card_template_violet_square.png')]
        print(self.pix_maps[self.suit])
        self.background = QtGui.QGraphicsPixmapItem(self.pix_maps[self.suit],self)
        '''
        self.background = QtGui.QGraphicsRectItem(0,0,64,64,self)
        self.background.setBrush(QtGui.QBrush(self.suit_color[self.suit]))
        self.whiteLayerBackground = QtGui.QGraphicsRectItem(8,8,48,48,self)
        self.whiteLayerBackground.setBrush(QtGui.QBrush(QtCore.Qt.black))
        '''
        self.number = QtGui.QGraphicsTextItem(str(value),self)
        self.number.setDefaultTextColor(self.suit_color[self.suit])
        self.number.setX(17)
        self.number.setY(3)
        self.font = QtGui.QFont('Ubuntu Mono',36,1)
        self.number.setFont(self.font)
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QtCore.QRectF(0,0,64,64)

    def hoverEnterEvent(self, event):
        cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)
        QtGui.QApplication.instance().setOverrideCursor(cursor)

    def hoverLeaveEvent(self,event):
        QtGui.QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self,event):
        new_position = event.scenePos()

        old_position = self.scenePos()
        #new_position.setY(old_position.y())
        print("Moved!")

        self.setX(new_position.x()-32)
        self.setY(new_position.y()-32)

    def mousePressEvent(self, event): 
        print(self.zValue())
        self.setZValue(1)
        new_position = event.scenePos()

        self.setX(new_position.x()-32)
        self.setY(new_position.y()-32)
        pass

    def mouseReleaseEvent(self, event): 
        self.setZValue(0)
        pass

    def get_card(self):
        return self
        


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    widgetApp = AppWidget()
    widgetApp.show()
    sys.exit(app.exec_())
