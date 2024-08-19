# Main application file
import streamlit as st
from auth import register_user, login_user
from db import setup_database
from navbar import show_navbar


# run once to set up database
setup_database()



def login_screen():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username and password:     # Checks if fields are not empty
            user = login_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.sidebar.success("Logged in successfully")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
        else:
            st.sidebar.error("Username and password are required")

    if st.sidebar.button("New User"):
        st.session_state['show_register'] = True
        st.rerun()



def register_screen():
    st.sidebar.title("Register")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Register"):
        if new_username and new_password:    # checks if username and password are not blank
            register_user(new_username, new_password)
            st.sidebar.success("Registered successfully! Please login")
            st.session_state['show_register'] = False
            st.rerun()

        else:
            st.sidebar.error("Username and password are required")


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    if st.session_state['logged_in']:
        # Main application code here
        show_navbar()


    else:
        if st.session_state['show_register']:
            register_screen()
        else:
            login_screen()


main()