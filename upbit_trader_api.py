import requests
import jwt
from requests_jwt import JWTAuth
from urllib.parse import urlencode
import time
import math
import json
from pandas.io.json import json_normalize

current_milli_time = lambda: int(round(time.time() * 1000))

SECRET_KEY = ""
ACCESS_KEY = ""
RETRY = 3

def get_headers(queryString=None):
    if(queryString == None) :
        payload = {
            'access_key': ACCESS_KEY,
            'nonce': current_milli_time()
        }
    else:
        payload = {
            'access_key': ACCESS_KEY,
            'nonce': current_milli_time(),
            'query': queryString
        }

    encoded_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    headers = {
        "Authorization": "Bearer " + encoded_token.decode("utf-8")
    }
    return headers

def get_candle_data(market, period, to,count):
    retry = RETRY
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

def get_orderbook_info(market):
    retry = RETRY
    while(retry > 0):
        try:
            url = "https://api.upbit.com/v1/orderbook"
            querystring = {"markets": market}
            response = requests.request("GET", url, params=querystring)
            return response.json()[0]
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def get_account_info():
    retry = RETRY
    while(retry > 0):
        try:
            # jwt_token = {'token':encoded_token}
            url = "https://api.upbit.com/v1/accounts"
            headers = get_headers()
            response = requests.get(url, headers=headers)
            return response.json()[0]
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def get_chance_info(market="KRW-BTC"):
    retry = RETRY
    while(retry > 0):
        try:
            raw_query = {'market':market}
            queryString = urlencode(raw_query)
            url = "https://api.upbit.com/v1/orders/chance?" + queryString
            headers = get_headers(queryString)
            response = requests.get(url, headers=headers)
            return response.json()
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1


# wait, done, cancel
def get_order_list(type='wait', page=1):
    retry = RETRY
    while(retry > 0):
        try:
            raw_query = {'state':type,
                         'page':page}
            queryString = urlencode(raw_query)
            url = "https://api.upbit.com/v1/orders?" + queryString
            headers = get_headers(queryString)
            response = requests.get(url, headers=headers)
            return response.json()
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def get_order_info(uuid):
    retry = RETRY
    while(retry > 0):
        try:
            raw_query = {'uuid':uuid}
            queryString = urlencode(raw_query)
            url = "https://api.upbit.com/v1/order?" + queryString
            headers = get_headers(queryString)
            response = requests.get(url, headers=headers)
            return response.json()
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def create_order(market, side, price, volume):
    retry = RETRY
    while(retry > 0):
        try:
            raw_query = {'market':market,
                         'side':side,
                         'volume':volume,
                         'price':price,
                         'ord_type':'limit'}
            queryString = urlencode(raw_query)
            url = "https://api.upbit.com/v1/orders?" + queryString
            headers = get_headers(queryString)
            response = requests.post(url, headers=headers)
            return response.json()
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def get_market_code():
    retry = RETRY
    while(retry > 0):
        try:
            url = "https://api.upbit.com/v1/market/all"
            response = requests.request("GET", url)
            return response.json()
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def cancel_order(uuid):
    retry = RETRY
    while(retry > 0):
        try:
            raw_query = {'uuid':uuid}
            queryString = urlencode(raw_query)
            url = "https://api.upbit.com/v1/order?" + queryString
            headers = get_headers(queryString)
            response = requests.delete(url, headers=headers)
            return response.json()['uuid']
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def get_current_tick(market):
    retry = RETRY
    while (retry > 0):
        try:
            url = "https://api.upbit.com/v1/trades/ticks"
            raw_query = {"market": market}
            response = requests.get(url, params=raw_query)
            return response.json()[0]
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def get_current_ticker(market):
    retry = RETRY
    while (retry > 0):
        try:
            url = "https://api.upbit.com/v1/ticker"
            raw_query = {"markets": market}
            response = requests.get(url, params=raw_query)
            return response.json()[0]
        except:
            print("error has occured")
            time.sleep(0.5)
            retry -= 1

def calculate_volume(price, balance, price_unit, percentage=1, fee=0.0005):
    if(price_unit > 1):
        balance = balance//price_unit * price_unit
        min_trade_cur_decimal = 1e-8
        before_fee_unit = balance / price * percentage
        expected_fee = before_fee_unit * fee
        volume = math.floor(
            (before_fee_unit - expected_fee) * (
                1 / min_trade_cur_decimal)) * min_trade_cur_decimal
    else:
        before_fee_unit = balance / price * percentage
        volume = before_fee_unit * (1-fee)
    return volume