import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLCDNumber
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
        lcd = QLCDNumber(self)
        layout = QVBoxLayout()

        #液晶部分が自動伸長する設定
        lcd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(lcd)

        self.setLayout(layout)

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
        # 電卓のボタン配置
        for position, name in zip(positions, names):

            if name == '':
                continue
            button = QPushButton(name)
            layout.addWidget(button, *position)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = QWidget()
    lcd_widget = LCDWidget()
    pushbutton_widget = PushButtonWidget()
    #作成した液晶画面と、ボタンをメインウィンドウに上下に配置
    panel_layout = QVBoxLayout()
    panel_layout.addWidget(lcd_widget)
    panel_layout.addWidget(pushbutton_widget)
    panel.setLayout(panel_layout)

    # メインウィンドウ描画
    main_window = QMainWindow()
    main_window.setGeometry(300, 300, 390, 300)
    main_window.setCentralWidget(panel)
    main_window.setWindowTitle('Calculator')
    main_window.show()
    sys.exit(app.exec_())