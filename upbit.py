import requests
import json

import time

while True:
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    # url = "https://api.upbit.com/v1/ticker?markets=KRW-ETH"

    response = requests.get(url)


    # print(response.text)

    result = response.json()
    print(result[0]['trade_price'])
    time.sleep(5)

