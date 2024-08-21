import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
from navbar import show_navbar

# Convert Streamlit secrets to a dictionary forthe credentials reading
firebase_credentials = {
    "type": st.secrets["FIREBASE"]["type"],
    "project_id": st.secrets["FIREBASE"]["project_id"],
    "private_key_id": st.secrets["FIREBASE"]["private_key_id"],
    "private_key": st.secrets["FIREBASE"]["private_key"],
    "client_email": st.secrets["FIREBASE"]["client_email"],
    "client_id": st.secrets["FIREBASE"]["client_id"],
    "auth_uri": st.secrets["FIREBASE"]["auth_uri"],
    "token_uri": st.secrets["FIREBASE"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["FIREBASE"]["client_x509_cert_url"],
    "universe_domain": st.secrets["FIREBASE"]["universe_domain"]
}

# Function to initialize the Firebase app
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred)

# Call the initialization function
initialize_firebase()

# Predefined credentials for testing
def get_test_credentials():
    # This function should return existing credentials for testing.
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
            # st.rerun()
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
