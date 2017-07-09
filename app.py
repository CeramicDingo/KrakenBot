import brain
import data
import backtest
import time

datadir = r'C:\Users\craig\Desktop\BOT Project'
keyfile = r'C:\Users\craig\Desktop\BOT Project\kraken.key'

crypto = 'XXBT'
fiat = 'ZEUR'
timeframe = 1
ma_1 = 5
ma_2 = 15

# Trading Pairs:
# XETHZEUR
# XXBTZEUR
# 1234

d = data.Data(datadir, keyfile, crypto, fiat, timeframe)
d.import_ohlc()
d.refresh_ohlc()

# print('Data: ' + str(d.ohlc_data))
# print('Last ID: ' + str(d.ohlc_last_id))

d.update_sma(ma_1)
d.update_sma(ma_2)
# print(str(d.calcs_data))

# Loop for x minutes
# for t in range(2):
#     d.refresh_ohlc()
#     print('Data: ' + str(d.ohlc_data))
#     print('Last ID: ' + str(d.ohlc_last_id))
#     time.sleep(60)

b = brain.Brain(d)
# b.sma_decide(ma_1, ma_2)

# Backtest
t = backtest.Backtest(d, b)
t.test_sma(ma_1, ma_2)

d.export_ohlc()
d.export_ohlc_csv()
d.export_trades()
