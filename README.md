# 51bitquant-multi_pairs_martingle_bot
A muti pairs martingle trading bot for Binance exchange. 


## Configuration

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
 "open_pos_from_drop_down": 0.05, 
 "exit_profit_pct": 0.01,
 "profit_pull_back_pct": 0.01, 
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


