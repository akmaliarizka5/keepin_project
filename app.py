import streamlit as st

from views.dashboard_page import render_dashboard_page
from views.login_page import render_login_page
from views.register_page import render_register_page
from ui_helpers import configure_page, get_logo_html, init_session_state, render_global_css


configure_page()
init_session_state()
render_global_css()

logo_html = get_logo_html()

if st.session_state["current_page"] == "login":
    render_login_page(logo_html)
elif st.session_state["current_page"] == "register":
    render_register_page()
elif st.session_state["current_page"] == "dashboard":
    render_dashboard_page(logo_html)
