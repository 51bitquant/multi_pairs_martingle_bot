
# 币安强势币多交易对马丁策略机器人

币安多交易对强势币马丁格尔策略。支持币安现货或者合约，目前只支持做多的马丁策略。

# 如何使用

1. 安装python解析器，这里推荐安装anaconda， 通过anaconda
   可以方便创建python解析器
   
2. 创建python解析器，这里以创建python
   3.9版本解析器为例子，解析器的名称为mytrader, 终端命令行中输入以下命令:
    
   > conda create -n mytrader python==3.9

3. 激活你的python trader解析器：

   > conda activate mytrader

4. 把下载下来，进行解压, 并在终端中切换到该代码所在的目录，
   你可能需要cd到这个代码所在的目录
   
5. 安装项目依赖的库，执行如下命令：

   >  pip install -r requirements.txt
   
   需要说明的是requirements.txt文件是在代码中，你可以打开看看里面依赖的库，当然你也可以手动安装各个依赖库，分别执行如下命令：
   
   > pip install requests==2.29.0 
   
   > pip install apscheduler==3.10.1 
   
   > pip install pandas
    
   > pip install numpy

    当然你可以安装不指定python版本的库，但是如果有一些库接口更改的话，可能会有问题。

6. 修改配置文config.json,
   如果没有找到该文件可以复制config-example.json文件，然后它名字改为config.json。具体的配置参数可以看下面文档的说明。

