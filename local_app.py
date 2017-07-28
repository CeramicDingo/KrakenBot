import brain
import data
import backtest
import time
import logging

# Windows
# datadir = r'C:\Users\craig\Desktop\BOT Project'
# keyfile = r'C:\Users\craig\Desktop\BOT Project\kraken.key'

# Linux
datadir = r'/home/craig/KrakenBot/Data/'
keyfile = r'/home/craig/KrakenBot/Key/kraken.key'

# Set up logging
# logging.basicConfig(filename=datadir + '\\' + 'krakenbot.log',level=logging.DEBUG)

# Trading Pairs:
# XETH  ZEUR
# XXBT  ZEUR
# XLTC  ZEUR

# Set trading pair, OHLC timeframe and moving avg vals
crypto = 'XXBT'
fiat = 'ZEUR'
timeframe = 240
ma_1 = 7
ma_2 = 16
type = 'EMA' # EMA / SMA

# Set up data object and import / refresh data
d = data.Data(datadir, keyfile, crypto, fiat, timeframe)
d.import_ohlc()
d.refresh_ohlc()

# Update SMA calcs for imported data
d.update_sma(ma_1)
d.update_sma(ma_2)

# Update EMA calcs for imported data
d.update_ema(ma_1)
d.update_ema(ma_2)

# Loop for x minutes
# for mins in range(720):
#     d.refresh_ohlc()
#     print('Refreshing OHLC data. Last ID: ' + str(d.ohlc_last_id))
#     time.sleep(60)

# Set up brain object with data and trade vol
b = brain.Brain(d)

# Backtest - pass data and brain object parameters
bt = backtest.Backtest(d, b)

# Monte carlo simulation from min to max MA
bt.run_ma_sim(type, 1, 50)

# Simulate single MA combo and export simulated trades
# bt.ma_sim(type, ma_1, ma_2)
# bt.export_trades()

# Save data
# d.export_ohlc()
# d.export_ohlc_csv()

# Testing
# d.get_cryptobal()
# d.get_fiatbal()
# print(str(b.check_min_f()))

# Random stuff
# Get tradable asset pairs
# AP = d.k.query_public('AssetPairs')
# print(AP)
