from BTCMarkets import BTCMarkets
import config

client = BTCMarkets(config.BTCMARKET_PUBLIC_API_KEY, config.BTCMARKET_PRIVATE_API_KEY)

print(client.get_market_tick('ETH', 'AUD'))
print(client.get_market_orderbook('ETH', 'AUD'))
print(client.get_market_trades('ETH', 'AUD'))