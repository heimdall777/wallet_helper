import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

from analysis.mpi import MoneyFlowIndex
from analysis.rsi import RelativeStrengthIndex
from pages.portfolio import PortfolioOptimization
from pages.technical import TechnicalAnalysis

# App configuration
from services.stooq_service import StooqService

st.set_page_config(page_title="Finance App", )
plt.style.use('seaborn')

# App sidebar
st.sidebar.header('Pages')


def show_pages_menu():
    return st.sidebar.radio("", ('Technical analysis', 'Portfolio Optimization'))


def show_page():
    if pages == 'Technical analysis':
        technical_analysis = TechnicalAnalysis(st)
        technical_analysis.show()
    elif pages == 'Portfolio Optimization':
        portfolio = PortfolioOptimization(st)
        portfolio.show()


pages = show_pages_menu()
show_page()

st.sidebar.header('User panel')

input_type = st.sidebar.radio("Select the data type", ('FILE', 'YAHOO API', 'Stooq API'))
st.sidebar.multiselect('Analysis', ['MFI', 'RSI'])
df = pd.DataFrame()

if input_type == 'YAHOO API':
    ticker_symbol = st.sidebar.text_input('Enter Ticker Symbol')
    start_date = st.sidebar.date_input('Start date:')
    end_date = st.sidebar.date_input('End date:')
    if len(ticker_symbol) > 0:
        # Getting data from API
        tickerData = yf.Ticker(ticker_symbol)
        df = tickerData.history(start=str(start_date), end=str(end_date))
        st.write(df)

if input_type == 'Stooq API':
    ticker_symbol = st.sidebar.text_input('Enter Ticker Symbol')
    start_date = st.sidebar.date_input('Start date:')
    end_date = st.sidebar.date_input('End date:')
    df = StooqService.download(ticker_symbol, start_date, end_date)
    if not df.empty:
        st.write(df)

else:
    uploaded_file = st.sidebar.file_uploader("Choose a file with data", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.dropna(inplace=True)
        # Set date as the index to have the same DF as from Yahoo API
        df = df.set_index(pd.DatetimeIndex(df['Date']).values)
        st.write(df)

if not df.empty:
    mpi = MoneyFlowIndex(df)
    result_df = mpi.calculate()
    mpi.show_mpi(plt, st, result_df)
    mpi.show_close_price_plot_with_signals(plt, st, result_df)

    rsi = RelativeStrengthIndex(df)
    result_rsi_df = rsi.calculate()
    rsi.show_rsi(plt, st, result_rsi_df)
