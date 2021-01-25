from analysis.mpi import MoneyFlowIndex
import pandas as pd
import yfinance as yf


class TechnicalAnalysis:
    def __init__(self, st, plt):
        self.st = st
        self.plt = plt

    def show(self):
        self.st.write("""
        # Technical analysis
        """)
        options = self.__show_panel()

        input_type = self.st.sidebar.radio("Select the data type", ('FILE', 'YAHOO API'))
        df = pd.DataFrame()

        if input_type == 'YAHOO API':
            ticker_symbol = self.st.sidebar.text_input('Enter Ticker Symbol')
            start_date = self.st.sidebar.date_input('self.start date:')
            end_date = self.st.sidebar.date_input('End date:')
            if len(ticker_symbol) > 0:
                # Getting data from API
                ticker_data = yf.Ticker(ticker_symbol)
                df = ticker_data.history(start=str(start_date), end=str(end_date))
                self.st.write(df)

        else:
            uploaded_file = self.st.sidebar.file_uploader("Choose a file with data", type=['csv'])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                df.dropna(inplace=True)
                # Set date as the index to have the same DF as from Yahoo API
                df = df.set_index(pd.DatetimeIndex(df['Date']).values)
                self.st.write(df)

        if not df.empty and options:
            if 'MFI' in options:
                mpi = MoneyFlowIndex(df)
                result_df = mpi.calculate()
                mpi.show_mpi(self.plt, self.st, result_df)
                mpi.show_close_price_plot_with_signals(self.plt, self.st, result_df)

    def __show_panel(self):
        self.st.sidebar.header('User panel')
        return self.st.sidebar.multiselect(
            'Select technical indicator',
            ['MFI', 'RSI'], [])
