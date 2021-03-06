import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

from analysis.mpi import MoneyFlowIndex

st.set_page_config(page_title="Finance App")
plt.style.use('seaborn')

st.sidebar.header('Pages')
sides = st.sidebar.radio("", ('Technical analysis', 'Portfolio Optimization'))

st.sidebar.header('User panel')

input_type = st.sidebar.radio("Select the data type", ('FILE', 'YAHOO API'))
df = pd.DataFrame()

st.write("""
# Technical analysis
""")

if input_type == 'YAHOO API':
    ticker_symbol = st.sidebar.text_input('Enter Ticker Symbol')
    start_date = st.sidebar.date_input('Start date:')
    end_date = st.sidebar.date_input('End date:')
    if len(ticker_symbol) > 0:
        # Getting data from API
        tickerData = yf.Ticker(ticker_symbol)
        df = tickerData.history(start=str(start_date), end=str(end_date))
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
