import time


class Trade(object):

    def __init__(self, data, expiry):
        self.d = data
        self.expiry = expiry # Order expires after x seconds (0 = doesn't expire)
        pass

    # Place a market buy/sell order for x vol, return result array from server
    def market_order(self, otype, vol):
        req_data = {'pair': self.d.tradingpair, 'type': otype, 'ordertype': 'market', 'volume': vol,
                    'expiretm': '+' + str(self.expiry)}

        query = self.d.k.query_private('AddOrder', req_data)

        for error in query['error']:
            print(str(error))

        time.sleep(1) # API call limiter
        return query

