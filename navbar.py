import streamlit as st
from streamlit_navigation_bar import st_navbar
from stock_dashboard import show_Stock_Dashboard
from PortfolioSimulator import Show_Portfolio_Simulator

def show_navbar():
    page = st_navbar(["Portfolio", "Stock Dashboard"])
    if page == 'Stock Dashboard':
        show_Stock_Dashboard()
    elif page == 'Portfolio':
        Show_Portfolio_Simulator()