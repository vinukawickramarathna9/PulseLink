import streamlit as st
from data.base import footer


def app():
    st.markdown(footer, 
                unsafe_allow_html=True)
