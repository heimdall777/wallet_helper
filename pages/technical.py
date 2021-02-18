from analysis.mpi import MoneyFlowIndex
from analysis.rsi import RelativeStrengthIndex
from services.file_service import FileService
from services.stooq_service import StooqService
from services.yf_service import YahooFinanceService


class TechnicalAnalysis:
    def __init__(self, st, plt):
        self.st = st
        self.plt = plt

    def show(self):
        self.st.write("""
        # Technical analysis
        """)
        self.st.sidebar.header('User panel')

        input_type_form = self.st.sidebar.radio("Select the data type", ('FILE', 'YAHOO API', 'Stooq API'))
        selected_analysis_form = self.st.sidebar.multiselect('Analysis', ['MFI', 'RSI'])
        self.__process_input(input_type_form, selected_analysis_form)

    def __process_mpi(self, df):
        mpi = MoneyFlowIndex(df)
        result_df = mpi.calculate()
        mpi.show_mpi(self.plt, self.st, result_df)
        mpi.show_close_price_plot_with_signals(self.plt, self.st, result_df)

    def __process_rsi(self, df):
        rsi = RelativeStrengthIndex(df)
        result_rsi_df = rsi.calculate()
        rsi.show_rsi(self.plt, self.st, result_rsi_df)

    def __process_input(self, input_type, selected_analysis_form):
        if input_type in ['YAHOO API', 'Stooq API']:
            ticker_symbol = self.st.sidebar.text_input('Enter Ticker Symbol')
            start_date = self.st.sidebar.date_input('Start date:')
            end_date = self.st.sidebar.date_input('End date:')
            if input_type == 'YAHOO API':
                df = YahooFinanceService.download(ticker_symbol, start_date, end_date)
            elif input_type == 'Stooq API':
                df = StooqService.download(ticker_symbol, start_date, end_date)
        else:
            uploaded_file = self.st.sidebar.file_uploader("Choose a file with data", type=['csv'])
            df = FileService.upload(uploaded_file)

        if not df.empty:
            self.st.write(df)
            self.__process_analysis(selected_analysis_form, df)

    def __process_analysis(self, selected_analysis, data):
        if 'MFI' in selected_analysis:
            self.__process_mpi(data)
        if 'RSI' in selected_analysis:
            self.__process_rsi(data)
