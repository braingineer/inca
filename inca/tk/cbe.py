import requests
from dateutil import parser
from contextlib import contextmanager
#from autobahn.twisted.websocket import WebSocketServerProtocol

class CoinbaseExchange(object):
    api_url = 'http://api.exchange.coinbase.com/'
    from_prod = "BTC"
    to_prod = "USD"

    @staticmethod
    def _call(method, params={}):
        url = {
                'currencies'        : 'currencies/',
                'time'              : 'time/',
                'products'          : 'products' ,
                'order_book'        : 'products/{}-{}/book',
                'product_ticker'    : 'products/{}-{}/ticker',
                'product_trades'    : 'products/{}-{}/trades',
                'product_stats'     : 'products/{}-{}/stats',
                  }
        url = url[method].format(CoinbaseExchange.from_prod, CoinbaseExchange.to_prod)

        return insertPythonTime( requests.get(CoinbaseExchange.api_url + url, params=params).json() )

    @staticmethod
    @contextmanager
    def context(f=None, t=None, reset=True):
        ce = CoinbaseExchange
        ce.from_prod, _f = (f or ce.from_prod), ce.from_prod
        ce.to_prod, _t = (t or ce.to_prod), ce.to_prod
        yield ce
        if reset:
            ce.from_prod = _f
            ce.to_prod = _t

    @staticmethod
    def getProducts():
        return CoinbaseExchange._call("products")
    
    @staticmethod    
    def getProductOrderBook(level=1):
        return CoinbaseExchange._call("order_book", {'level':level})
    
    @staticmethod    
    def getProductTicker():
        return CoinbaseExchange._call("product_ticker")
    
    @staticmethod            
    def getProductTrades():
        return CoinbaseExchange._call("product_trades")
    
    @staticmethod    
    def getProductHistoricRates():
        raise Exception("not implemented yet")
    
    @staticmethod    
    def getProductStats():
        return CoinbaseExchange._call("product_stats")
    
    @staticmethod    
    def getCurrencies():
        return CoinbaseExchange._call("currencies")
    
    @staticmethod    
    def getTime():
        return CoinbaseExchange._call("time")

def ConvertTime(json_time):
    return parser.parse(json_time)

def insertPythonTime(return_json):
    for row in return_json:
        if type(row) is dict:
            if row.has_key("time"):
                row['python_time'] = ConvertTime(row['time'])
    return return_json


def get_price(denom):
    if denom.lower() == "eth":
        with CoinbaseExchange.context("ETH", 'BTC') as ce:
            return ce.getProductTicker()['price']

    elif denom.lower() == "btc":
        with CoinbaseExchange.context("BTC", "USD") as ce:
            return ce.getProductTicker()['price']
