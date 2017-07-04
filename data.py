import krakenex
import csv
import os
import json


class Data(object):

    def __init__(self, datadir='', keyfile='', tradingpair='', timeframe=15):
        self.datadir = datadir
        self.k = krakenex.API()
        self.k.load_key(keyfile)
        self.tradingpair = tradingpair
        self.timeframe = timeframe
        self.ohlc_file = datadir + '\\' + tradingpair + str(timeframe) + '_OHLC.json'
        self.ohlc_file_csv = datadir + '\\' + tradingpair + str(timeframe) + '_OHLC.csv'
        self.ohlc_data = []
        self.ohlc_last_file = datadir + '\\' + tradingpair + str(timeframe) + '_OHLC_LASTID.json'
        self.ohlc_last_id = 0
        # self.crypto_bal = 0.0
        # self.fiat_bal = 0.0
        return

    def _parse_ohlc(self, result):
        print('Parsing OHLC data.')
        for item in result:
            if item[0] > self.ohlc_last_id:
                result.remove(item)
            else:
                item[1] = float(item[1])
                item[2] = float(item[2])
                item[3] = float(item[3])
                item[4] = float(item[4])
                item[5] = float(item[5])
                item[6] = float(item[6])
        return result

    def import_ohlc(self):

        if os.path.isfile(self.ohlc_file) and os.path.isfile(self.ohlc_last_file):
            print('Importing existing OHLC data.')
            with open(self.ohlc_file, 'r', newline='') as f:
                self.ohlc_data = json.load(f)
            with open(self.ohlc_last_file, 'r', newline='') as f:
                self.ohlc_last_id = json.load(f)
        else:
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
