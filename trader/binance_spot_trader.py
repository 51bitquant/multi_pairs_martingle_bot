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

from gateway import BinanceSpotHttp, OrderStatus, OrderType, OrderSide
from utils import config
from utils import round_to, floor_to
import logging
from datetime import datetime
from utils.config import signal_data
from utils.positions import Positions


class BinanceSpotTrader(object):
    """
        Disclaimer 免责声明:
        the binance spot trader, 币安现货马丁格尔策略.
        the Martingle strategy in Crypto Market will endure a lot of risk， use it before you understand the risk and martingle strategy, and the code may have bugs,
        Use it at your own risk. We won't ensure you will earn money from this code.
        马丁策略在合约上会有很大的风险，请注意风险, 使用前请熟知该代码，可能会有bugs或者其他未知的风险。

    """

    def __init__(self):
        """
        :param api_key:
        :param secret:
        :param trade_type: 交易的类型， only support future and spot.
        """
        self.http_client = BinanceSpotHttp(api_key=config.api_key, secret=config.api_secret,
                                           proxy_host=config.proxy_host, proxy_port=config.proxy_port)

        self.symbols_dict = {}  # 全市场的交易对.
        self.tickers_dict = {}  # 全市场的tickers数据.

        self.buy_orders_dict = {}  # 买单字典 buy orders {'symbol': [], 'symbol1': []}
        self.sell_orders_dict = {}  # 卖单字典. sell orders  {'symbol': [], 'symbol1': []}
        self.positions = Positions('spot_positions.json')
        self.initial_id = 0

    def get_exchange_info(self):
        data = self.http_client.get_exchange_info()
        if isinstance(data, dict):
            items = data.get('symbols', [])
            for item in items:

                symbol = item['symbol']
                if symbol.__contains__('UP') or symbol.__contains__('DOWN'):
                    # won't trade the UP and DOWN token.
                    continue

                if item.get('quoteAsset') == 'USDT' and item.get('status') == "TRADING":

                    symbol_data = {"symbol": symbol}
                    for filters in item['filters']:
                        if filters['filterType'] == 'PRICE_FILTER':
                            symbol_data['min_price'] = float(filters['tickSize'])
                        elif filters['filterType'] == 'LOT_SIZE':
                            symbol_data['min_qty'] = float(filters['stepSize'])
                        elif filters['filterType'] == 'MIN_NOTIONAL':
                            symbol_data['min_notional'] = float(filters['minNotional'])

                    self.symbols_dict[symbol] = symbol_data

    def get_all_tickers(self):

        tickers = self.http_client.get_all_tickers()
        if isinstance(tickers, list):
            for tick in tickers:
                symbol = tick['symbol']
                ticker = {"bid_price": float(tick['bidPrice']), "ask_price": float(tick["askPrice"])}
                self.tickers_dict[symbol] = ticker
        else:
            self.tickers_dict = {}

    def get_klines(self, symbol: str, interval, limit):
        return self.http_client.get_kline(symbol=symbol, interval=interval, limit=limit)

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

                        symbol = buy_order.get('symbol')
                        print(f"{symbol}: buy order was canceled,  time: {datetime.now()}")

                        min_qty = self.symbols_dict.get(symbol).get('min_qty', 0)
                        price = float(check_order.get('price'))
                        qty = float(check_order.get('executedQty', 0))

                        if qty > 0:
                            self.positions.update(symbol=symbol, trade_price=price, trade_amount=qty, min_qty=min_qty,
                                                  is_buy=True)

                            logging.info(
                                f"{symbol}: buy order was partially filled, price: {price}, qty: {qty}, time: {datetime.now()}")


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

                        symbol = sell_order.get('symbol')
                        print(f"{symbol}: sell order was canceled, time: {datetime.now()}")

                        min_qty = self.symbols_dict.get(symbol).get('min_qty', 0)
                        price = float(check_order.get('price'))
                        qty = float(check_order.get('executedQty', 0))

                        if qty > 0:
                            self.positions.update(symbol=symbol, trade_price=price, trade_amount=qty, min_qty=min_qty,
                                                  is_buy=False)

                            logging.info(
                                f"{symbol}: sell order was partially filled, price: {price}, qty: {qty}, total_profit: {self.positions.total_profit}, time: {datetime.now()}")


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
                        print(f"sell order status is: New, time: {datetime.now()}")
                    else:
                        print(
                            f"sell order status is not in above options: {check_order.get('status')}, time: {datetime.now()}")

        # the expired\canceled\delete orders
        for delete_order in delete_sell_orders:
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

        deleted_positions = []
        for s in symbols:
            pos_data = self.positions.positions.get(s)
            pos = pos_data.get('pos')
            bid_price = self.tickers_dict.get(s, {}).get('bid_price', 0)  # bid price
            ask_price = self.tickers_dict.get(s, {}).get('ask_price', 0)  # ask price

            min_qty = self.symbols_dict.get(s, {}).get('min_qty')
            min_price = self.symbols_dict.get(s, {}).get("min_price")

            if bid_price > 0 and ask_price > 0:
                value = pos * bid_price
                if value < self.symbols_dict.get(s, {}).get('min_notional', 0):
                    print(f"{s} notional value is small, delete the position data.")
                    deleted_positions.append(s)  #
                    # del self.positions.positions[s]  # delete the position data if the position notional is very small.
                else:
                    avg_price = pos_data.get('avg_price')
                    self.positions.update_profit_max_price(s, bid_price)
                    # calculate profit 计算利润.
                    profit_pct = bid_price / avg_price - 1
                    drawdown_pct = pos_data.get('profit_max_price', 0) / bid_price - 1

                    dump_pct = pos_data.get('last_entry_price', 0) / bid_price - 1
                    current_increase_pos_count = pos_data.get('current_increase_pos_count',1)

                    loss_pct = avg_price / bid_price - 1  # loss percent.

                    # there is profit here, consider whether exit this position.
                    if profit_pct >= config.exit_profit_pct and drawdown_pct >= config.profit_drawdown_pct and len(self.sell_orders_dict.get(s, [])) <= 0:
                        """
                        the position is profitable and drawdown meets requirements.
                        """

                        # cancel the buy orders. when we want to place sell orders, we need to cancel the buy orders.
                        buy_orders = self.buy_orders_dict.get(s, [])
                        for buy_order in buy_orders:
                            print(
                                "cancel the buy orders and send the profit order.")
                            self.http_client.cancel_order(s, buy_order.get('clientOrderId'))
                        # the price tick and quantity precision.

                        qty = floor_to(abs(pos), min_qty)
                        price = round_to(bid_price, min_price)

                        sell_order = self.http_client.place_order(symbol=s, order_side=OrderSide.SELL,
                                                                  order_type=OrderType.LIMIT, quantity=qty,
                                                                  price=price)

                        if sell_order:
                            # resolve sell order
                            orders = self.sell_orders_dict.get(s, [])
                            orders.append(sell_order)
                            self.sell_orders_dict[s] = orders

                    elif loss_pct >= config.stop_loss_pct > 0 and len(self.sell_orders_dict.get(s, [])) <= 0:
                        # set the stop loss
                        # cancel the buy orders. when we want to place sell orders, we need to cancel the buy orders.
                        buy_orders = self.buy_orders_dict.get(s, [])
                        for buy_order in buy_orders:
                            print(
                                "cancel the buy orders and send the sell order for stop loss.")
                            self.http_client.cancel_order(s, buy_order.get('clientOrderId'))
                        # the price tick and quantity precision.

                        qty = floor_to(abs(pos), min_qty)
                        price = round_to(bid_price, min_price)

                        sell_order = self.http_client.place_order(symbol=s, order_side=OrderSide.SELL,
                                                                  order_type=OrderType.LIMIT, quantity=qty,
                                                                  price=price)

                        if sell_order:
                            # resolve sell order
                            orders = self.sell_orders_dict.get(s, [])
                            orders.append(sell_order)
                            self.sell_orders_dict[s] = orders

                    elif dump_pct >= config.increase_pos_when_drop_down and len(self.buy_orders_dict.get(s,
                                                                                                         [])) <= 0 and current_increase_pos_count <= config.max_increase_pos_count:

                        # if the market price continue drop down you can increase your positions.
                        # cancel the sell orders, when we want to place buy orders, we need to cancel the sell orders.
                        sell_orders = self.sell_orders_dict.get(s, [])
                        for sell_order in sell_orders:
                            print(
                                "cancel the sell orders, when we want to place buy orders, we need to cancel the sell orders")
                            self.http_client.cancel_order(s, sell_order.get('clientOrderId'))

                        buy_value = config.initial_trade_value * config.trade_value_multiplier ** current_increase_pos_count

                        qty = floor_to(buy_value / ask_price, min_qty)
                        price = round_to(ask_price, min_price)

                        buy_order = self.http_client.place_order(symbol=s, order_side=OrderSide.BUY,
                                                                 order_type=OrderType.LIMIT, quantity=qty,
                                                                 price=price)
                        if buy_order:
                            # resolve buy orders
                            orders = self.buy_orders_dict.get(s, [])
                            orders.append(buy_order)

                            self.buy_orders_dict[s] = orders

            else:
                print(f"{s}: bid_price: {bid_price}, ask_price: {bid_price}")

        for s in deleted_positions:
            del self.positions.positions[s]  # delete the position data if the position notional is very small.

        self.positions.save_data()
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
            s = signal['symbol']
            if signal['signal'] == 1 and index < left_times and s not in pos_symbols and signal[
                'hour_turnover'] >= config.turnover_threshold:
                ## allowed_lists and blocked_lists cannot be satisfied at the same time
                if len(config.allowed_lists) > 0 and s in config.allowed_lists:
                    index += 1
                    # the last one hour's the symbol jump over some percent.
                    self.place_order(s, signal['pct'], signal['pct_4h'])

                if s not in config.blocked_lists and len(config.allowed_lists) == 0:
                    index += 1
                    self.place_order(s, signal['pct'], signal['pct_4h'])

                if len(config.allowed_lists) == 0 and config.blocked_lists == 0:
                    index += 1
                    self.place_order(s, signal['pct'], signal['pct_4h'])

    def place_order(self, symbol: str, hour_change: float, four_hour_change: float):

        buy_value = config.initial_trade_value

        min_price = self.symbols_dict.get(symbol, {}).get("min_price")
        min_qty = self.symbols_dict.get(symbol, {}).get('min_qty')
        ask_price = self.tickers_dict.get(symbol, {}).get('ask_price', 0)  # ask price
        if ask_price <= 0:
            logging.error(f"error -> spot {symbol} ask_price is :{ask_price}")
            return

        price = round_to(ask_price, min_price)
        qty = floor_to(buy_value / ask_price, min_qty)

        buy_order = self.http_client.place_order(symbol=symbol, order_side=OrderSide.BUY,
                                                 order_type=OrderType.LIMIT, quantity=qty,
                                                 price=price)

        print(
            f"{symbol} hour change: {hour_change}, 4hour change: {four_hour_change}, place buy order: {buy_order}")
        if buy_order:
            # resolve buy orders
            orders = self.buy_orders_dict.get(symbol, [])
            orders.append(buy_order)
            self.buy_orders_dict[symbol] = orders
