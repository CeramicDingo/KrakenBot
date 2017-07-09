from collections import deque


class Calcs:

    def __init__(self):
        pass

    # Calculate SMA from OHLC data
    def calc_sma(self, data, ma):
        result = {}
        count = 0
        ma_prices = deque()

        for item in data:
            count += 1
            if count < ma:
                ma_prices.append(item[4])
                result[item[0]] = 0.0
            elif count == ma:
                ma_prices.append(item[4])
                cum_total = 0.0

                for val in ma_prices:
                    cum_total += val

                result[item[0]] = cum_total / ma
            else:
                ma_prices.popleft()
                ma_prices.append(item[4])
                cum_total = 0.0

                for val in ma_prices:
                    cum_total += val

                result[item[0]] = cum_total / ma
        return result
