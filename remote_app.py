import data
import brain
import time
from json import JSONDecodeError
from socket import timeout

# Location of data directory and keyfile
datadir = r'/home/craig/KrakenBot/Data/'
keyfile = r'/home/craig/KrakenBot/Key/kraken.key'

# Trading Pairs:
# XETH  ZEUR
# XXBT  ZEUR
# XLTC  ZEUR

# Set trading pair, OHLC timeframe and SMA vals
crypto = 'XXBT'
fiat = 'ZEUR'
timeframe = 60
ma_1 = 7
ma_2 = 16
type = 'EMA' # EMA / SMA

# Set up data object and import / refresh data
d = data.Data(datadir, keyfile, crypto, fiat, timeframe)
d.import_ohlc() # Import OHLC data from file (if it exists)

# Set up brain object with data obj
b = brain.Brain(d, 0.3, 240) # Qty of crypto to trade and order timeout (should be less than the run interval below)

# Main program control loop
try:
    while True:
        # Refresh and save data
        try:
            d.refresh_ohlc()
        except JSONDecodeError:
            print('ERROR: Unexpected response from server, skipping...')
        except timeout:
            print('ERROR: Query to server timed out...')
        else:
            d.export_ohlc() # Save OHLC data

            # d.update_sma(ma_1) # Update sma 1 calcs
            # d.update_sma(ma_2) # Update sma 2 calcs
            d.update_ema(ma_1) # Update ema 1 calcs
            d.update_ema(ma_2) # Update ema 2 calcs

            # Make a decision if data updated OK. Brain makes calls to API, so put inside its own try block
            try:
                b.ma_decide(type, ma_1, ma_2)
            except JSONDecodeError:
                print('ERROR: Unexpected response from server...')
            except timeout:
                print('ERROR: Query to server timed out...')
            except KeyError:
                print('ERROR: Key error, null result from server...')

        time.sleep(300) # Time in seconds to wait before next cycle

finally:  # Append to export file when the program terminates, otherwise will have duplicates
    d.export_decisions()
    d.export_trades()

