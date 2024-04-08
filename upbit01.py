import requests
import pyupbit

# url = "https://api.upbit.com/v1/market/all?isDetails=true"
#
# headers = {"accept": "application/json"}
# res = requests.get(url, headers=headers)
# result = res.json()
# print(result[0]["market"])

coinTicker = pyupbit.get_tickers(fiat="KRW")


# print(coinTicker)

