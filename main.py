import streamlit as st
import matplotlib.pyplot as plt

from analysis.mpi import MoneyFlowIndex
from pages.portfolio import PortfolioOptimization
from pages.technical import TechnicalAnalysis

# App configuration
st.set_page_config(page_title="Finance App")
plt.style.use('seaborn')

# App sidebar
st.sidebar.header('Pages')


def show_pages_menu():
    return st.sidebar.radio("", ('Technical analysis', 'Portfolio Optimization'))


def show_page():
    if pages == 'Technical analysis':
        technical_analysis = TechnicalAnalysis(st, plt)
        technical_analysis.show()
    elif pages == 'Portfolio Optimization':
        portfolio = PortfolioOptimization(st)
        portfolio.show()


pages = show_pages_menu()
show_page()
