import matplotlib.pyplot as plt
import streamlit as st

from analysis.mpi import MoneyFlowIndex
from analysis.rsi import RelativeStrengthIndex
from pages.portfolio import PortfolioOptimization
from pages.technical import TechnicalAnalysis
# App configuration
from services.file_service import FileService
from services.stooq_service import StooqService
from services.yf_service import YahooFinanceService

st.set_page_config(page_title="Finance App", )
plt.style.use('seaborn')

# App sidebar
st.sidebar.header('Pages')


def __show_pages_menu():
    return st.sidebar.radio("", ('Technical analysis', 'Portfolio Optimization'))


def __show_page():
    if pages == 'Technical analysis':
        technical_analysis = TechnicalAnalysis(st)
        technical_analysis.show()
    elif pages == 'Portfolio Optimization':
        portfolio = PortfolioOptimization(st)
        portfolio.show()


def __process_mpi(df):
    mpi = MoneyFlowIndex(df)
    result_df = mpi.calculate()
    mpi.show_mpi(plt, st, result_df)
    mpi.show_close_price_plot_with_signals(plt, st, result_df)


def __process_rsi(df):
    rsi = RelativeStrengthIndex(df)
    result_rsi_df = rsi.calculate()
    rsi.show_rsi(plt, st, result_rsi_df)


def __process_input(input_type):
    if input_type in ['YAHOO API', 'Stooq API']:
        ticker_symbol = st.sidebar.text_input('Enter Ticker Symbol')
        start_date = st.sidebar.date_input('Start date:')
        end_date = st.sidebar.date_input('End date:')
        if input_type == 'YAHOO API':
            df = YahooFinanceService.download(ticker_symbol, start_date, end_date)
        elif input_type == 'Stooq API':
            df = StooqService.download(ticker_symbol, start_date, end_date)
    else:
        uploaded_file = st.sidebar.file_uploader("Choose a file with data", type=['csv'])
        df = FileService.upload(uploaded_file)

    if not df.empty:
        st.write(df)
        __process_analysis(selected_analysis_form, df)


def __process_analysis(selected_analysis, data):
    if 'MFI' in selected_analysis:
        __process_mpi(data)
    if 'RSI' in selected_analysis:
        __process_rsi(data)


pages = __show_pages_menu()
__show_page()

st.sidebar.header('User panel')

input_type_form = st.sidebar.radio("Select the data type", ('FILE', 'YAHOO API', 'Stooq API'))
selected_analysis_form = st.sidebar.multiselect('Analysis', ['MFI', 'RSI'])
__process_input(input_type_form)
