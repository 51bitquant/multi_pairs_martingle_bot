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

import json


class Config:

    def __init__(self):

        self.platform: str = "binance_spot"  # 交易的平台
        self.api_key: str = None
        self.api_secret: str = None
        self.max_pairs = 4
        self.pump_pct = 0.03  # 需要涨多少以上才能进入交易池里面.
        self.initial_trade_value = 500
        self.trade_value_multiplier = 1.3
        self.increase_pos_when_drop_down = 0.05
        self.exit_profit_pct = 0.01  # 出场的利润.
        self.profit_pull_back_pct = 0.01  # 回调百分比.
        self.trading_fee = 0.0004  #
        self.max_increase_pos_count = 5
        self.proxy_host = ""  # proxy host
        self.proxy_port = 0  # proxy port


    def loads(self, config_file=None):
        """ Load config file.

        Args:
            config_file: config json file.
        """
        configures = {}
        if config_file:
            try:
                with open(config_file) as f:
                    data = f.read()
                    configures = json.loads(data)
            except Exception as e:
                print(e)
                exit(0)
            if not configures:
                print("config json file error!")
                exit(0)
        self._update(configures)

    def _update(self, update_fields):
        """
        更新update fields.
        :param update_fields:
        :return: None

        """

        for k, v in update_fields.items():
            setattr(self, k, v)


config = Config()
signal_data = {'id': 0, 'signals': []}
