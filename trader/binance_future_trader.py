"""
    币安推荐码:  返佣10%
    https://www.binancezh.pro/cn/register?ref=AIR1GC70

    币安合约推荐码: 返佣10%
    https://www.binancezh.com/cn/futures/ref/51bitquant

    if you don't have a binance account, you can use the invitation link to register one:
    https://www.binancezh.com/cn/futures/ref/51bitquant

    or use the inviation code: 51bitquant

    服务器购买地址: https://www.ucloud.cn/site/global.html?invitation_code=C1x2EA81CD79B8C#dongjing
    The Multi-Pairs Martingle Trading Bot
"""

from gateway import BinanceFutureHttp, OrderStatus, OrderType, OrderSide
from utils import config
from utils import round_to
import logging
from datetime import datetime
from utils.config import signal_data
from utils.positions import Positions


class BinanceFutureTrader(object):

    def __init__(self):
        """
        the binance future trader, 币安合约交易的网格交易,
        the grid trading in Future will endure a lot of risk， use it before you understand the risk and grid strategy.
        网格交易在合约上会有很大的风险，请注意风险
        """

        self.http_client = BinanceFutureHttp(api_key=config.api_key, secret=config.api_secret,
                                             proxy_host=config.proxy_host, proxy_port=config.proxy_port)

        self.symbols_dict = {}  # 全市场的交易对.
        self.tickers_dict = {}  # 全市场的tickers数据.

        self.buy_orders_dict = {}  # 买单字典 buy orders {'symbol': [], 'symbol1': []}
        self.sell_orders_dict = {}  # 卖单字典. sell orders  {'symbol': [], 'symbol1': []}
        self.positions = Positions()
        self.initial_id = 0

    def get_exchange_info(self):
        data = self.http_client.exchangeInfo()

        if isinstance(data, dict):
            items = data.get('symbols', [])
            for item in items:
                if item.get('quoteAsset') == 'USDT' and item.get('status') == "TRADING":

                    symbol = item['symbol']
                    symbol_data = {"symbol": symbol}

                    for filters in item['filters']:
                        if filters['filterType'] == 'PRICE_FILTER':
                            symbol_data['min_price'] = float(filters['tickSize'])
                        elif filters['filterType'] == 'LOT_SIZE':
                            symbol_data['min_qty'] = float(filters['stepSize'])
                        elif filters['filterType'] == 'MIN_NOTIONAL':
                            symbol_data['min_notional'] = float(filters['notional'])

                    self.symbols_dict[symbol] = symbol_data

        # print(len(self.symbols),self.symbols)  # 129 个交易对.

    def get_klines(self, symbol: str, interval, limit):
        return self.http_client.get_kline(symbol=symbol, interval=interval, limit=limit)

    def get_all_tickers(self):

        tickers = self.http_client.get_all_tickers()
        if isinstance(tickers, list):
            for tick in tickers:
                symbol = tick['symbol']
                ticker = {"bid_price": float(tick['bidPrice']), "ask_price": float(tick["askPrice"])}
                self.tickers_dict[symbol] = ticker
        else:
            self.tickers_dict = {}

    def start(self):
        """
        执行核心逻辑，网格交易的逻辑.

        the grid trading logic
        :return:
        """

        delete_buy_orders = []  # the buy orders need to remove from buy_orders[] list
        delete_sell_orders = []  # the sell orders need to remove from sell_orders[] list

        # 买单逻辑,检查成交的情况.

        for key in self.buy_orders_dict.keys():
            for buy_order in self.buy_orders_dict.get(key, []):
                check_order = self.http_client.get_order(buy_order.get('symbol'),
                                                         client_order_id=buy_order.get('clientOrderId'))

                if check_order:
                    if check_order.get('status') == OrderStatus.CANCELED.value:
                        delete_buy_orders.append(buy_order)

                        print(f"{buy_order.get('symbol')}: buy order was canceled, time: {datetime.now()}")

                    elif check_order.get('status') == OrderStatus.FILLED.value:
                        delete_buy_orders.append(buy_order)
                        # 买单成交，挂卖单.
                        symbol = buy_order.get('symbol')
                        price = float(check_order.get('price'))
                        qty = float(check_order.get('origQty'))
                        min_qty = self.symbols_dict.get(symbol).get('min_qty', 0)

                        self.positions.update(symbol=symbol, trade_price=price, trade_amount=qty, min_qty=min_qty,
                                              is_buy=True)

                        logging.info(
                            f"{symbol}: buy order was filled, price: {price}, qty: {qty}, time: {datetime.now()}")


                    elif check_order.get('status') == OrderStatus.NEW.value:
                        print(f"{buy_order.get('symbol')}: buy order is new, time: {datetime.now()}")

                    else:
                        print(
                            f"{buy_order.get('symbol')} buy order's status is not in above options, status: {check_order.get('status')}, time: {datetime.now()}")

        # the expired\canceled\delete orders
        for delete_order in delete_buy_orders:
            for key in self.buy_orders_dict.keys():
                orders = self.buy_orders_dict.get(key, [])
                if delete_order in orders:
                    orders.remove(delete_order)

        # 卖单逻辑, 检查卖单成交情况.
        for key in self.sell_orders_dict.keys():
            for sell_order in self.sell_orders_dict.get(key, []):
                check_order = self.http_client.get_order(sell_order.get('symbol'),
                                                         client_order_id=sell_order.get('clientOrderId'))
                if check_order:
                    if check_order.get('status') == OrderStatus.CANCELED.value:
                        delete_sell_orders.append(sell_order)

                        print(f"{sell_order.get('symbol')}: sell order was canceled, time: {datetime.now()}")
                    elif check_order.get('status') == OrderStatus.FILLED.value:
                        delete_sell_orders.append(sell_order)

                        symbol = check_order.get('symbol')
                        price = float(check_order.get('price'))
                        qty = float(check_order.get('origQty'))

                        min_qty = self.symbols_dict.get(symbol).get('min_qty', 0)
                        self.positions.update(symbol=symbol, trade_price=price, trade_amount=qty, min_qty=min_qty,
                                              is_buy=False)

                        logging.info(
                            f"{symbol}: sell order was filled, price: {price}, qty: {qty}, total_profit: {self.positions.total_profit}, time: {datetime.now()}")


                    elif check_order.get('status') == OrderStatus.NEW.value:
                        print(f"sell order status is: New, 时间: {datetime.now()}")
                    else:
                        print(
                            f"sell order status is not in above options: {check_order.get('status')}, 时间: {datetime.now()}")

        # the expired\canceled\delete orders
        for delete_order in delete_buy_orders:
            for key in self.sell_orders_dict.keys():
                orders = self.sell_orders_dict.get(key, [])
                if delete_order in orders:
                    orders.remove(delete_order)

        ####################################
        """
        check about the current position and order status.
        """

        self.get_all_tickers()
        if len(self.tickers_dict.keys()) == 0:
            return

        symbols = self.positions.positions.keys()

        for s in symbols:
            pos_data = self.positions.positions.get(s)
            pos = pos_data.get('pos')
            bid_price = self.tickers_dict.get(s, {}).get('bid_price', 0)  # bid price
            ask_price = self.tickers_dict.get(s, {}).get('ask_price', 0)  # ask price

            min_qty = self.symbols_dict.get(s, {}).get('min_qty')

            if bid_price > 0 and ask_price > 0:
                value = pos * bid_price
                if value < self.symbols_dict.get(s, {}).get('min_notional', 0):
                    print(f"{s} 的仓位价值小于最小的仓位价值, 所以删除了该交易对的仓位.")
                    del self.positions.positions[s]  # 删除仓位价值比较小的交易对.
                else:
                    avg_price = pos_data.get('avg_price')
                    self.positions.update_profit_max_price(s, bid_price)
                    # 计算利润.
                    profit_pct = bid_price / avg_price - 1
                    pull_back_pct = self.positions.positions.get(s, {}).get('profit_max_price', 0) / bid_price - 1

                    dump_pct = self.positions.positions.get(s, {}).get('last_entry_price', 0) / bid_price - 1
                    current_increase_pos_count = self.positions.positions.get(s, {}).get('current_increase_pos_count',
                                                                                         1)

                    # 判断是否是有利润，然后考虑出场.
                    if profit_pct >= config.exit_profit_pct and pull_back_pct >= config.profit_pull_back_pct and len(
                            self.sell_orders_dict.get(s, [])) <= 0:
                        """
                        the position has the profit and pull back meet requirements.
                        """

                        # cancel the buy orders. when we want to place sell orders, we need to cancel the buy orders.
                        buy_orders = self.buy_orders_dict.get(s, [])
                        for buy_order in buy_orders:
                            print(
                                "cancel the buy orders. when we want to place sell orders, we need to cancel the buy orders.")
                            self.http_client.cancel_order(s, buy_order.get('clientOrderId'))
                        # 处理价格和精度.
                        qty = round_to(abs(pos), min_qty)

                        sell_order = self.http_client.place_order(symbol=s, order_side=OrderSide.SELL,
                                                                  order_type=OrderType.LIMIT, quantity=qty,
                                                                  price=bid_price)

                        if sell_order:
                            # resolve sell order
                            orders = self.sell_orders_dict.get(s, [])
                            orders.append(sell_order)
                            self.sell_orders_dict[s] = orders

                    # if the market price continue drop down you can increase your positions.

                    elif dump_pct >= config.increase_pos_when_drop_down and len(self.buy_orders_dict.get(s,
                                                                                                         [])) <= 0 and current_increase_pos_count <= config.max_increase_pos_count:

                        # cancel the sell orders, when we want to place buy orders, we need to cancel the sell orders.
                        sell_orders = self.sell_orders_dict.get(s, [])
                        for sell_order in sell_orders:
                            print(
                                "cancel the sell orders, when we want to place buy orders, we need to cancel the sell orders")
                            self.http_client.cancel_order(s, sell_order.get('clientOrderId'))

                        buy_value = config.initial_trade_value * config.trade_value_multiplier ** current_increase_pos_count

                        qty = round_to(buy_value / bid_price, min_qty)

                        buy_order = self.http_client.place_order(symbol=s, order_side=OrderSide.BUY,
                                                                 order_type=OrderType.LIMIT, quantity=qty,
                                                                 price=bid_price)
                        if buy_order:
                            # resolve buy orders
                            orders = self.buy_orders_dict.get(s, [])
                            orders.append(buy_order)

                            self.buy_orders_dict[s] = orders

            else:
                print(f"{s}: bid_price: {bid_price}, ask_price: {bid_price}")

        pos_symbols = self.positions.positions.keys()  # 有仓位的交易对信息.
        pos_count = len(pos_symbols)  # 仓位的个数.

        left_times = config.max_pairs - pos_count

        if self.initial_id == signal_data.get('id', self.initial_id):
            # the id is not updated, indicates that the data is not updated.
            # print("the current initial_id is the same, we do nothing.")
            return

        self.initial_id = signal_data.get('id', self.initial_id)

        index = 0
        for signal in signal_data.get('signals', []):
            if signal['signal'] == 1 and index < left_times and signal['symbol'] not in pos_symbols:

                index += 1
                s = signal['symbol']
                # the last one hour's the symbol jump over some percent.

                buy_value = config.initial_trade_value
                min_qty = self.symbols_dict.get(s, {}).get('min_qty')
                bid_price = self.tickers_dict.get(s, {}).get('bid_price', 0)  # bid price
                if bid_price <= 0:
                    print(f"error -> future {s} bid_price is :{bid_price}")
                    return

                qty = round_to(buy_value / bid_price, min_qty)

                buy_order = self.http_client.place_order(symbol=s, order_side=OrderSide.BUY,
                                                         order_type=OrderType.LIMIT, quantity=qty,
                                                         price=bid_price)
                print(f"{s} price change is {signal['pct']}, place buy order: {buy_order}")
                if buy_order:
                    # resolve buy orders
                    orders = self.buy_orders_dict.get(s, [])
                    orders.append(buy_order)
                    self.buy_orders_dict[s] = orders


            else:
                pass
