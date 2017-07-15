import csv


class Backtest:

    def __init__(self, data, brain):
        self.d = data
        self.b = brain
        self.backtest_data = []
        self.backtest_data_file = self.d.datadir + '\\' + self.d.tradingpair + str(self.d.timeframe) + '_BACKTEST.csv'
        pass

    # Simulate a single moving average combination. Data object needs to be updated with the
    # required SMA calcs before calling.
    def sma_sim(self, ma_1, ma_2):
        firstrun = True
        profit = 0.0
        last_id = self.d.ohlc_last_id

        # Calculate buy and hold profit / loss using first and last OHLC data frames.
        buy_hold = self.d.ohlc_data[-1][4] - self.d.ohlc_data[0][4]

        print('Backtesting SMA using values: ' + str(ma_1) + '/' + str(ma_2))

        for frame in self.d.ohlc_data:
            if firstrun:
                # Don't do anything for the first frame, since we don't have a prev value.
                firstrun = False
            elif frame[0] == last_id:
                # Stop if there are no further records.
                break
            else:
                decision = self.b.sma_decide_sim(ma_1, ma_2, frame[0])
                price = decision[2]

                if decision[0] == 'BUY':
                    profit -= price
                elif decision[0] == 'SELL':
                    profit += price

        # Calculate profit in excess of buy & hold.
        vs_buy_hold = profit - buy_hold

        result = [str(ma_1) + '/' + str(ma_2), profit, buy_hold, vs_buy_hold]
        self.backtest_data.append(result)

        print('Profit: ' + str(profit))
        print('Buy & hold: ' + str(buy_hold))
        print('vs Buy & hold: ' + str(vs_buy_hold))
        return vs_buy_hold

    def export(self):
        print('Exporting backtest data to CSV.')

        # Export sim data (overwrite existing data)
        with open(self.backtest_data_file, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(self.backtest_data)
        return

    # Simulate SMA strategy for a given data object from ma_min to ma_max
    def run_sma_sim(self, ma_min, ma_max):
        best_profit = 0.0
        best_ma = ''

        # Calculate SMA values upto ma_max
        for x in range (ma_max):
            self.d.update_sma(x+1)

        for ma_1 in range(ma_min, ma_max):
            for ma_2 in range(ma_min, ma_max):
                if ma_1 < ma_2:
                    profit = self.sma_sim(ma_1, ma_2)
                    if profit > best_profit:
                        best_profit = profit
                        best_ma = str(ma_1) + '/' + str(ma_2)
        print('Best combo is: ' + best_ma + ' with ' + str(best_profit) + ' profit vs buy and hold.')
        self.export()
        return