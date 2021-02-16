import pandas_datareader.data as web
import pandas as pd


class StooqService:

    @staticmethod
    def download(ticker_symbol, start_date, end_date):
        if len(ticker_symbol) > 0:
            # Getting data from API
            return web.DataReader(ticker_symbol, data_source='stooq', start=str(start_date), end=str(end_date))
        else:
            return pd.DataFrame()
