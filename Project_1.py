from alpaca.data import StockHistoricalDataClient,TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.requests import OrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
import pandas as pd
import random
import numpy as np
from alpaca.trading.client import TradingClient
import time

api_key = ''
api_secret = ''
base_url = 'https://paper-api.alpaca.markets'  # Use paper trading base URL for testing
client = StockHistoricalDataClient(api_key,api_secret)
trading_client = TradingClient(api_key, api_secret, paper=True)


# selection = random.sample(range(504), 5)
# symbol = pd.read_csv("constituents_csv.csv")
# symbol_list = []
# for i in selection:
#     s = symbol.iloc[i]["Symbol"]
#     symbol_list.append(s)
# start_time = pd.to_datetime("2024-02-13").tz_localize('America/New_York')
# end_time = pd.to_datetime("2024-02-14").tz_localize('America/New_York')
#
# for i in range(5):
#     request_params = StockBarsRequest(
#         symbol_or_symbols=symbol_list[i],
#         timeframe=TimeFrame.Minute,
#         start=start_time
#         )
#     data = client.get_stock_bars(request_params).df.tz_convert('America/New_York',level=1)
#     name = "data" + str(i) + ".csv"
#     data.to_csv(name)

def Strategy(period):
    signal = []
    flag = False
    for i in range(period):
        if flag == False:
            s = random.randint(0,1)
            if s == 0:
                signal.append(0)
                flag = True
            else:
                signal.append(-1)
        else:
            s = random.randint(0,1)
            if s == 1:
                signal.append(1)
                flag = False
            else:
                signal.append(-1)
    if flag == True:
        if signal[-1] != 0:
            signal.pop()
            signal.append(1)
        else:
            signal.pop()
            signal.append(-1)
    return np.array(signal)

def Backtest(data,signal):
    buy = []
    sell = []
    for i in range(len(signal)):
        if signal[i] == 0:
            buy.append(data.iloc[i]["close"])
        if signal[i] == 1:
            sell.append(data.iloc[i]["close"])
    b = np.array(buy)
    s = np.array(sell)
    rate = (s-b)/b
    return rate.sum()

ROR = 0.0
for i in range(5):
    name = "data" + str(i) +".csv"
    data = pd.read_csv(name)
    ROR +=Backtest(data,Strategy(len(data)))
print(ROR)

symbol = pd.read_csv("constituents_csv.csv")
def paper_trading(symbol_list):
    while True:
        selection = random.sample(range(504), 5)
        symbol = []
        for i in selection:
            s = symbol_list.iloc[i]["Symbol"]
            symbol.append(s)
        account = trading_client.get_account()
        while float(account.cash) < 90000:
            account = trading_client.get_account()
        value = float(account.cash)/5
        for i in range(5):
            print(value)
            request_params_buy = OrderRequest(
                symbol = symbol[i],
                notional=int(value),
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                time_in_force=TimeInForce.DAY
                )
            trading_client.submit_order(request_params_buy)
        time.sleep(300)
        position = trading_client.get_all_positions()
        if len(position) != 0:
            for i in range(len(position)):
                request_params_sell = OrderRequest(
                    symbol = position[i].symbol,
                    qty=position[i].qty,
                    side=OrderSide.SELL,
                    type=OrderType.MARKET,
                    time_in_force=TimeInForce.DAY
                    )
                trading_client.submit_order(request_params_sell)

paper_trading(symbol)