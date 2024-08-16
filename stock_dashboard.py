import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from pandas import DataFrame

def show_Stock_Dashboard():
    # Get ticker and dates from user
    st.title("Stock Dashboard")
    ticker = st.sidebar.text_input('Ticker', 'TSLA')
    start_date = st.sidebar.date_input('Start Date', value=None)
    end_date = st.sidebar.date_input('End Date')

    # download to the application or get the historical information for a ticker
    data = yf.download(ticker, start=start_date, end=end_date)  # Downloads the data for ticker
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)  # Sets up parameters for the line graph
    st.plotly_chart(fig)  # Displays the information as a line graph

    pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

    with pricing_data:
        st.header("Price Movements")
        data2 = data  # create new variable to modify data info
        data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(
            1) - 1  # calculates adjusted close price divided by previous adjusted close
        data2.dropna(inplace=True)  # omits showing the NA
        st.write(data2)  # Prints it out
        annual_return = data[
                            '% Change'].mean() * 252 * 100  # Calculates annual return based on the average daily percentage change
        st.write("Anual Return is ", annual_return, "%")
        stdev = np.std(data2["% Change"]) * np.sqrt(252)  # Calculates how much a price varies over time
        st.write("Standard Deviation is ", stdev * 100, "%")
        st.write("Risk Adj. Return is ", annual_return / (stdev * 100))

    with fundamental_data:
        # balance sheet info
        st.subheader("Balance Sheet")
        stock = yf.Ticker(ticker)
        bs = stock.balance_sheet
        st.write(bs)
        # income statement
        st.subheader("Income Statement")
        income_s = stock.income_stmt
        st.write(income_s)
        # cash flow statement
        st.subheader("Cash Flow Statement")
        cfs = stock.cashflow
        st.write(cfs)

    import requests
    with news:
        st.write("News")





