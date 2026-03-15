import streamlit as st
from data.base import about_diabets, warn

def app():
    st.markdown("## 📋 Clinical Information & Education")
    st.markdown("---")
    st.markdown(about_diabets)
    st.markdown("---")
    st.markdown("## ⚠️ Medical Disclaimer")
    st.warning(warn)
