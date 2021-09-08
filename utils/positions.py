# -*- coding:utf-8 -*-
"""

    币安推荐码:  返佣10%
    https://www.binancezh.pro/cn/register?ref=AIR1GC70

    币安合约推荐码: 返佣10%
    https://www.binancezh.com/cn/futures/ref/51bitquant

    if you don't have a binance account, you can use the invitation link to register one:
    https://www.binancezh.com/cn/futures/ref/51bitquant

    or use the inviation code: 51bitquant

    网格交易: 适合币圈的高波动率的品种，适合现货， 如果交易合约，需要注意防止极端行情爆仓。


    服务器购买地址: https://www.ucloud.cn/site/global.html?invitation_code=C1x2EA81CD79B8C#dongjing
"""
from utils.config import config
from utils.utility import get_file_path, load_json, save_json


class Positions:

    def __init__(self, file_name):
        self.file_name = file_name
        self.positions = {}
        self.total_profit = 0
        self.read_data()  # read the saved data

    def read_data(self):
        filepath = get_file_path(self.file_name)
        data = load_json(filepath)
        if not bool(data):
            data['total_profit'] = self.total_profit
            data['positions'] = self.positions
        else:
            self.total_profit = float(data.get('total_profit', 0))
            self.positions = data.get('positions', {})

    def save_data(self):
        filename = get_file_path(self.file_name)
        save_json(filename, {'total_profit': self.total_profit, 'positions': self.positions})

    def update(self, symbol: str, trade_amount: float, trade_price: float, min_qty: float, is_buy: bool = False):
        """
        :param symbol:
        :param trade_amount:
        :param trade_price:
        :param is_buy:
        :return:
        """
        pos = self.positions.get(symbol, None)
        if pos is None:
            #
            pos = {'symbol': symbol, 'pos': 0, 'avg_price': 0, 'last_entry_price': 0, 'current_increase_pos_count': 0,
                   'profit_max_price': 0}

        if is_buy:
            pos['current_increase_pos_count'] = pos['current_increase_pos_count'] + 1
            pos['avg_price'] = (trade_amount * trade_price + pos['avg_price'] * pos['pos']) / (
                    trade_amount + pos['pos'])
            pos['pos'] = trade_amount + pos['pos']
            pos['last_entry_price'] = trade_price

        else:
            self.total_profit += (trade_price - pos[
                'avg_price']) * trade_amount - 2 * trade_amount * trade_price * config.trading_fee
            pos['pos'] = pos['pos'] - trade_amount

        if pos['pos'] < min_qty:
            if self.positions.get(symbol, None):
                del self.positions[symbol]
        else:
            self.positions[symbol] = pos

    def update_profit_max_price(self, symbol: str, price: float):
        """
        :param symbol:
        :param price:
        :return:
        """
        if self.positions.get(symbol, None):
            self.positions[symbol]['profit_max_price'] = max(price, self.positions[symbol]['profit_max_price'])
