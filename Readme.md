# Upbit API Collections

This repo contains api for upbit exchange.  
cralwer_server.py :   
  saves recent ohlcv(open-high-low-close-volume) candle as pandas dataframe  

upbit_trader_api.py : 
  handles api request (create order/ check order status/ cancel order/ get order book/ get ohlcv candle ...)  

## Getting Started

```

$ python cralwer_server.py -t "KRW-BTC" -p "./data/" -m 5 -c 400 -l 15000


usage: crawler_server.py [-h] [-t TARGET] [-p PATH] [-m MINUTE] [-c COUNT]
                         [-l LENGTH]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        provide coin name e.g. KRW-BTC
  -p PATH, --path PATH  designate where to save ohlcv data
  -m MINUTE, --minute MINUTE
                        data frequency min provided e.g. 1, 5, 15, 30, 60, 240
  -c COUNT, --count COUNT
                        provide count e.g. 400
  -l LENGTH, --length LENGTH
                        provide total length e.g. 15000

```


### Prerequisites

common library such as numpy, pandas matplotlib

```python
pip install -r requirements.txt
```

```
## usage for upbit_trader_api

# set up api keys
import upbit_trader_api
upbit_trader_api.ACCESS_KEY = ""
upbit_trader_api.SECRET_KEY = ""

# create buy, sell order
uuid = upbit_trader_api.create_order(market="KRW-BTC", side='bid', price=price, volume=volume)
uuid = upbit_trader_api.create_order(market="KRW-BTC", side='ask', price=price, volume=volume)
# cancel order
upbit_trader_api.cancel_order(uuid)
# check order status
upbit_trader_api.get_order_info(uuid)

```

[upbit_trader_api](https://github.com/miroblog/upbit_api_collection/blob/master/example_upbit_trader_api.ipynb) / [cralwer_server](https://github.com/miroblog/upbit_api_collection/blob/master/crawler_server_example.ipynb)

```python
ohlcv['close'].plot()
plot.show()
```
![close](https://github.com/miroblog/upbit_api_collection/blob/master/png/close.png)


```python
show_limit = 20 # plot latest 20 candles
candlestick_ohlc(ax1, df_ohlc.values[-show_limit:], width=0.001, colorup='g')
plt.show()
```
![candle](https://github.com/miroblog/upbit_api_collection/blob/master/png/ohlc.png)

## Authors

* **Lee Hankyol** - *Initial work* - [Upbit_API_COLLECTION](https://github.com/miroblog/upbit_api_collection)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
