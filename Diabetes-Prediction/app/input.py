import streamlit as st
import pandas as pd


def app():
    # Check for URL parameters and set default values
    initialize_from_url_params()
    
    # Check if sidebar should be displayed
    if st.session_state.get('sidebar_state', 'expanded') == 'collapsed':
        # Show panel button when sidebar is collapsed
        col1, col2 = st.columns([2, 10])
        with col1:
            if st.button("☰ Show Panel", help="Show the sidebar", type="primary", key="sidebar_show_btn"):
                st.session_state.sidebar_state = "expanded"
                st.rerun()
        
        # Show a minimal floating input panel instead
        with st.expander("📋 Clinical Parameters", expanded=False):
            return create_input_form_compact()
    
    # Show full sidebar when expanded
    return create_sidebar_form()

def initialize_from_url_params():
    """Initialize input values from URL parameters if provided"""
    # Get URL parameters
    query_params = st.query_params
    
    # Set default values from URL parameters if available
    if 'pregnancies' in query_params:
        st.session_state.setdefault('url_pregnancies', int(query_params['pregnancies']))
    if 'glucose' in query_params:
        st.session_state.setdefault('url_glucose', float(query_params['glucose']))
    else:
        st.session_state.setdefault('url_glucose', 100.0)
    if 'bmi' in query_params:
        st.session_state.setdefault('url_bmi', float(query_params['bmi']))
    if 'age' in query_params:
        st.session_state.setdefault('url_age', int(query_params['age']))
    if 'insulin' in query_params:
        st.session_state.setdefault('url_insulin', float(query_params['insulin']))
    else:
        st.session_state.setdefault('url_insulin', 100.0)
    if 'auto_predict' in query_params and query_params['auto_predict'] == 'true':
        st.session_state.setdefault('auto_predict_requested', True)

def create_sidebar_form():
    # Toggle button inside sidebar
    if st.sidebar.button("✖ Hide Panel", help="Hide the sidebar", key="sidebar_hide_btn", use_container_width=True):
        st.session_state.sidebar_state = "collapsed"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Minimal CareSync branded header
    st.sidebar.markdown("""
        <div style="background: white; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #e5e7eb; 
        margin-bottom: 24px;
        text-align: center;">
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
                <div style="background: #3b82f6; 
                color: white; 
                border-radius: 6px; 
                padding: 4px 8px; 
                margin-right: 8px;
                font-size: 14px;">
                    ❤️
                </div>
                <h3 style="color: #000000; margin: 0; font-size: 18px; font-weight: 600;">
                    CareSync
                </h3>
            </div>
            <p style="color: #000000; font-size: 12px; margin: 0; font-weight: 500;">
                Clinical Assessment Portal
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Clean parameter input section
    st.sidebar.markdown("### Clinical Parameters")
    st.sidebar.markdown("---")

    return create_input_controls(st.sidebar)

def create_input_form_compact():
    # Compact form for collapsed sidebar - organized in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Basic Info")
        pregnancies_value = st.number_input(
            'Pregnancies', 
            min_value=0, 
            max_value=20, 
            value=st.session_state.get('url_pregnancies', 1)
        )
        age_value = st.number_input(
            'Age (years)', 
            min_value=0, 
            max_value=100, 
            value=st.session_state.get('url_age', 25)
        )
        
    with col2:
        st.markdown("#### Measurements")
        glucose_value = st.number_input(
            'Glucose (mg/dL)', 
            min_value=0.0, 
            max_value=250.0, 
            value=st.session_state.get('url_glucose', 100.0)
        )
        bmi_value = st.number_input(
            'BMI', 
            min_value=0.0, 
            max_value=100.0, 
            value=st.session_state.get('url_bmi', 37.0), 
            format="%.1f"
        )
        
    with col3:
        st.markdown("#### Clinical Data")
        insulin_value = st.number_input(
            'Insulin (μU/mL)', 
            min_value=0.0, 
            max_value=1000.0, 
            value=st.session_state.get('url_insulin', 100.0)
        )
        
        # Compact reference info
        st.info("**Reference:** Glucose: 70-100 mg/dL")

    return pd.DataFrame([[pregnancies_value, glucose_value, insulin_value, bmi_value, age_value]], 
                        columns=['Pregnancies', 'Glucose', 'Insulin','BMI','Age'])

def create_input_controls(container):
    # Pregnancies
    pregnancies_value = container.number_input(
        'Pregnancies',
        min_value=0,
        max_value=20,
        value=st.session_state.get('url_pregnancies', 1),
        help="Number of pregnancies"
    )

    # Glucose
    glucose_value = container.number_input(
        'Glucose (mg/dL)',
        min_value=0.0,
        max_value=250.0,
        value=st.session_state.get('url_glucose', 100.0),
        help="Plasma glucose concentration"
    )

    # Insulin
    insulin_value = container.number_input(
        'Insulin (μU/mL)',
        min_value=0.0,
        max_value=1000.0,
        value=st.session_state.get('url_insulin', 100.0),
        help="2-Hour serum insulin"
    )

    # BMI
    bmi_value = container.number_input(
        'BMI',
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.get('url_bmi', 37.0),
        format="%.1f",
        help="Body Mass Index"
    )

    # Age
    age_value = container.number_input(
        'Age (years)',
        min_value=0,
        max_value=100,
        value=st.session_state.get('url_age', 25),
        help="Patient age"
    )

    # Professional divider
    container.markdown("---")
    
    # Reference ranges
    container.info("**Reference Ranges**  \nGlucose: 70-100 mg/dL • BMI: 18.5-24.9")
    
    # Medical disclaimer
    container.warning("**Medical Disclaimer:** For educational purposes. Consult healthcare professionals for medical advice.")
    
    return pd.DataFrame([[pregnancies_value, glucose_value, insulin_value, bmi_value, age_value]], 
                        columns=['Pregnancies', 'Glucose', 'Insulin','BMI','Age'])    