# multi_pairs_martingle_bot English Documentation
 A muti pairs martingle trading bot for Binance exchange.

### Configuration

```
 {
  "platform": "binance_future",
  "api_key": "xxxx",
  "api_secret": "xxxxx",
  "max_pairs": 4,
  "pump_pct": 0.026,
  "pump_pct_4h": 0.045,
  "initial_trade_value": 200,
  "trade_value_multiplier": 1.5,
  "increase_pos_when_drop_down": 0.05,
  "exit_profit_pct": 0.01,
  "profit_pull_back_pct": 0.01,
  "trading_fee": 0.0004,
  "max_increase_pos_count": 5,
  "turnover_threshold": 100000,
  "blocked_lists": [
    "BTCUSDT",
    "ADAUSDT"
  ],
  "allowed_lists": [],
  "proxy_host": "",
  "proxy_port": 0
}


```

1. platform: binance_future for Binance Future Exchange, binance_spot
   for Binance Spot Exchange
2. api_key: api key from Binance exchange api key
3. api_secret: api secret from Binance exchange.
4. max_pairs: the max number of pair you want to trade.
5. pump_pct: the price will jump pct in one hour.
6. initial_trade_value: the first order you want to trade.
7. increase_pos_when_drop_down: after entering a position, you want to
   increase your position when the price go down some percentage.

8. exit_profit_pct: exit your position when you get profit.

9. profit_pull_back_pct: pull back

10. trading_fee: trading fee rate.
 
11. max_increase_pos_count: how many times you want to increase your
    positions

12. turnover_threshold: the pair's trading value should be over this
    value, the default value is 100,000 USDT.
13. blocked_lists: if you don't want to trade the symbols/pairs, put it
    here likes ['XMLUSDT', 'XRPUSDT'], 
    
14. allowed_lists: if you only want to trade some specific pairs, put it
    here, like : ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']

15. proxy_host: proxy host ip location like '132.148.123.22'

16. proxy_port: proxy port like : 8888, 9999 ect.

### how-to use
1. just config your config.json file, past your api key and secret from
   Binance, and modify your settings in config.json file.
2. run the main.py file, or you can use shell script by sh start.sh



### contact me
Wechat: bitquant51


# 强势币多交易对马丁策略机器人
多个交易对的马丁格尔策略。可以在币安上交易现货或者合约。

###配置文件

```
 {
  "platform": "binance_future",
  "api_key": "xxxx",
  "api_secret": "xxxxx",
  "max_pairs": 4,
  "pump_pct": 0.03,
  "initial_trade_value": 500,
  "trade_value_multiplier": 1.3,
  "increase_pos_when_drop_down": 0.05,
  "exit_profit_pct": 0.01,
  "profit_pull_back_pct": 0.01,
  "trading_fee": 0.0004,
  "max_increase_pos_count": 5,
  "proxy_host": "",
  "proxy_port": 0
}

```
配置文件的参数说明。

1. platform: 可选的值有两个,分别是binance_future和binance_spot，
   如果你想交易现货，就填写binance_spot, 合约就写binance_future
2. api_key: 币安交易所的api key
3. api_secret: 币安交易所的api secret
4. max_pairs: 交易对的最大数量，如果你想同时持仓10个交易对，那么这里就写10.
5. pump_pct: 小时线暴涨百分之多少后入场,
   当然你可以修改源码，修改你的入场逻辑。这个策略的思路是挑选小时暴涨的币，然后用马丁格尔的策略去交易。
6. initial_trade_value: 每个交易对的初始交易金额
7. increase_pos_when_drop_down: 回调多少后加仓。

8. exit_profit_pct: 出场点位

9. profit_pull_back_pct: 最高值回调多少后，且有利润的时候才出场.

10. trading_fee: 交易的资金费率。
 
11. max_increase_pos_count: 最大的加仓次数.
    
12. turnover_threshold:
    这个是过滤值，就是要求一小时的最低成交量不能低于多少，默认是值 100,000 USDT.
13. blocked_lists:
    这个是禁止交易的交易对，如果你想过滤某写不想交易的山寨币，你可以把他们放在这个列表上如:
    ['XMLUSDT', 'XRPUSDT'],
    
14. allowed_lists: 如果你只想交易某一些交易对，那么放这里:
    ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']

15. proxy_host: 代理主机ip地址： 如'132.148.123.22'

16. proxy_port: 代理主机的端口号如: 8888, 9999 ect.


### 如何使用
1. 把代码下载下来，然后编辑config.json文件，它会读取你这个配置文件，记得填写你的交易所的api
   key 和 secret, 然后保存该配置文件，配置文件选项的说明如上面描述。
2. 直接运行main.py文件或者通过shell脚本运行, 执行 sh start.sh 就可以运行。


### 联系我
如果关于代码任何有问题，可以提交issues, 或者联系我微信: bitquant51

