class Backtest:

    def __init__(self, data, brain):
        self.d = data
        self.b = brain
        pass

    def test_sma(self, ma_1, ma_2):
        print('Backtesting SMA using values: ' + str(ma_1) + '/' + str(ma_2))

        # SMA data for ma_2 not populated till the [n]-1 th record
        # (e.g. SMA20 = 20th record populated, so start data from 20th record).
        population = self.d.ohlc_data[ma_2 -1:]
        last_id = self.d.ohlc_last_id

        firstrun = True
        prev = 0

        for frame in population:
            if firstrun:
                # Don't do anything for the first frame, since we don't SMA data for previous frame.
                firstrun = False
                prev = frame[0]
            elif frame[0] == last_id:
                # Stop if there are no further records.
                break
            else:
                self.b.sma_decide(ma_1, ma_2, frame[0], prev)
                prev = frame[0]
        return
