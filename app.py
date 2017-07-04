import data
import time

datadir = r'C:\Users\craig\Desktop\BOT Project'
keyfile = r'C:\Users\craig\Desktop\BOT Project\kraken.key'

# Trading Pairs:
# XETHZEUR
# XXBTZEUR

d = data.Data(datadir, keyfile,'XXBTZEUR', 1)
d.import_ohlc()
print('Data: ' + str(d.ohlc_data))
print('Last ID: ' + str(d.ohlc_last_id))

# Loop for x minutes
for t in range(2):
    d.refresh_ohlc()
    print('Data: ' + str(d.ohlc_data))
    print('Last ID: ' + str(d.ohlc_last_id))
    time.sleep(60)

d.export_ohlc()
d.export_ohlc_csv()