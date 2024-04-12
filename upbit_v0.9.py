import sys
import requests
import pyupbit
import json
import time
import PyQt5

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  # thread 사용 시 필요
from PyQt5 import uic
from PyQt5.QtGui import QIcon


form_class = uic.loadUiType("ui/bitUp.ui")[0]  # ui 불러오는 부분

# signal class : 업비트서버에 요청을 보내 코인정보를 받아오는 일만 하는 클래스
class UpbitCall(QThread):
    # signal함수 선언
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)  # 필수
    # float: double보다 차지하는 메모리 양이 적다

    def __init__(self, ticker):  # signal class 객체가 선언될 때 MainWindow에서 코인 종류 받아오기
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):  # 필수
        while self.alive:  # 일단 무한루프 --> 나중에 멈추는 기능 추가 필요
            url = "https://api.upbit.com/v1/ticker"
            param = {"markets": f"KRW-{self.ticker}"}
            # url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"과 동일
            response = requests.get(url, params=param)

            result = response.json()

            trade_price = result[0]["trade_price"]  # 비트코인의 현재가
            high_price = result[0]["high_price"]
            low_price = result[0]["low_price"]
            prev_closing_price = result[0]["prev_closing_price"]  # 전일종가
            trade_volume = result[0]["trade_volume"]  # 최근 거래량
            acc_trade_volume_24h = result[0]["acc_trade_volume_24h"]  # 24시간 누적거래량
            acc_trade_price_24h = result[0]["acc_trade_price_24h"]  # 24시간 누적거래대금
            signed_change_rate = result[0]["signed_change_rate"]  # 부호가 있는 변화율

            # 받아온 부분을 보내주는 부분
            self.coinDataSent.emit(
                float(trade_price),
                float(high_price),
                float(low_price),
                float(prev_closing_price),
                float(trade_volume),
                float(acc_trade_volume_24h),
                float(acc_trade_price_24h),
                float(signed_change_rate)
            )

            # 업비트 호출 타임 딜레이 시킴
            time.sleep(5)

    def close(self):
        self.alive = False

# 위에서 불러온 값을 윈도우에 뿌려주는 부분
class MainWindow(QMainWindow, form_class):  # slot class
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("비트코인 정보 프로그램 v0.7")
        self.setWindowIcon(QIcon("icon/btc.png"))
        self.statusBar().showMessage("Upbit Api Application Ver 0.7")

        self.ticker = "BTC"

        self.ubc = UpbitCall(self.ticker)  # signal class로 객체 선언
        self.ubc.coinDataSent.connect(self.fillCoinData)
        # slot 함수 만들어서 연결해야 됨
        self.ubc.start()  # signal class run() 실행
        self.combobox_setting()  # 콤보박스 초기화 설정 함수
        self.coin_comboBox.currentIndexChanged.connect(self.coin_comboBox_selected)
        # 콤보박스의 메뉴 선택 변경 이벤트가 발생했을 때 호출될 함수 설정

    def combobox_setting(self):
        tickerList = coinTicker = pyupbit.get_tickers(fiat="KRW")  # 코인종류 가져오기

        coinList =[]

        # "KRW-" 부분 제거
        for ticker in tickerList:
            coinList.append(ticker[4:])

        coinList.remove("BTC")
        coinList = sorted(coinList)  # 정렬
        coinList = ["BTC"] + coinList

        self.coin_comboBox.addItems(coinList)

    def coin_comboBox_selected(self):  # 콤보박스에서 새로운 코인이 선택되었을 때 호출
        selected_ticker = self.coin_comboBox.currentText()  # 콤보박스에서 선택된 메뉴의 리스트 가져오기
        self.ticker =selected_ticker

        self.coin_ticker_label.setText(self.ticker)
        self.ubc.close()  # while문의 무한루프가 멈춤
        self.ubc = UpbitCall(self.ticker)  # signal class로 객체 선언
        self.ubc.coinDataSent.connect(self.fillCoinData)
        # slot 함수 만들어서 연결해야 됨
        self.ubc.start()  # signal class run() 실행


    def fillCoinData(self,
                     trade_price,
                     high_price,
                     low_price,
                     prev_closing_price,
                     trade_volume,
                     acc_trade_volume_24h,
                     acc_trade_price_24h,
                     signed_change_rate
    ):
        self.trade_price.setText(f"{trade_price:,.2f}원")
        self.high_price.setText(f"{high_price:,.2f}원")
        self.low_price.setText(f"{low_price:,.2f}원")
        self.prev_closing_price.setText(f"{prev_closing_price:,.2f}원")
        self.trade_volume.setText(f"{trade_volume:,.5f}개")
        self.acc_trade_volume_24h.setText(f"{acc_trade_volume_24h:,.3f}개")
        self.acc_trade_price_24h.setText(f"{acc_trade_price_24h:,.2f}개")
        self.signed_change_rate.setText(f"{signed_change_rate:,.9f}%")
        self.update_style()

    def update_style(self):  # 변화율의 +-에 따라 적, 청색 변화
        if "-" in self.signed_change_rate.text():
            self.signed_change_rate.setStyleSheet("background-color:blue;color:white;")
            self.trade_price.setStyleSheet("color:blue;")
        else:
            self.signed_change_rate.setStyleSheet("background-color:red;color:white;")
            self.trade_price.setStyleSheet("color:red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())






