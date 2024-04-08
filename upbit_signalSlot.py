import sys
import requests
import pyupbit
import json
import time
import PyQt5

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SignalThread(QThread):  # signal part
    signal1 = pyqtSignal()   # signal 함수
    signal2 = pyqtSignal(int, int)  # signal 함수

    def run(self):
        self.signal1.emit()
        self.signal2.emit(1000, 2000)

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        signalClass = SignalThread()

        signalClass.signal1.connect(self.signal1_print)
        # signal함수와  solt함수를 연결
        signalClass.signal2.connect(self.signal2_print)
        signalClass.run()

    @pyqtSlot()
    def signal1_print(self):  # slot 함수
        print("signal1이 제출됨(emit)!!")

    @pyqtSlot(int, int)
    def signal2_print(self, int1, int2):  # slot 함수
        print(f"signal2이 제출됨(emit)!! -->{int1}, {int2}")
        # 실제 프로그램에는 윈도우에 뿌려주는 내용이 옴

app = QApplication(sys.argv)
win = MainWin()
win.show()
sys.exit(app.exec_())



