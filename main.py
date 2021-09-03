"""
    币安推荐码:  返佣10%
    https://www.binancezh.pro/cn/register?ref=AIR1GC70

    币安合约推荐码: 返佣10%
    https://www.binancezh.com/cn/futures/ref/51bitquant

    if you don't have a binance account, you can use the invitation link to register one:
    https://www.binancezh.com/cn/futures/ref/51bitquant

    or use the inviation code: 51bitquant

    风险提示: 网格交易在单边行情的时候，会承受比较大的风险，请你了解整个代码的逻辑，然后再使用。
    RISK NOTE: Grid trading will endure great risk at trend market, please check the code before use it. USE AT YOUR OWN RISK.

"""

import time
import logging
from trader.binance_spot_trader import BinanceSpotTrader
from trader.binance_future_trader import BinanceFutureTrader
from utils import config
from apscheduler.schedulers.background import BackgroundScheduler

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=format, filename='log.txt')
logger = logging.getLogger('binance')
from typing import Union
from gateway.binance_future import Interval
import numpy as np
import pandas as pd
from datetime import datetime

pd.set_option('expand_frame_repr', False)

from utils.config import signal_data


def get_data(trader: Union[BinanceFutureTrader, BinanceSpotTrader]):
    # traders.symbols is a dict data structure.
    symbols = trader.symbols_dict.keys()

    signals = []

    # we calculate the signal here.
    for symbol in symbols:
        klines = trader.get_klines(symbol=symbol, interval=Interval.HOUR_1, limit=100)
        if len(klines) > 0:
            df = pd.DataFrame(klines, dtype=np.float64,
                              columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'a1', 'a2',
                                       'a3', 'a4', 'a5'])
            df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]
            df.set_index('open_time', inplace=True)
            df.index = pd.to_datetime(df.index, unit='ms') + pd.Timedelta(hours=8)

            df_4hour = df.resample(rule='4H').agg({'open': 'first',
                                        'high': 'max',
                                        'low': 'min',
                                        'close': 'last',
                                        'volume': 'sum'
                                        })

            # print(df)

            # calculate the pair's price change is one hour. you can modify the code below.
            pct = df['close'] / df['open'] - 1
            pct_4h = df_4hour['close']/df_4hour['open'] - 1

            value = {'pct': pct[-1], 'pct_4h':pct_4h[-1] , 'symbol': symbol}


            # calculate your signal here.
            if value['pct'] >= config.pump_pct or value['pct_4h'] >= config.pump_pct_4h:
                # the signal 1 mean buy signal.
                value['signal'] = 1
            elif value['pct'] <= -config.pump_pct or value['pct_4h'] <= -config.pump_pct_4h:
                value['signal'] = -1
            else:
                value['signal'] = 0

            signals.append(value)

    signals.sort(key=lambda x: x['pct'], reverse=True)
    signal_data['id'] = signal_data['id'] + 1
    signal_data['time'] = datetime.now()
    signal_data['signals'] = signals
    print(signal_data)

if __name__ == '__main__':

    config.loads('./config.json')

    if config.platform == 'binance_spot':
        trader = BinanceSpotTrader()
    else:
        trader = BinanceFutureTrader()

    trader.get_exchange_info()
    get_data(trader)  # for testing

    scheduler = BackgroundScheduler()
    scheduler.add_job(get_data, trigger='cron', hour='*/1', args=(trader,))
    scheduler.start()

    while True:
        time.sleep(10)
        trader.start()

"""
strategy idea: 

1. 每1个小时会挑选出前几个波动率最大的交易对(假设交易的是四个交易对).
2. 然后根据设置的参数进行下单(假设有两个仓位,那么波动率最大的两个，且他们过去一段时间是暴涨过的)
3. 然后让他们执行马丁策略.

"""
