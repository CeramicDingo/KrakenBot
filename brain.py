import time


class Brain:

    def __init__(self, data):
        self.d = data
        pass

    # Simulate an SMA decision. The frame curr -1 should be available, this is not checked within the method.
    def sma_decide_sim(self, ma_1, ma_2, curr):

        key_ma_1 = 'SMA' + str(ma_1)
        key_ma_2 = 'SMA' + str(ma_2)

        # Get index of current frame and previous frame
        curr_i = self.d.ohlc_index.index(curr)
        prev_i = curr_i - 1

        # Get frame ID of previous frame
        prev = self.d.ohlc_data[prev_i][0]

        # Retrieve SMA calcs from data object
        curr_ma_1 = self.d.calcs_data[curr][key_ma_1]
        curr_ma_2 = self.d.calcs_data[curr][key_ma_2]

        prev_ma_1 = self.d.calcs_data[prev][key_ma_1]
        prev_ma_2 = self.d.calcs_data[prev][key_ma_2]

        # Log decision for the current frame
        trade = []

        # Convert frame ID (unix time) to a timestamp string
        ts = time.asctime(time.gmtime(curr))

        if self.d.sim_open_position == False and (prev_ma_1 != 0.0 and prev_ma_2 != 0.0):
            # If we don't have an open position, look for BUY opportunities
            if curr_ma_1 > curr_ma_2 and prev_ma_1 <= prev_ma_2:
                decision = 'BUY'
                self.d.sim_open_position = True
                price = self.d.price_data[curr]
                trade.append(decision)
                trade.append(self.d.tradingpair)
                trade.append(price)
                trade.append(ts)
            else:
                decision = 'HOLD'
                price = self.d.price_data[curr]
                trade.append(decision)
                trade.append(self.d.tradingpair)
                trade.append(price)
                trade.append(ts)
        elif self.d.sim_open_position == True and (prev_ma_1 != 0.0 and prev_ma_2 != 0.0):
            # If we do have an open position, look for SELL opportunities
            if curr_ma_1 < curr_ma_2 and prev_ma_1 >= prev_ma_2:
                decision = 'SELL'
                self.d.sim_open_position = False
                price = self.d.price_data[curr]
                trade.append(decision)
                trade.append(self.d.tradingpair)
                trade.append(price)
                trade.append(ts)
            else:
                decision = 'HOLD'
                price = self.d.price_data[curr]
                trade.append(decision)
                trade.append(self.d.tradingpair)
                trade.append(price)
                trade.append(ts)
        else:
            # If ma_1 or ma_2 is zero, then we don't have enough data to make decision
            decision = 'HOLD'
            price = self.d.price_data[curr]
            trade.append(decision)
            trade.append(self.d.tradingpair)
            trade.append(price)
            trade.append(ts)

        return trade

    # def sma_decide(self, ma_1, ma_2):
    #     return trade
