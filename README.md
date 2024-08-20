# Portfolio Management and Stock Dashboard Tool

This project consists of a portfolio management tool and a stock dashboard application. The portfolio management tool allows users to track their stock investments, while the stock dashboard provides detailed insights and analysis for individual stocks, including historical price data, financial metrics, and news.

## Usage

### Portfolio Management Tool

**Login/Signup:**
- Open the application in your browser.
- Use the login screen to access existing accounts or create a new user account.

**Add Stocks to Portfolio:**
- Enter stock ticker symbols, purchase dates, and the number of stocks purchased.
- Click "Fetch Stock Price" to get the stock price on the selected date.
- Add stocks to your portfolio and view current investments.

**Performance and Analysis:**
- Use the "Calculate Portfolio Performance" button to see detailed performance metrics.
- View portfolio performance compared to the S&P 500 through interactive charts.
- Analyze portfolio and benchmark risks.

### Stock Dashboard

**View Stock Data:**
- Enter a stock ticker symbol and select date ranges in the sidebar.
- View historical price data and current stock metrics.

**Analyze Pricing Data:**
- Check historical price movements and calculate annual return and risk-adjusted return.

**Access Financial Data:**
- View balance sheets, income statements, and cash flow statements.

**Read Latest News:**
- Fetch and display the latest news articles related to the stock.



## Features

### Portfolio Management Tool
- **User Authentication**: Secure login and registration using Firebase.
- **Portfolio Tracking**: Add stocks, track performance, and calculate gains/losses.
- **Visualizations**: Compare portfolio performance against the S&P 500.
- **Risk Analysis**: Evaluate portfolio and benchmark risks.

### Stock Dashboard
- **Stock Metrics**: Display current price, price changes, and percentage change.
- **Pricing Data**: View historical price movements and calculate annual return and risk-adjusted return.
- **Financial Data**: Access balance sheets, income statements, and cash flow statements.
- **News**: Fetch and display the latest news related to the stock.



## Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Firebase project and credentials
- News API key for fetching news data

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name](https://github.com/StephyB-97/Portfolio_Management.git

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**
   
   Ensure you have the requirements.txt file in your repository. Install the necessary Python packages using pip:

   ```bash
   pip install -r requirements.txt

4. **Setup Firebase**

Obtain your Firebase credentials JSON file.

Place the JSON file in the root directory of the project.

Add the file to .gitignore to prevent it from being committed to version control.

5. **Configure Environmental Variable**

Create a .env file in the root directory and add the following configuration:

```bash
FIREBASE_CONFIG_PATH= (the path of your json file)
API_KEY= (your API key)

6. **Run the Application**

```bash
streamlit run main.py






