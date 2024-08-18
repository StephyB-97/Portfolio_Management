import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from pandas import DataFrame
import requests
import json

API_KEY = '60d0e31e3d254620a59ca513bec82984'


def fetch_news(api_key, ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        if articles:
            # Parse the source field correctly
            for article in articles:
                article['source'] = article['source'].get('name', 'Unknown Source')

            df_news = pd.DataFrame(articles)

            # Convert publishedAt to datetime for sorting
            df_news['publishedAt'] = pd.to_datetime(df_news['publishedAt'])

            # Sort by publishedAt (newest first) and select top 10
            df_news = df_news.sort_values(by='publishedAt', ascending=False).head(10)

            return df_news
        else:
            return pd.DataFrame()  # Return empty DataFrame if no articles
    else:
        st.error("Failed to fetch news: " + data.get('message', 'Unknown error'))
        return pd.DataFrame()


def show_Stock_Dashboard():
    # Get ticker and dates from user
    st.title("Stock Dashboard")
    ticker = st.sidebar.text_input('Ticker', 'TSLA')
    start_date = st.sidebar.date_input('Start Date', value=None)
    end_date = st.sidebar.date_input('End Date')

    # download to the application or get the historical information for a ticker
    data = yf.download(ticker, start=start_date, end=end_date)  # Downloads the data for ticker
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)  # Sets up parameters for the line graph
    ticker_metric = yf.Ticker(ticker)
    current_price = ticker_metric.info['currentPrice']
    previous_close = ticker_metric.info['previousClose']
    company_name = ticker_metric.info['shortName']
    delta = current_price- previous_close
    percentage_change = (delta / previous_close) * 100
    st.metric(label=company_name, value=f"{current_price:.2f} USD", delta=f"${delta:.2f} ({percentage_change:.2f}%)")

    st.plotly_chart(fig)  # Displays the information as a line graph

    pricing_data, financial_data, news = st.tabs(["Pricing Data", "Financial Data", "Latest News"])

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

    with financial_data:
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

    with news:
        st.header(f'Latest News for {ticker}')
        df_news = fetch_news(API_KEY, ticker)
        if not df_news.empty:
            for index, row in df_news.iterrows():
                st.write(f"**Source:** {row['source']}")
                st.write(f"**Author:** {row['author']}")
                st.write(f"**Published Date:** {row['publishedAt'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**Description:** {row['description']}")

                # Create a clickable title that redirects to the URL
                st.markdown(f"[**{row['title']}**]({row['url']})")

                st.write("---")  # Separator line
        else:
            st.write("No news data available.")







