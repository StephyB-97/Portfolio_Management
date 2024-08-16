import streamlit as st
from streamlit_navigation_bar import st_navbar
from stock_dashboard import show_Stock_Dashboard

def show_navbar():
    # Navbar without the css_class parameter
    page = st_navbar(["Documentation", "Stock Dashboard", "Examples"])
    if page == 'Stock Dashboard':
        show_Stock_Dashboard()
    elif page == 'Documentation':
        st.write("Documentation")
    elif page == 'Examples':
        st.write("Examples")





