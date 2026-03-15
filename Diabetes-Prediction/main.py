import streamlit as st

# Clear any potential problematic session state
if 'sidebar_toggle' in st.session_state:
    del st.session_state['sidebar_toggle']

# Initialize sidebar state
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="CareSync - Diabetes Risk Assessment",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# Header
from app.header import app
app()

# Inputs
from app.input import app
input_data =  app()

# Prediction
from app.predict import app
app(input_data)

#### Explain
from app.explainer import app
app(input_data)

# Model performance
from app.performance import app
app()

# DB predictions
from app.db_predictions import app
app()

# perm_importance
from app.perm_importance import app
app()

# About
from app.about import app
app()

# Footer
from app.footer import app
app()
