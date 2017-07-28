from collections import deque


class Calcs(object):

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

    # Calculate EMA from OHLC data
    def calc_ema(self, data, ema):
        result = {}
        count = 0
        cum_total = 0.0
        w_multiplier = (2/(ema + 1))
        prev_ema = 0.0

        for item in data:
            count += 1
            if count < ema: # Not enough data points to calculate EMA
                cum_total += item[4] # Close price
                result[item[0]] = 0.0 # OHLC ID / result
            elif count == ema: # On the first EMA calc, the prev EMA is not available, so use SMA
                cum_total += item[4]
                ema_val = cum_total / ema # SMA to seed first EMA value
                result[item[0]] = ema_val
                prev_ema = ema_val
            else: # Calculate EMA as normal
                close = item[4]
                ema_val = (close-prev_ema)*w_multiplier+prev_ema
                result[item[0]] = ema_val
                prev_ema = ema_val
        return result
