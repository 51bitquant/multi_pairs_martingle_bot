# 51bitquant-multi_pairs_martingle_bot
A muti pairs martingle trading bot for Binance exchange. 


## Configuration

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

## how-to use
1. just config your config.json file, past your api key and secret from
   Binance, and modify your settings in config.json file.
2. run the main.py file, or you can use shell script by sh start.sh



## contact me
Wechat: bitquant51



