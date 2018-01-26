import base64, hashlib, hmac, urllib, time, urllib, json
import urllib.request 
from collections import OrderedDict

DOMAIN_BASE = 'https://api.btcmarkets.net'

BTCMARKET_PARAM_MULTIPLYER = 100000000

# If postData is None, it will use GET method otherwise POST
def http_request(key, secret, path, postData = None):
    nowInMilisecond = str(int(time.time() * 1000))
    if postData == None:
        stringToSign = path + "\n" + nowInMilisecond + "\n"  
    else:
        stringToSign = path + "\n" + nowInMilisecond + "\n" + postData  
    stringToSign = stringToSign.encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, stringToSign, digestmod=hashlib.sha512).digest())

    header = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'User-Agent': 'btc markets python client',
        'accept-charset': 'utf-8',  
        'apikey': key,
        'signature': signature,
        'timestamp': nowInMilisecond,
    }

    if postData == None:
        request = urllib.request.Request(DOMAIN_BASE + path, None, header, method='GET')
    else:
        request = urllib.request.Request(DOMAIN_BASE + path, postData.encode(), header)
    opener = urllib.request.build_opener()
    response = opener.open(request)
    raw_data = response.read()
    raw_data = raw_data.decode()

    return json.loads(raw_data)


class BTCMarkets:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret)

    def pretty_format_json(self, j):
        return json.dumps(j, sort_keys=True, indent=4)

    def trade_history(self, currency, instrument, limit = 5, since = 1):
        limit = int(limit)
        since = int(since)
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        output = http_request(self.key, self.secret, '/order/trade/history', postData) 

        if output['success']:
            output = output['trades']
            for i in range(len(output)):
                output[i]['price'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['volume'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['fee'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['creationTime'] = time.ctime(output[i]['creationTime'])
            return self.pretty_format_json(output)
        else:
            return output['errorMessage']

    # To sell, use statement like: order_create('AUD', 'ETH', 1300, 1, 'ask')
    # To buy, use statement like: order_create('AUD', 'ETH', 1300, 1, 'bid')
    # The return dictionary will contain the order_id, you'll need taht to cancel order or query status of order
    def order_create(self, currency, instrument, price, volume, side, order_type='Limit', client_request_id='1'):
        price = float(price) * BTCMARKET_PARAM_MULTIPLYER
        volume = float(volume) * BTCMARKET_PARAM_MULTIPLYER
        price = int(price)
        volume = int(volume)

        data = OrderedDict([('currency', currency),('instrument', instrument),
            ('price', price),('volume', volume),('orderSide', side),('ordertype', order_type),
            ('clientRequestId', client_request_id)])
        postData = json.dumps(data, separators=(',', ':'))

        output = http_request(self.key, self.secret, '/order/create', postData) 
        return self.pretty_format_json(output)

    def order_cancel(self, order_ids):
        order_ids = int(order_ids)
        data_obj = {'orderIds':[order_ids]} 
        postData = json.dumps(data_obj, separators=(',', ':'))
        output = http_request(self.key, self.secret, '/order/cancel', postData)
        return self.pretty_format_json(output)

    def order_history(self, currency, instrument, limit = 5, since = 1):
        limit = int(limit)

        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        output = http_request(self.key, self.secret, '/order/history', postData) 

        if output['success']:
            output = output['orders']
            for i in range(len(output)):
                output[i]['creationTime'] = time.ctime(output[i]['creationTime'])
                output[i]['price'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['volume'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['openVolume'] /= BTCMARKET_PARAM_MULTIPLYER
        return self.pretty_format_json(output)

    # Will return all open orders 
    def order_open(self, currency, instrument, limit = 1, since = 1):
        limit = int(limit)
        since = int(since)
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        output = http_request(self.key, self.secret, '/order/open', postData) 

        if output['success']:
            output = output['orders']
            for i in range(len(output)):
                output[i]['creationTime'] = time.ctime(output[i]['creationTime'])
                output[i]['price'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['volume'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['openVolume'] /= BTCMARKET_PARAM_MULTIPLYER
        return self.pretty_format_json(output)

    def order_detail(self, order_ids):
        order_ids = int(order_ids)
        data_obj = {'orderIds':[order_ids]} 
        postData = json.dumps(data_obj, separators=(',', ':'))
        output = http_request(self.key, self.secret, '/order/detail', postData)
        if output['success']:
            output = output['orders']
            for i in range(len(output)):
                output[i]['creationTime'] = time.ctime(output[i]['creationTime'])
                output[i]['price'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['volume'] /= BTCMARKET_PARAM_MULTIPLYER
                output[i]['openVolume'] /= BTCMARKET_PARAM_MULTIPLYER
        return self.pretty_format_json(output)

    def account_balance(self):
        output = http_request(self.key, self.secret, '/account/balance')
        for i in range(len(output)):
            output[i]['balance'] /= BTCMARKET_PARAM_MULTIPLYER
            output[i]['pendingFunds'] /= BTCMARKET_PARAM_MULTIPLYER
        return self.pretty_format_json(output)

    # currency_in is AUD usually
    # currency_out is cryptocurrency type
    def get_market_tick(self,currency_in,currency_out):
        output = http_request(self.key, self.secret, '/market/%s/%s/tick' % (currency_in,currency_out))
        if 'timestamp' in output:
            output['timestamp'] = time.ctime(output['timestamp'])
        return self.pretty_format_json(output)

    def get_market_orderbook(self,currency_in,currency_out):
        output = http_request(self.key, self.secret, '/market/%s/%s/orderbook' % (currency_in,currency_out))
        return self.pretty_format_json(output)

    def get_market_trades(self,currency_in,currency_out):
        output = http_request(self.key, self.secret, '/market/%s/%s/trades' % (currency_in,currency_out))
        if 'date' in output:
            output['date'] = time.ctime(output['date'])
        return self.pretty_format_json(output)