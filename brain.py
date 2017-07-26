import time
import trade


class Brain(object):

    def __init__(self, data, c_vol=0.01):
        self.d = data
        self.c_vol = c_vol # Units of crypto to trade
        self.trd = trade.Trade(self.d, 60) # Trade obj with order expiry of x seconds
        self.open_position = False
        self.sim_open_position = False # For simulations / backtests
        pass

    # Check we have enough crypto to start trading with (above c_vol)
    def check_min_c(self):
        result = False
        cryptobal = self.d.get_cryptobal()

        if cryptobal >= self.c_vol:
            result = True

        return result

    # Check we have enough fiat to start trading with (enough fiat to buy c_vol)
    def check_min_f(self):
        result = False

        price = self.d.ohlc_data[-1][4] # Last close price
        unitprice = price * self.c_vol # Calculate unit price based on c_vol qty

        fiatbal = self.d.get_fiatbal()

        if fiatbal > (unitprice * 0.01): # Assume 1% commission rate
            result = True

        return result

    # Decide whether to execute a live trade for the chosen SMAs
    def sma_decide(self, ma_1, ma_2):
        fiatcheck = self.check_min_f()
        cryptocheck = self.check_min_c()

        # If we have >= crypto than the trading vol, then we are looking to sell
        if cryptocheck:
            self.open_position = True
        else:
            self.open_position = False

        key_ma_1 = 'SMA' + str(ma_1)
        key_ma_2 = 'SMA' + str(ma_2)

        # Get ID of current frame and previous frame
        curr = self.d.ohlc_data[-1][0]
        prev = self.d.ohlc_data[-2][0]

        # Retrieve SMA calcs from dict object
        curr_ma_1 = self.d.calcs_data[curr][key_ma_1]
        curr_ma_2 = self.d.calcs_data[curr][key_ma_2]

        prev_ma_1 = self.d.calcs_data[prev][key_ma_1]
        prev_ma_2 = self.d.calcs_data[prev][key_ma_2]

        # Log decisions
        decision_log = []

        # Log executed trades
        trade_log = []

        # Get current UNIX epoch and convert to a timestamp string
        ts = time.asctime(time.gmtime())

        if (fiatcheck or cryptocheck) and (prev_ma_1 != 0.0 and prev_ma_2 != 0.0):
            # Firstly check that we have either enough crypto or fiat to begin trading,
            # also make sure that we have enough SMA data to make a decision
            if not self.open_position:
                # If we don't have an open position, look for BUY opportunities
                if curr_ma_1 > curr_ma_2 and prev_ma_1 <= prev_ma_2:
                    decision = 'buy' # Needs to be lower case to be valid to the API

                    # Log decision
                    price = self.d.price_data[curr]
                    decision_log.append(decision)
                    decision_log.append(self.d.tradingpair)
                    decision_log.append(price)
                    decision_log.append(curr)
                    decision_log.append(ts)
                    self.d.decision_log.append(decision_log)

                    print('BUY - SMA Crossover.')

                    # Execute trade and log outcome
                    print('***Executing market BUY order***')
                    trade_log.append(self.trd.market_order(decision, self.c_vol))
                    self.d.trade_log.append(trade_log)
                else:
                    decision = 'hold'

                    # Log decision
                    price = self.d.price_data[curr]
                    decision_log.append(decision)
                    decision_log.append(self.d.tradingpair)
                    decision_log.append(price)
                    decision_log.append(curr)
                    decision_log.append(ts)
                    self.d.decision_log.append(decision_log)

                    print('HOLD - No BUY/SELL signals.')

            elif self.open_position:
                # If we do have an open position, look for SELL opportunities
                if curr_ma_1 < curr_ma_2 and prev_ma_1 >= prev_ma_2:
                    decision = 'sell'

                    # Log decision
                    price = self.d.price_data[curr]
                    decision_log.append(decision)
                    decision_log.append(self.d.tradingpair)
                    decision_log.append(price)
                    decision_log.append(curr)
                    decision_log.append(ts)
                    self.d.decision_log.append(decision_log)

                    print('SELL - SMA Crossover.')

                    # Execute trade and log outcome
                    print('***Executing market SELL order***')
                    trade_log.append(self.trd.market_order(decision, self.c_vol))
                    self.d.trade_log.append(trade_log)
                else:
                    decision = 'hold'

                    # Log decision
                    price = self.d.price_data[curr]
                    decision_log.append(decision)
                    decision_log.append(self.d.tradingpair)
                    decision_log.append(price)
                    decision_log.append(curr)
                    decision_log.append(ts)
                    self.d.decision_log.append(decision_log)

                    print('HOLD - No BUY/SELL signals.')
        else:
            # Fallback position is to hold (not enough data or crypto/fiat)
            decision = 'hold'

            # Log decision
            price = self.d.price_data[curr]
            decision_log.append(decision)
            decision_log.append(self.d.tradingpair)
            decision_log.append(price)
            decision_log.append(curr)
            decision_log.append(ts)
            self.d.decision_log.append(decision_log)

            print('HOLD - Not enough data, or balance too low.')
        return

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

        if self.sim_open_position == False and (prev_ma_1 != 0.0 and prev_ma_2 != 0.0):
            # If we don't have an open position, look for BUY opportunities
            if curr_ma_1 > curr_ma_2 and prev_ma_1 <= prev_ma_2:
                decision = 'BUY'
                self.sim_open_position = True
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
        elif self.sim_open_position == True and (prev_ma_1 != 0.0 and prev_ma_2 != 0.0):
            # If we do have an open position, look for SELL opportunities
            if curr_ma_1 < curr_ma_2 and prev_ma_1 >= prev_ma_2:
                decision = 'SELL'
                self.sim_open_position = False
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
