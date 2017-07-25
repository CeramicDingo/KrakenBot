import krakenex
import csv
import os
import json
import calcs
import time


class Data(object):

    def __init__(self, datadir, keyfile, crypto, fiat, timeframe=15):
        self.datadir = datadir
        self.k = krakenex.API()
        self.k.load_key(keyfile)
        self.tradingpair = crypto+fiat
        self.timeframe = timeframe
        self.ohlc_file = datadir + '\\' + self.tradingpair + str(timeframe) + '_OHLC.json'
        self.ohlc_file_csv = datadir + '\\' + self.tradingpair + str(timeframe) + '_OHLC.csv'
        self.ohlc_data = []
        self.ohlc_index = [] # Populated with every frame ID in order to obtain index for ohlc_data
        self.ohlc_last_file = datadir + '\\' + self.tradingpair + str(timeframe) + '_OHLC_LASTID.json'
        self.ohlc_last_id = 0
        self.calcs_data = {} # Multiple SMAs calculated for each OHLC frame
        self.price_data = {} # Closing price for each OHLC frame
        self.crypto = crypto
        self.fiat = fiat
        self.trade_log = [] # Log of any (real) executed trades
        self.trade_log_file = datadir + '\\' + self.tradingpair + str(timeframe) + '_TRADES.json'
        self.decision_log = [] # Log of decisions buy/sell/hold
        self.decision_log_file = datadir + '\\' + self.tradingpair + str(timeframe) + '_DECISIONS.csv'
        pass

    def _parse_ohlc(self, result):
        print('Parsing OHLC data.')
        # Parse the strings to floats
        for item in result:
            item[1] = float(item[1])
            item[2] = float(item[2])
            item[3] = float(item[3])
            item[4] = float(item[4])
            item[5] = float(item[5])
            item[6] = float(item[6])
        # Remove last item (since this is always the un-committed frame
        del result[-1]
        return result

    def import_ohlc(self):
        if os.path.isfile(self.ohlc_file) and os.path.isfile(self.ohlc_last_file):
            # Check for exisiting data file and import if it exists
            print('Importing existing OHLC data.')

            with open(self.ohlc_file, 'r', newline='') as f:
                self.ohlc_data = json.load(f)
            with open(self.ohlc_last_file, 'r', newline='') as f:
                self.ohlc_last_id = json.load(f)

            self._update_calcs_keys()
            self._update_price_data()
            self._update_ohlc_index()
        else:
            # Import new data is data file does not exist
            print('Existing OHLC data not found.')
            self.refresh_ohlc()
        return

    def refresh_ohlc(self):
        req_data = {'pair': self.tradingpair, 'interval': self.timeframe, 'since': self.ohlc_last_id}
        print('Refreshing OHLC data. Requesting from API: ' + str(req_data))

        query = self.k.query_public('OHLC', req_data)
        self.ohlc_last_id = query['result']['last']
        ohlc = query['result'][self.tradingpair]

        # Parse OHLC data
        ohlc_p = self._parse_ohlc(ohlc)

        for item in ohlc_p:
            self.ohlc_data.append(item)

        self._update_calcs_keys()
        self._update_price_data()
        self._update_ohlc_index()
        return

    # Populate all the keys with blank dicts to be used for calc data later (e.g. SMA)
    def _update_calcs_keys(self):
        for item in self.ohlc_data:
            if item[0] not in self.calcs_data:
                self.calcs_data[item[0]] = {}
        return

    # Use the closing price (item[4])
    def _update_price_data(self):
        for item in self.ohlc_data:
            if item[0] not in self.price_data:
                self.price_data[item[0]] = item[4]
        return

    def _update_ohlc_index(self):
        self.ohlc_index.clear() # Clear index list before re-populating

        for item in self.ohlc_data:
            self.ohlc_index.append(item[0])
        return

    def update_sma(self, ma):
        c = calcs.Calcs()
        sma = c.calc_sma(self.ohlc_data, ma)

        for k,v in sma.items():
            self.calcs_data[k].update({'SMA' + str(ma): v})
        return

    def export_ohlc(self):
        print('Exporting OHLC / Last ID data.')

        with open(self.ohlc_file, 'w', newline='') as f:
            json.dump(self.ohlc_data, f)
        with open(self.ohlc_last_file, 'w', newline='') as f:
            json.dump(self.ohlc_last_id, f)
        return

    def export_ohlc_csv(self):
        print('Exporting OHLC data to CSV.')

        with open(self.ohlc_file_csv, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(self.ohlc_data)
        return

    def export_trades(self):
        print('Exporting trade data.')

        with open(self.trade_log_file, 'a', newline='') as f:
            json.dump(self.trade_log, f)
        return

    def export_decisions(self):
        print('Exporting decision data.')

        with open(self.decision_log_file, 'a', newline='') as f:
            w = csv.writer(f)
            w.writerows(self.decision_log)
        return

    def get_fiatbal(self):
        query = self.k.query_private('Balance')
        fiatbal = float(query['result'][self.fiat])
        time.sleep(1) # API call limiter
        return fiatbal

    def get_cryptobal(self):
        query = self.k.query_private('Balance')
        cryptobal = float(query['result'][self.crypto])
        time.sleep(1) # API call limiter
        return cryptobal