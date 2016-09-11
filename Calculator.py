import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

class LCDWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lcd = QLCDNumber(self)
        print('lcd init!:' + str(self.lcd))
        self.layout = QVBoxLayout()

        #液晶部分が自動伸長する設定
        self.lcd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.lcd)

        self.setLayout(self.layout)

    def updateDisplay(self, number):
        print('Update Display!')
        print('lcd :' + str(self.lcd))
        self.lcd.display(number)
        self.lcd.update()
        print('Update End!')

class PushButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                '1', '2', '3', '-',
                '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]
        self.currentNum = 0.0
        self.resultNum = 0.0
        self.tmpNum = 0.0
        self.minusCount = 0
        self.pushOperatorFlg = False
        self.plusButtonClickFlg = False
        self.minusButtonClickFlg = False
        self.asterliskButtonClickFlg = False
        self.slashButtonClickFlg = False
        self.dotButtonClickFlg = False
        self.state = ''
        # 電卓のボタン配置
        for position, name in zip(positions, names):

            if name == '':
                continue
            button = QPushButton(name)
            layout.addWidget(button, *position)
            if name == '+':
                button.clicked.connect(self.plusButtonClicked)
            elif name == '-':
                button.clicked.connect(self.minusButtonClicked)
            elif name == '*':
                button.clicked.connect(self.asterliskButtonClicked)
            elif name == '/':
                button.clicked.connect(self.slashButtonClicked)
            elif name == '=':
                button.clicked.connect(self.equalButtonClicked)
            elif name == 'Cls':
                button.clicked.connect(self.clsButtonClicked)
            elif name == 'Bck':
                button.clicked.connect(self.bckButtonClicked)
            elif name == 'Close':
                button.clicked.connect(self.closeButtonClicked)
            elif name == '.':
                button.clicked.connect(self.dotButtonClicked)
            else:
                button.clicked.connect(self.numberButtonClicked)
        self.setLayout(layout)

    #LcdWidgetのインスタンスを取得する(ボタン押下時の液晶画面更新等に使用)
    def setLcdWidget(self, lcdWidget):
        self.lcdwidget = lcdWidget
        print('set lcdwidget! :' + str(self.lcdwidget))

    def numberButtonClicked(self):
        print('Number Button Clicked!')
        # シグナル送信元のウィジェット取得(押下ボタンウィジェット)
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        print ('Now Display Number' + str(self.lcdwidget.lcd.value()))
        if(self.currentNum == 0 or self.pushOperatorFlg == True):
            self.currentNum = int(buttonText)
            self.lcdwidget.updateDisplay(int(buttonText))
        elif (self.state == 'DOT'):
            print('dot!')
            print(int(buttonText) / 10)
            self.currentNum = self.tmpNum + int(buttonText) / 10
            self.lcdwidget.updateDisplay(self.currentNum)
        else:
            self.currentNum = self.currentNum * 10 + (int(buttonText))
            self.lcdwidget.updateDisplay(self.currentNum)

    def plusButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        self.tmpNum += self.currentNum
        #同じ演算子ボタンを2回以上押下した場合
        if(self.state == 'PLUS'):
            self.resultNum += self.tmpNum
            self.lcdwidget.updateDisplay(self.resultNum)
            self.tmpNum = 0
        self.setState(buttonText)
        self.pushOperatorFlg = True

    def minusButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        if (self.state != 'MINUS'):
            self.tmpNum = self.currentNum
        if (self.state == 'MINUS'):
            if(self.minusCount == 0):
                self.resultNum = self.tmpNum - self.currentNum
                self.minusCount += 1
            else:
                self.resultNum -= self.currentNum
            self.lcdwidget.updateDisplay(self.resultNum)
        self.setState(buttonText)
        self.pushOperatorFlg = True

    def slashButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        self.tmpNum = self.currentNum
        if (self.state == 'DIVIDE'):
            if self.currentNum != 0:
                if(self.resultNum == 0):
                    self.resultNum = self.currentNum / self.tmpNum
                    self.lcdwidget.updateDisplay(self.resultNum)
                else:
                    self.resultNum /= self.currentNum
                    self.lcdwidget.updateDisplay(self.resultNum)
            else:
                self.init(True)
                return
            self.tmpNum = 0
        self.setState(buttonText)
        self.pushOperatorFlg = True

    def asterliskButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        self.tmpNum = self.currentNum
        # 同じ演算子ボタンを2回以上押下した場合
        if self.state == 'MULTIPLE':
            if(self.resultNum == 0):
                self.resultNum = self.currentNum * self.tmpNum
            else:
                self.resultNum *= self.currentNum
            self.lcdwidget.updateDisplay(self.resultNum)
            self.tmpNum = 0
        self.setState(buttonText)
        self.pushOperatorFlg = True

    def equalButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        if (self.state == 'PLUS'):
            self.resultNum = self.tmpNum + self.currentNum
        elif (self.state == 'MINUS'):
            self.resultNum = self.tmpNum - self.currentNum
        elif (self.state == 'MULTIPLE'):
            self.resultNum = self.tmpNum * self.currentNum
        elif (self.state == 'DIVIDE'):
            if(self.currentNum != 0):
                self.resultNum = self.tmpNum / self.currentNum
            else:
                self.init(True)
                return
        self.lcdwidget.updateDisplay(self.resultNum)
        self.currentNum = 0
        self.pushOperatorFlg = False

    def dotButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        self.tmpNum = self.currentNum
        self.setState(buttonText)

    def clsButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        self.init()

    def bckButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()

    def closeButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()

    def init(self, Error=False):
        self.tmpNum = 0
        self.resultNum = 0
        self.currentNum = 0
        self.state = ''
        if(Error == False):
            self.lcdwidget.updateDisplay(0)
        else:
            print('Zero Divide Error!!!!!!')
            self.lcdwidget.updateDisplay('ERROR')


    def setState(self, buttonText):
       if(buttonText == '+'):
           print('setFlg!' + buttonText)
           self.state = 'PLUS'
       elif(buttonText == '-'):
           print('setFlg!' + buttonText)
           self.state = 'MINUS'
       elif(buttonText == '*'):
           print('setFlg!' + buttonText)
           self.state = 'MULTIPLE'
       elif(buttonText == '/'):
           print('setFlg!' + buttonText)
           self.state = 'DIVIDE'
       elif(buttonText == '.'):
           print('setFlg!' + buttonText)
           self.state = 'DOT'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = QWidget()
    lcd_widget = LCDWidget()
    print('new lcdwidget! :' + str(lcd_widget))
    pushbutton_widget = PushButtonWidget()
    pushbutton_widget.setLcdWidget(lcd_widget)
    #作成した液晶画面,ボタンをメインウィンドウに上下に配置
    panel_layout = QVBoxLayout()
    panel_layout.addWidget(lcd_widget)
    panel_layout.addWidget(pushbutton_widget)
    panel.setLayout(panel_layout)

    # メインウィンドウ描画
    main_window = QMainWindow()
    main_window.setGeometry(300, 300, 400, 300)
    main_window.setCentralWidget(panel)
    main_window.setWindowTitle('Calculator')
    main_window.show()
    sys.exit(app.exec_())