7. 运行代码： 如果是在本地电脑可以直接在终端输入：python main.py,
   或者在pycharm中直接运行，但是记得为代码配置为刚才创建的python解析器。具体的配置可以参考[网易云课堂的视频](https://study.163.com/course/courseMain.htm?courseId=1209509824&share=2&shareId=480000001919830)
   
8. 服务器运行
   
   在服务器端运行，如果是在linux服务器，可以用守护进程的方式运行：
    
   > nohup python -u main.py > nohup_log.out 2>&1 &
   
   当然你可以通过shell命令来执行代码中的start.sh 文件。
   
   如果需要购买服务器，这里推荐ucloud, 新用户优惠比较大，链接如下:
   [https://passport.ucloud.cn/?invitation_code=C1x2EA81CD79B8C](https://passport.ucloud.cn/?invitation_code=C1x2EA81CD79B8C)

###配置文件参数说明

```
 {
  "platform": "binance_spot",
  "api_key": "",
  "api_secret": "",
  "max_pairs": 4,
  "pump_pct": 0.026,
  "pump_pct_4h": 0.045,
  "initial_trade_value": 200,
  "stop_loss_pct": 0,
  "trade_value_multiplier": 1.5,
  "increase_pos_when_drop_down": 0.05,
  "exit_profit_pct": 0.01,
  "profit_drawdown_pct": 0.01,
  "trading_fee": 0.0004,
  "max_increase_pos_count": 5,
  "turnover_threshold": 100000,
  "blocked_lists": [],
  "allowed_lists": [],
  "proxy_host": "",
  "proxy_port": 0,
  "taker_price_pct": 0.005
}

```
配置文件的参数说明。

1. platform: 可选的值有两个,分别是binance_future和binance_spot，
   如果你想交易现货，就填写binance_spot, 合约就写binance_future

2. api_key: 币安交易所的api key

3. api_secret: 币安交易所的api secret

4. max_pairs: 交易对的最大数量，如果你想同时持仓10个交易对，那么这里就写10.

5. pump_pct: 1小时线暴涨百分之多少后入场,
   当然你可以修改源码，修改你的入场逻辑。这个策略的思路是挑选小时暴涨的币，然后用马丁格尔的策略去交易。

6. pump_pct_4h: 4小时线暴涨百分之多少后入场

7. initial_trade_value: 每个交易对的初始交易金额

8. stop_loss_pct: 设置止损百分比， 0.2 表示亏损20%后出场。

9. trade_value_multiplier:
   马丁格尔加仓系数，如果是2表示下一次交易的金额是上一次交易金额的两倍。

10. increase_pos_when_drop_down: 回调多少后加仓。

11. exit_profit_pct: 盈利百分之多少后出场点

12. profit_drawdown_pct: 最高值回调多少后，且有利润的时候才出场.

13. trading_fee: 交易的资金费率。
 
14. max_increase_pos_count: 最大的加仓次数.
    
15. turnover_threshold:
   这个是过滤值，就是要求一小时的最低成交量不能低于多少，默认是值 100,000 USDT.
16. blocked_lists:
   这个是禁止交易的交易对，如果你想过滤某写不想交易的山寨币，你可以把他们放在这个列表上如:
   ['XMLUSDT', 'XRPUSDT'],
    
17. allowed_lists: 如果你只想交易某一些交易对，那么放这里:
   ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']

18. proxy_host: 代理主机ip地址： 如'132.148.123.22'

19. proxy_port: 代理主机的端口号如: 8888, 9999 ect.

20. taker_price_pct: 当前盘口吃价比例，类似市价单效果


### 如何使用
1. 把代码下载下来，然后编辑config.json文件，它会读取你这个配置文件，记得填写你的交易所的api
   key 和 secret, 然后保存该配置文件，配置文件选项的说明如上面描述。
2. 直接运行main.py文件或者通过shell脚本运行, 执行 sh start.sh 就可以运行。


### 联系我
如果关于代码任何有问题，可以提交issues, 或者联系我微信: bitquant51


# multi_pairs_martingle_bot English Documentation
 Binance exchange muti pairs martingle trading bot for Binance exchange.

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
  "stop_loss_pct": 0,
  "trade_value_multiplier": 1.5,
  "increase_pos_when_drop_down": 0.05,
  "exit_profit_pct": 0.01,
  "profit_drawdown_pct": 0.01,
  "trading_fee": 0.0004,
  "max_increase_pos_count": 5,
  "turnover_threshold": 100000,
  "blocked_lists": [
    "BTCUSDT",
    "ADAUSDT"
  ],
  "allowed_lists": [],
  "proxy_host": "",
  "proxy_port": 0,
  "taker_price_pct": 0.005
}


```

1. platform: binance_future for Binance Future Exchange, binance_spot
   for Binance Spot Exchange

2. api_key: api key from Binance exchange api key

3. api_secret: api secret from Binance exchange.

4. max_pairs: the max number of pair you want to trade.

5. pump_pct: when the price pump some percent in one hour, will enter
   position.

6. pump_pct_4h: when the price pump some percent in four hour, will
   enter position.

7. initial_trade_value: the first order you want to trade.

8. stop_loss_pct: set the stop loss, 0.2 means 20%

9. trade_value_multiplier: the martingle ratio, if the value is 2, then
   the next trading value will multiply the last trading value.

10. increase_pos_when_drop_down: after entering a position, you want to
    increase your position when the price go down some percentage.

11. exit_profit_pct: exit your position when you get some profit
    percent.

12. profit_drawdown_pct: drawdown some percent of your profit, then you
will exit your position(also need to meet the requirement of the exit_profit_pct).

13. trading_fee: trading fee rate.
 
14. max_increase_pos_count: how many times you want to increase your
   positions

15. turnover_threshold: the pair's trading value should be over this
   value, the default value is 100,000 USDT.
16. blocked_lists: if you don't want to trade the symbols/pairs, put it
   here likes ['XMLUSDT', 'XRPUSDT'],
    
17. allowed_lists: if you only want to trade some specific pairs, put it
   here, like : ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']

18. proxy_host: proxy host ip location like '132.148.123.22'

19. proxy_port: proxy port like : 8888, 9999 ect.

20. taker_price_pct: the taker price

### how-to use
1. just config your config.json file, past your api key and secret from
   Binance, and modify your settings in config.json file.
2. run the main.py file, or you can use shell script by sh start.sh



### contact me
Wechat: bitquant51

