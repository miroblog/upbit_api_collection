# -*- coding: utf-8 -*-
import datetime as dt
import json
import pandas as pd
from pandas.io.json import json_normalize
from dateutil.parser import parse
import time
import requests

def upbit_get_next_to(last_row):
    k = None
    try:
        temp = last_row['candle_date_time_utc'].values[0]
        k = parse(temp)
    except:
        print(k)
        return None
    return k.strftime("%Y-%m-%d %H:%M:%S")

def get_candle_data(market, period, to,count):
    retry = 3
    while(retry > 0):
        try:
            url = "https://api.upbit.com/v1/candles/minutes/{0}".format(period)
            querystring = {"market": market,
                           'to': to,
                           'count':count}
            response = requests.request("GET", url, params=querystring)
            json_obj = json.loads(response.text)
            temp = json_normalize(json_obj)
            return temp
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def rename_col(df):
    df = df.rename(columns={'opening_price': 'open',
                            'high_price': 'high',
                            'low_price': 'low',
                            'trade_price': 'close',
                            'candle_acc_trade_volume': 'volume',
                            'candle_date_time_utc': 'datetime'})
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df

def main():
    to = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame()
    while (len(df.index) < DATA_LENGTH):
        data = get_candle_data("{0}".format(TARGET_NAME), UPBIT_PERIOD, to, UPBIT_COUNT)
        df = df.append(data, ignore_index=True)
        df.drop_duplicates(subset=['candle_date_time_utc'], keep='first', inplace=True)
        next_to = upbit_get_next_to(df.tail(1))
        k = -1
        while (next_to is None):
            next_to = upbit_get_next_to(df.iloc[k - 1:k])
            k -= 10
        to = next_to
        print("{0} : {1}".format(TARGET_NAME, len(df.index)))
    result = df.reindex(index=df.index[::-1])
    file_suffix = str(UPBIT_PERIOD) + "_" + str(len(df.index)) + ".csv"
    result = rename_col(result)
    result.to_csv(DATA_PATH + TARGET_NAME + "_" + file_suffix, index=False)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", default="400", help="provide coin name e.g. KRW-BTC")
    parser.add_argument("-p", "--path", default="./data/", help="designate where to save ohlcv data")
    parser.add_argument("-m", "--minute", default="./data/", help="data frequency min provided e.g. 1, 5, 15, 30, 60, 240")
    parser.add_argument("-c", "--count", default="400", help="provide count e.g. 400 ")
    parser.add_argument("-l", "--length", default="10000", help="provide total length e.g. 15000 ")
    args = parser.parse_args()
    TARGET_NAME = args.target
    UPBIT_PERIOD = args.minute
    UPBIT_COUNT = args.count
    DATA_PATH = args.path
    DATA_LENGTH = args.length

    # sanity check
    # get market list
    url = "https://api.upbit.com/v1/market/all"
    response = requests.request("GET", url)
    markets = response.json()
    market_list = [info['market'] for info in markets]

    # check !
    if args.target not in market_list:
        raise ValueError('could not find {0} in {1}'.format(args.target, market_list))
    main()
