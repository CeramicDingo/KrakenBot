import brain
import data
import backtest
import time

# Windows
# datadir = r'C:\Users\craig\Desktop\BOT Project'
# keyfile = r'C:\Users\craig\Desktop\BOT Project\kraken.key'

# Linux
datadir = r'/home/craig/KrakenBot/Data/'
keyfile = r'/home/craig/KrakenBot/Key/kraken.key'

# Trading Pairs:
# XETHZEUR
# XXBTZEUR
crypto = 'XXBT'
fiat = 'ZEUR'

timeframe = 60
ma_1 = 16
ma_2 = 28

# Set up data object and import / refresh data
d = data.Data(datadir, keyfile, crypto, fiat, timeframe)
d.import_ohlc()
d.refresh_ohlc()

# print('Data: ' + str(d.ohlc_data))
# print('Last ID: ' + str(d.ohlc_last_id))

# Perform SMA calcs
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

# Backtest - pass data and brain object parameters
t = backtest.Backtest(d, b)

# Simulate SMA combinations min / max SMA
t.run_sma_sim(1, 100)

# Simulate single SMA combo and export simulated trades
# t.sma_sim(ma_1, ma_2)
# t.export_trades()

# Save data
d.export_ohlc()
d.export_ohlc_csv()
d.export_trades()
