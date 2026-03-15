
import streamlit as st
import pandas as pd
from sklearn.inspection import permutation_importance
from loader import X, y, model
import plotly.express as px

def app():
    st.markdown("## 🧬 Clinical Parameter Importance Analysis")
    st.markdown("---")
    st.markdown("### Feature Significance in Diabetes Risk Assessment")
    
    cols = st.columns(2)
    perm_importance = permutation_importance(model, X, model.predict(X), n_repeats=5, random_state=42)

    perm_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': perm_importance.importances_mean
    }).sort_values(by='Importance', ascending=False)

    perm_importance_df = perm_importance_df.sort_values(by='Importance', ascending=False)
    fig = px.bar(perm_importance_df, y='Feature', x='Importance', orientation='h',
                labels={'Importance': 'Clinical Parameter Importance Score', 'Feature': 'Health Parameters'},
                title='CareSync AI Model - Clinical Parameter Significance for Diabetes Risk Assessment')
    fig.update_layout(yaxis=dict(autorange='reversed'))
    cols[0].plotly_chart(fig)
    
    # Add clinical explanation
    cols[1].markdown("### 📋 Clinical Interpretation")
    cols[1].markdown("""
    **Parameter Importance Analysis:**
    
    This chart displays the relative importance of each clinical parameter in determining diabetes risk. 
    Higher scores indicate parameters that have greater influence on the AI model's risk assessment.
    
    **Clinical Significance:**
    - **Glucose**: Blood sugar levels - primary indicator
    - **BMI**: Body mass index - obesity risk factor  
    - **Age**: Age-related risk increase
    - **Insulin**: Insulin resistance indicator
    - **Pregnancies**: Gestational diabetes history
    
    **Healthcare Provider Use:** This analysis helps prioritize which patient parameters require 
    closest monitoring and intervention for diabetes prevention and management.
    """)