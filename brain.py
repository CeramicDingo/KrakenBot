import datetime


class Brain:

    def __init__(self, data):
        self.d = data
        pass

    # Decide on a trade using SMA. Curr / Prev parameters used for back testing purposes and is the frame ID.
    # If curr / prev parameters are provide will run as a backtest
    def sma_decide(self, ma_1, ma_2, curr=None, prev=None):
        test = True
        if curr is None or prev is None:
            curr = self.d.ohlc_data[-1][0]
            prev = self.d.ohlc_data[-2][0]
            test = False

        key_ma_1 = 'SMA' + str(ma_1)
        key_ma_2 = 'SMA' + str(ma_2)

        curr_ma_1 = self.d.calcs_data[curr][key_ma_1]
        curr_ma_2 = self.d.calcs_data[curr][key_ma_2]

        prev_ma_1 = self.d.calcs_data[prev][key_ma_1]
        prev_ma_2 = self.d.calcs_data[prev][key_ma_2]

        trade = []
        dt = datetime.datetime.now()

        # print('Prev: ' + str(prev))
        # print('\t' + key_ma_1 + ': ' + str(prev_ma_1))
        # print('\t' + key_ma_2 + ': ' + str(prev_ma_2))
        # print('Curr: ' + str(curr))
        # print('\t' + key_ma_1 + ': ' + str(curr_ma_1))
        # print('\t' + key_ma_2 + ': ' + str(curr_ma_2))

        if not self.d.open_position:
            # If we don't have an open position, look for BUY opportunities
            if curr_ma_1 > curr_ma_2 and prev_ma_1 <= prev_ma_2:
                decision = 'BUY'
                self.d.open_position = True
                # Log the trade. Assume last OHLC price for now (will amend with actual BUY / SELL price.
                # trade.append(decision + '\t' + self.d.tradingpair + '\t@' + str(self.d.ohlc_data[-1][4]))
                trade.append(decision)
                trade.append(self.d.tradingpair)
                if test:
                    price = self.d.price_data[curr]
                    trade.append(price)
                    trade.append(str(dt))
                else:
                    trade.append(self.d.ohlc_data[-1][4])
                    trade.append(str(dt))
                # Need to fix this, so backtesting doesn't mess up main trade log, move test trades data to
                # backtest object.
                self.d.trade_log.append(trade)
                # print(decision)
                print(trade)
            else:
                decision = 'HOLD'
                # print(decision)
        else:
            # If we do have an open position, look for SELL opportunities
            if curr_ma_1 < curr_ma_2 and prev_ma_1 >= prev_ma_2:
                decision = 'SELL'
                self.d.open_position = False
                # Log the trade. Assume last OHLC price for now (will amend with actual BUY / SELL price.
                # trade.append(decision + '\t' + self.d.tradingpair + '\t@' + str(self.d.ohlc_data[-1][4]))
                trade.append(decision)
                trade.append(self.d.tradingpair)
                if test:
                    price = self.d.price_data[curr]
                    trade.append(price)
                    trade.append(str(dt))
                else:
                    trade.append(self.d.ohlc_data[-1][4])
                    trade.append(str(dt))
                self.d.trade_log.append(trade)
                # print(decision)
                print(trade)
            else:
                decision = 'HOLD'
                # print(decision)
        return decision

