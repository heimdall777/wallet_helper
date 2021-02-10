import yfinance as yf


class YahooFianceService:

    def download(self, q):
        ticker_symbol = q.args.ticker
        start_date = q.args.start_date
        end_date = q.args.end_date
        if len(ticker_symbol) > 0:
            # Getting data from API
            ticker_data = yf.Ticker(ticker_symbol)
            return ticker_data.history(start=str(start_date), end=str(end_date))
