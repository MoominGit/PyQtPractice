import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
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
        self.state = 'START'
        #リストにクリックした数字を格納する
        self.numberList = [0, 0]
        #リストの中の格納領域を指定する
        #0 = 電卓起動時
        #1 = 1度でも=か演算子が押された場合
        self.inputPositon = 0
        #最後に押した演算子
        #=を押した際の計算に使用する
        self.lastPushOperator = ''
        #計算後はリストの0番目を常に表示
        self.displayPositon = 0
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
        if(self.state != 'START' and self.state != 'DOT'):
            self.inputPositon = 1
        # シグナル送信元のウィジェット取得(押下ボタンウィジェット)
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        print('Now Display Number' + str(self.lcdwidget.lcd.value()))
        if(self.state == 'START'):
            if(self.numberList[self.inputPositon] == 0):
                self.numberList[self.inputPositon] = int(buttonText)
            else:
                self.numberList[self.inputPositon] = self.numberList[self.inputPositon] * 10 + int(buttonText)
        else:
            if (self.numberList[self.inputPositon] == 0):
                self.numberList[self.inputPositon] = int(buttonText)
            else:
                if(self.state == 'DOT'):
                    self.numberList[self.inputPositon] = self.numberList[self.inputPositon] + int(buttonText) / 10
                else:
                    self.numberList[self.inputPositon] = self.numberList[self.inputPositon] * 10 + int(buttonText)
        self.lcdwidget.updateDisplay(self.numberList[self.inputPositon])

    def plusButtonClicked(self):
        clickedButton = self.sender()
        if(self.state != 'PLUS'):
            self.state = 'PLUS'
            self.lastPushOperator = clickedButton.text()
        else:
            self.numberList.append(self.calc(self.numberList.pop(0), self.lastPushOperator, self.numberList.pop(0)))
            self.numberList.append(0)
            self.lcdwidget.updateDisplay(self.numberList[self.displayPositon])

    def minusButtonClicked(self):
        clickedButton = self.sender()
        if(self.state != 'MINUS'):
            self.state = 'MINUS'
            self.lastPushOperator = clickedButton.text()
        else:
            self.numberList.append(self.calc(self.numberList.pop(0), self.lastPushOperator, self.numberList.pop(0)))
            self.numberList.append(0)
            self.lcdwidget.updateDisplay(self.numberList[self.displayPositon])

    def slashButtonClicked(self):
        clickedButton = self.sender()
        if(self.state != 'DIVIDE'):
            self.state = 'DIVIDE'
            self.lastPushOperator = clickedButton.text()
        else:
            self.numberList.append(self.calc(self.numberList.pop(0), self.lastPushOperator, self.numberList.pop(0)))
            self.numberList.append(0)
            self.lcdwidget.updateDisplay(self.numberList[self.displayPositon])

    def asterliskButtonClicked(self):
        clickedButton = self.sender()
        if(self.state != 'MULTIPLE'):
            self.state = 'MULTIPLE'
            self.lastPushOperator = clickedButton.text()
        else:
            self.numberList.append(self.calc(self.numberList.pop(0), self.lastPushOperator, self.numberList.pop(0)))
            self.numberList.append(0)
            self.lcdwidget.updateDisplay(self.numberList[self.displayPositon])

    def equalButtonClicked(self):
        clickedButton = self.sender()
        self.numberList.append(self.calc(self.numberList.pop(0), self.lastPushOperator, self.numberList.pop(0)))
        self.numberList.append(0)
        print('Ret Number : ' + str(self.numberList[self.displayPositon]))
        self.lastPushOperator = clickedButton.text()
        self.lcdwidget.updateDisplay(self.numberList[self.displayPositon])
        self.state = 'EQUAL'

    def dotButtonClicked(self):
        clickedButton = self.sender()
        buttonText = clickedButton.text()
        self.setState(buttonText)

    def clsButtonClicked(self):
        self.init()

    def bckButtonClicked(self):
        if(self.state == 'EQUAL'):
            self.numberList[self.displayPositon] = int(self.numberList[self.displayPositon] / 10)
            self.lcdwidget.updateDisplay(self.numberList[self.displayPositon])
        else:
            self.numberList[self.inputPositon] = int(self.numberList[self.inputPositon] / 10)
            self.lcdwidget.updateDisplay(self.numberList[self.inputPositon])


    def closeButtonClicked(self):
        sys.exit()

    def calc(self, leftNumber, operator, rightNumber):
        if(operator == '+'):
            return leftNumber + rightNumber
        if(operator == '-'):
            return leftNumber - rightNumber
        if(operator == '*'):
            return leftNumber * rightNumber
        if(operator == '/'):
            try:
                return leftNumber / rightNumber
            except ZeroDivisionError:
                print('ZeroDivisionError')
                self.init('ERROR')

    def init(self, STATUS='ALLCLEAR'):
        self.lastPushOperator = ''
        self.state = 'START'
        self.inputPositon = 0
        for i in range(len(self.numberList)):
            self.numberList[i] = 0
        if(STATUS == 'ERROR'):
            #ここ警告を出す等したい(何故か出ない)
            sys.exit()
        elif(STATUS == 'ALLCLEAR'):
            self.lcdwidget.updateDisplay(0)




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
       elif(buttonText == '='):
           print('setFlg!' + buttonText)
           self.state = 'EQUAL'

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