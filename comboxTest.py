import sys
# import requests
# import pyupbit
# import json
# import time
import PyQt5

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  # thread 사용 시 필요
from PyQt5 import uic
# from PyQt5.QtGui import QIcon


form_class = uic.loadUiType("ui/combotest.ui")[0]  # ui 불러오는 부분

class MainWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox_setting()  # 밑에 만든 함수를 호출하는 기능
        self.comboBox.currentIndexChanged.connect(self.menu_select)  # 아래 함수 선언되면 항상 초기화자에 추가

    def comboBox_setting(self):
        menulist =['월요일','화요일','수요일','목요일','금요일']

        menulist = sorted(menulist)

        self.comboBox.addItems(menulist)

    # 이벤트 처리하는 함수(콤보박스 동작 부분)
    def menu_select(self):  #콤보박스 메뉴 변경시 호출되는 함수
        comboText = self.comboBox.currentText()  # 공식문서 signal part 찾아보면 됨

        self.output_label.setText(comboText)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())