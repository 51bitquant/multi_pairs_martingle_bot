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
  "exit_profit_pct": 0.01,
  "profit_pull_back_pct": 0.01,
  "trading_fee": 0.0004,
  "max_increase_pos_count": 5,
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
    

## how-to use
1. just config your config file, past your api key and secret from Binance.
2. run the main.py file, or you can use shell script by sh start.sh

Now only support Future. Still in beta testing. Use at your own risk.



