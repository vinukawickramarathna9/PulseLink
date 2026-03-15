import streamlit as st
import pandas as pd
from db_utils import fetch_recent_predictions


def app():
    st.markdown("## 🗂 Recent Diabetes Predictions (from DB)")
    st.markdown("---")

    col1, col2 = st.columns([1, 3])
    limit = col1.number_input("Rows", min_value=1, max_value=100, value=10)
    refresh = col2.button("Refresh")

    try:
        rows = fetch_recent_predictions(limit=limit)
        if not rows:
            st.info("No predictions found yet. Create one from the Admin page.")
            return
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Database error: {e}")
