import pandas_datareader.data as web
import pandas as pd


class StooqService:
    def download(self, q):
        ticker_symbol = q.args.ticker
        start_date = q.args.start_date
        end_date = q.args.end_date
        if len(ticker_symbol) > 0:
            # Getting data from API
            df = web.DataReader(ticker_symbol, data_source='stooq', start=str(start_date), end=str(end_date))
            df['Date'] = pd.to_datetime(df.index).date
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
