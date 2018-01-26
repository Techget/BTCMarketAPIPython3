# BTCMarketAPIPython3

Refer to official btcmarket api-python repo [api-client-python
](https://github.com/BTCMarkets/api-client-python), the official code only works with python2. I've updated it to work with python3, refactor some of the functions to make that easier to use, also make the output more readable. 
Feel free to use it. And welcome any chats relate to automation trade and blockchain technology.

To have a taste of it, first fill the `config.py` with your own btcmarket API Key, then run
```
from BTCMarkets import BTCMarkets
import config

client = BTCMarkets(config.BTCMARKET_PUBLIC_API_KEY, config.BTCMARKET_PRIVATE_API_KEY)

print(client.get_market_tick('ETH', 'AUD'))
# print(client.get_market_orderbook('ETH', 'AUD'))
# print(client.get_market_trades('ETH', 'AUD'))
```
Will get something like
```
{
    "bestAsk": 1353.88,
    "bestBid": 1353.8,
    "currency": "AUD",
    "instrument": "ETH",
    "lastPrice": 1353.8,
    "timestamp": "Fri Jan 26 18:00:05 2018",
    "volume24h": 3004.7537
}
```
There are comments/usage explaination for buy-sell order creation and cancellation, please have a look on the source code to get the idea of using it.
