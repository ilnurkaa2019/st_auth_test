import streamlit as st
import sqlite3
import hashlib
from streamlit_cookies_controller import CookieController
import time
# Initialize the cookies controller
cookie_controller = CookieController()
print()
print('start', list(st.session_state.keys()),list(cookie_controller.getAll().keys()))
# Database connection function
def get_db_connection():
    conn = sqlite3.connect('logs.db')
    return conn



# Function to authenticate user
def authenticate_user(username, password):
    def coder(username, password):
        a = f"{username}875ef5165a253cdd53d469fdc33a4bcc{password}"
        return hashlib.md5(a.encode()).hexdigest()
    conn = get_db_connection()
    c = conn.cursor()
    password_hash = coder(username, password)
    c.execute('SELECT id FROM user WHERE login = ? '
              'AND hash = ?', (username, password_hash))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Function to handle login
def login(username, password):
    print('login', list(st.session_state.keys()))
    user_id = authenticate_user(username, password)
    if user_id:
        # Set a cookie with the user ID
        cookie_controller.set("user_id", user_id)
        st.session_state["user_id"] = user_id
        st.success("Logged in successfully!")
        time.sleep(0.5)  # Pause briefly before rerun
        st.rerun()  # Rerun to reflect the login state immediately
    else:
        st.error("Login failed")

def settings_page():
    st.title('settings')
def stations_page():
    st.title('settings')
# Function to handle logout
def logout_page():
    # Clear cookie by setting it to an empty value with a past expiration
    cookie_controller.set("user_id", "", max_age=0)
    st.session_state.pop("user_id", None)
    st.success("Logged out successfully!")
    time.sleep(0.5)  # Pause briefly before rerun
    st.rerun()  # Rerun to clear the interface

# Check if user is logged in
def check_session():

    # Check if the user_id cookie exists
    user_id = cookie_controller.get("user_id")
    print('user_id:', user_id)
    if user_id:
        # Restore session
        st.session_state["user_id"] = user_id
        st.success("Session restored!")

# Streamlit app layout
def main():
    st.title("Simple Streamlit Login App")
    check_session()
    print('main', list(st.session_state.keys()))

    if "user_id" in st.session_state:
        st.html("nav_bar.html")
        cookie_page = cookie_controller.get('page')
        settings_ = st.Page(settings_page, url_path='/settings', default=(cookie_page == 'settings'))
        stations_ = st.Page(stations_page, url_path='/stations', default=(cookie_page == 'stations'))
        logout_ = st.Page(logout_page, url_path='/logout', default=(cookie_page == 'logout'))
        if st.button('logout'):
            st.switch_page(logout_)
        pg = st.navigation([settings_, stations_, logout_], position='hidden')
        pg.run()
    else:
        print('main else', list(st.session_state.keys()))
        st.write("Please log in.")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login(username, password)

if __name__ == "__main__":
    main()