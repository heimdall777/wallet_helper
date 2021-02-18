import pandas as pd
import yfinance as yf


class YahooFinanceService:

    @staticmethod
    def download(ticker_symbol, start_date, end_date):
        if len(ticker_symbol) > 0:
            # Getting data from API
            ticker_data = yf.Ticker(ticker_symbol)
            return ticker_data.history(start=str(start_date), end=str(end_date))
        else:
            return pd.DataFrame()
