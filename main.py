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
logging.basicConfig(level=logging.INFO, format=format, filename='grid_trader_log.txt')
logger = logging.getLogger('binance')
from typing import Union
from gateway.binance_future import Interval
import numpy as np
import pandas as pd

pd.set_option('expand_frame_repr', False)

from utils.config import top_symbols


def get_data(trader: Union[BinanceFutureTrader, BinanceSpotTrader]):
    # traders.symbols 是一个字典.
    symbols = trader.symbols_dict.keys()

    datas = []
    # warning
    index = 0
    # end warning

    for symbol in symbols:
        klines = trader.get_klines(symbol=symbol, interval=Interval.HOUR_1, limit=100)
        if len(klines) > 0:
            df = pd.DataFrame(klines, dtype=np.float64,
                              columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'a1', 'a2',
                                       'a3', 'a4', 'a5'])
            df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]
            df.set_index('open_time', inplace=True)
            df.index = pd.to_datetime(df.index, unit='ms') + pd.Timedelta(hours=8)

            print(df)

            # 计算下他们涨跌幅度.
            pct = df['close'] / df['open'] - 1

            value = {'pct': pct[-1], 'symbol': symbol}
            datas.append(value)
        # warning
        index += 1

        if index > 5:
            break
    # end warning

    datas.sort(key=lambda x: x['pct'], reverse=True)
    top_symbols['id'] = top_symbols['id'] + 1
    top_symbols['symbols'] = datas


if __name__ == '__main__':

    config.loads('./config.json')

    if config.platform == 'binance_spot':
        trader = BinanceSpotTrader()
    else:
        trader = BinanceFutureTrader()

    trader.get_exchange_info()
    get_data(trader)

    scheduler = BackgroundScheduler()
    scheduler.add_job(get_data, trigger='cron', minute='*/10', args=(trader,))
    scheduler.start()

    while True:
        time.sleep(10)
        trader.start()

"""
策略逻辑
1. 每四个小时会挑选出前几个波动率最大的交易对(假设交易的是四个交易对).
2. 然后根据设置的参数进行下单(假设有两个仓位,那么波动率最大的两个，且他们过去一段时间是暴涨过的)
3. 然后让他们执行马丁策略.


"""
