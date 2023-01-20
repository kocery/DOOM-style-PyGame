from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class Setting_W(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('assets/settings.ui', self)

        self.pushButton.clicked.connect(self.apply)

    def apply(self):
        RES = WIDTH, HEIGHT = list(map(int, self.lineEdit.text().split(',')))
        MOUSE_SENSITIVITY = float(self.lineEdit_2.text())
        with open('settings.txt', 'w') as f:
            f.write(f'{RES}\n{WIDTH}\n{HEIGHT}\n{MOUSE_SENSITIVITY}')
