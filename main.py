import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
from navbar import show_navbar
import os
from dotenv import load_dotenv


load_dotenv()

# Firebase configuration
firebase_config = {
    "type": st.secrets["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace('\\n', '\n'),  # Handle newlines in private key
    "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_CLIENT_ID"],
    "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
    "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_X509_CERT_URL"]
}
cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
# Initialize Firebase
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)    # when run locally, comment this section out

# Predefined credentials for testing
def get_test_credentials():
    # This function should return existing credentials for testing.
    # Replace 'test@example.com' and 'testpassword' with actual test credentials from Firebase.
    email = 'test@test.com'
    password = 'testpassword'
    return email, password

def login_screen():
    st.title("Login")

    # Autofill with existing credentials
    email, password = get_test_credentials()

    email_input = st.text_input("Email Address", value=email)  # Autofill email
    password_input = st.text_input("Password", type="password", value=password)  # Autofill password

    def handle_login():
        if email_input and password_input:  # Checks if fields are not empty
            try:
                # Firebase does not have a direct method for email-password login.
                # We authenticate by trying to fetch the user by email and assume the password is correct.
                user = auth.get_user_by_email(email_input)
                st.session_state['logged_in'] = True
                st.session_state['username'] = user.uid
                st.success("Logged in successfully")

            except:
                st.error("Invalid credentials or user does not exist")
            #st.rerun()
        else:
            st.error("Email and password are required")

    st.button("Login", on_click=handle_login)

    if st.button("New User"):
        st.session_state['show_register'] = True
        st.rerun()

def register_screen():
    st.title("Register")
    new_username = st.text_input("New Username")
    email = st.text_input("Email Address")
    new_password = st.text_input("New Password", type="password")

    def handle_register():
        if new_username and email and new_password:  # Checks if fields are not empty
            try:
                user = auth.create_user(email=email, password=new_password, uid=new_username)
                st.success("Registered successfully! Redirecting to login page...")
                st.session_state['show_register'] = False

            except Exception as e:
                st.error(f"Registration failed: {e}")
        else:
            st.error("All fields are required")

    st.button("Register", on_click=handle_register)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    if st.session_state['logged_in']:
        # Main application code here
        show_navbar()  # Function to show the main application navbar
    else:
        if st.session_state['show_register']:
            register_screen()
        else:
            login_screen()

if __name__ == "__main__":
    main()
