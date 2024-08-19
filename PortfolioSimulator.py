import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Show_Portfolio_Simulator():
    st.title("Investment Portfolio Dashboard")

    # Initialize session state to store portfolio information
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []

    # Initialize session state for input fields
    if 'ticker' not in st.session_state:
        st.session_state.ticker = ''
    if 'purchase_date' not in st.session_state:
        st.session_state.purchase_date = pd.to_datetime('today')
    if 'stock_price' not in st.session_state:
        st.session_state.stock_price = 0.0
    if 'num_stocks' not in st.session_state:
        st.session_state.num_stocks = 1  # Default value set to 1 to avoid the error

    # Input fields for ticker and purchase date
    ticker = st.text_input("Enter Ticker Symbol:", value=st.session_state.ticker)
    purchase_date = st.date_input("Purchase Date", value=st.session_state.purchase_date)

    # Button to fetch the stock price for the selected date
    if st.button("Fetch Stock Price"):
        if ticker:
            try:
                stock_data = yf.download(ticker, start=purchase_date, end=purchase_date + pd.Timedelta(days=1))
                if not stock_data.empty:
                    st.session_state.stock_price = stock_data['Adj Close'][0]
                    st.success(f"Price on {purchase_date}: ${st.session_state.stock_price:.2f}")
                else:
                    st.warning(f"No data available for {ticker} on {purchase_date}.")
            except Exception as e:
                st.warning(f"Unable to fetch data for {ticker}: {e}")

    # Display the fetched stock price and input field for number of stocks
    if st.session_state.stock_price > 0:
        st.write(f"Price on {purchase_date}: ${st.session_state.stock_price:.2f}")
        num_stocks = st.number_input("Number of Stocks Purchased", min_value=1, value=st.session_state.num_stocks)

    # Button to add ticker to portfolio
    if st.button("Add to Portfolio"):
        if ticker and st.session_state.stock_price > 0:
            amount_invested = st.session_state.stock_price * num_stocks
            st.session_state.portfolio.append({
                'ticker': ticker,
                'date': purchase_date,
                'price': st.session_state.stock_price,
                'num_stocks': num_stocks,
                'amount': amount_invested
            })
            st.session_state.ticker = ''
            st.session_state.purchase_date = pd.to_datetime('today')
            st.session_state.stock_price = 0.0
            st.session_state.num_stocks = 1  # Reset to 1 after adding to the portfolio
            st.success(
                f"Added {ticker} with purchase date {purchase_date}, number of stocks {num_stocks}, and total amount ${amount_invested:.2f}")

    # Display current portfolio
    if st.session_state.portfolio:
        st.subheader("Current Portfolio")
        portfolio_df = pd.DataFrame(st.session_state.portfolio)
        st.write(portfolio_df)

    # Button to perform calculations
    if st.button("Calculate Portfolio Performance"):
        if st.session_state.portfolio:
            all_data = []
            weights = []
            tickers = [stock['ticker'] for stock in st.session_state.portfolio]
            amounts = [stock['amount'] for stock in st.session_state.portfolio]
            purchase_dates = [stock['date'] for stock in st.session_state.portfolio]

            for stock, amount, date in zip(st.session_state.portfolio, amounts, purchase_dates):
                try:
                    stock_data = yf.download(stock['ticker'], start=stock['date'], end=pd.to_datetime('today'))[
                        'Adj Close']
                    if stock_data.empty:
                        st.warning(f"No data available for {stock['ticker']} from {stock['date']}.")
                    else:
                        all_data.append(stock_data.rename(stock['ticker']))
                        weights.append(stock['amount'])
                except Exception as e:
                    st.warning(f"Unable to fetch data for {stock['ticker']} from {stock['date']}: {e}")

            if all_data:
                # Combine all data into one DataFrame
                data = pd.concat(all_data, axis=1)

                # Calculate cumulative returns
                ret_df = data.pct_change()
                cumul_ret = (ret_df + 1).cumprod() - 1

                # Calculate current value and gains/losses
                current_values = data.iloc[-1] * np.array([stock['num_stocks'] for stock in st.session_state.portfolio])
                invested_values = pd.Series(amounts, index=cumul_ret.columns)
                total_invested = invested_values.sum()
                gains_losses = (current_values - invested_values) / invested_values

                # Create DataFrame for display
                performance_df = pd.DataFrame({
                    'Amount Invested ($)': weights,
                    'Current Value ($)': current_values,
                    'Gains/Losses ($)': current_values - invested_values,
                    'Gains/Losses (%)': gains_losses * 100
                })

                st.subheader("Portfolio Performance")
                st.write(performance_df)

                # Create two columns for display
                col1, col2 = st.columns(2)

                # Left column: Overall portfolio performance
                with col1:
                    st.subheader("Overall Portfolio Performance")
                    total_investment = performance_df['Amount Invested ($)'].sum()
                    total_current_value = performance_df['Current Value ($)'].sum()
                    total_gains_losses = total_current_value - total_investment
                    total_gains_losses_pct = (total_gains_losses / total_investment) * 100

                    st.write(f"Total Amount Invested: ${total_investment:.2f}")
                    st.write(f"Total Current Value: ${total_current_value:.2f}")
                    st.write(f"Total Gains/Losses: ${total_gains_losses:.2f} ({total_gains_losses_pct:.2f}%)")

                # Benchmark comparison
                try:
                    start = min([stock['date'] for stock in st.session_state.portfolio])
                    benchmark = yf.download('^GSPC', start=start)['Adj Close']
                    bench_ret = benchmark.pct_change().dropna()
                    bench_dev = (bench_ret + 1).cumprod() - 1
                except Exception as e:
                    st.warning(f"Unable to fetch S&P 500 data: {e}")
                    bench_dev = pd.Series()

                # Tabs to show charts in percentage or USD
                percentage_tab, usd_tabs, portfolio_composition = st.tabs(
                    ["Percentage Chart", "USD Chart", "Portfolio Composition"])
                with percentage_tab:
                    # Original Chart (Percentage-based)
                    st.subheader("Portfolio Performance vs. S&P 500 (Percentage)")
                    tog = pd.concat([bench_dev, cumul_ret.sum(axis=1)], axis=1)
                    tog.columns = ['S&P500 Performance (%)', 'Portfolio Performance (%)']
                    st.line_chart(tog)

                # Convert cumulative returns to USD
                portfolio_value_in_usd = total_investment * (cumul_ret.sum(axis=1) + 1)
                sp500_value_in_usd = total_investment * (bench_dev + 1)

                # Create a DataFrame with the USD values for both the portfolio and S&P 500
                usd_value_df = pd.DataFrame({
                    'Portfolio Value ($)': portfolio_value_in_usd,
                    'S&P500 Value ($)': sp500_value_in_usd
                })

                with usd_tabs:
                    # New Chart (USD-based)
                    st.subheader("Portfolio Performance vs. S&P 500 in USD")
                    st.line_chart(usd_value_df)

                # Right column: Portfolio and benchmark risks
                with col2:
                    st.subheader("Portfolio Risk:")
                    pf_std = np.sqrt((weights @ ret_df.cov() @ weights))
                    st.write(pf_std)

                    st.subheader("Benchmark Risk:")
                    bench_risk = bench_ret.std()
                    st.write(bench_risk)

                with portfolio_composition:
                    st.subheader("Portfolio Composition:")

                    # Aggregate portfolio data by ticker
                    portfolio_df = pd.DataFrame(st.session_state.portfolio)
                    aggregated_df = portfolio_df.groupby('ticker').agg({
                        'amount': 'sum'
                    }).reset_index()

                    # Extract labels and sizes
                    labels = aggregated_df['ticker']
                    sizes = aggregated_df['amount']

                    # Create columns within the tab
                    col1, col2 = st.columns([1, 2])  # Adjust column width ratios as needed

                    # Left column: Pie chart
                    with col1:
                        fig, ax = plt.subplots(facecolor='#121212')
                        ax.pie(weights, labels=tickers, autopct='%1.1f%%', textprops={'color': 'white'})
                        st.pyplot(fig)

