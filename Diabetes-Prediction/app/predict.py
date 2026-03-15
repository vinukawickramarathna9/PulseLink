import time
import streamlit as st
from loader import model, accuracy_result
from data.config import thresholds
from function.function import make_donut
from data.base import mrk


def app(input_data):
    # Check if parameters were loaded from URL and show notification
    if st.session_state.get('auto_predict_requested', False):
        st.info("🔗 **Parameters loaded from CareSync Admin Panel** - Running diabetes risk assessment with provided clinical data.")
        # Clear the flag so notification doesn't show again
        if 'auto_predict_requested' in st.session_state:
            del st.session_state['auto_predict_requested']
    
    prediction = model.predict_proba(input_data)[:, 1]

    cols = st.columns(2)

    def stream_data():
        is_diabetes = f'High Risk - Diabetes Indicated' if prediction >= thresholds else 'Low Risk - No Diabetes Indicated'
        
        # Model Performance Information
        text = f"CareSync AI Model Performance\n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)
        text = f"Clinical Accuracy: {accuracy_result}%\n\n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)
            
        # Risk Assessment Result
        text = f"Diabetes Risk Assessment Result:\n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)
        text = f"{is_diabetes}\n\n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)
            
        # Probability Score
        text = f"Risk Probability Score: {(prediction * 100).round(2)[0]}%\n\n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)
            
        # Clinical Recommendation
        if prediction >= thresholds:
            text = f"Clinical Recommendation: Consult healthcare provider for further evaluation.\n"
        else:
            text = f"Clinical Recommendation: Continue regular health monitoring and healthy lifestyle.\n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)
        
        return 80

    cols[0].write_stream(stream_data)


    is_diabetes = f'<strong>⚠️ HIGH RISK</strong><br/>Diabetes Risk Detected<br/><small>Immediate medical consultation recommended</small>' if prediction >= thresholds else f'<strong>✅ LOW RISK</strong><br/>No Diabetes Risk Detected<br/><small>Continue preventive health measures</small>'
    border_color = '#ef4444' if prediction >= thresholds else '#3b82f6'  # Red for diabetes, blue for no diabetes
    text_color = '#ef4444' if prediction >= thresholds else '#3b82f6'  # Red for diabetes, blue for no diabetes
    chart_color = 'red' if prediction >= thresholds else 'blue'

    cols[1].markdown(mrk.format(border_color, text_color, is_diabetes), unsafe_allow_html=True)
    cols[1].write('\n\n\n\n\n')
    donut_chart_population = make_donut((prediction * 100).round(2)[0], 
                                        'Diabetes Risk',
                                        input_color=chart_color)

    cols[1].altair_chart(donut_chart_population)