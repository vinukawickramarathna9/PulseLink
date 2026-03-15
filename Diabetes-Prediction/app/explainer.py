import streamlit as st
import shap
import time
from loader import model
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Streamlit
import matplotlib.pyplot as plt


def app(input_data):
    sample_transformed = model.named_steps['feature_engineering'].transform(input_data)
    explainer = shap.TreeExplainer(model.named_steps['model'])
    shap_values_single = explainer.shap_values(sample_transformed)

    shap_values_class_1 = shap_values_single[0, :, 1]  # First sample, all features, class 1  


    def stream_data():
        text = f"""
Your inputs:\n
`Pregnancies`: {float(input_data.iloc[0]['Pregnancies'])}\n
`Glucose`: {float(input_data.iloc[0]['Glucose'])}\n
`Insulin`: {float(input_data.iloc[0]['Insulin'])}\n
`BMI`: {float(input_data.iloc[0]['BMI'])}\n
`Age`: {float(input_data.iloc[0]['Age'])}
                """
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)

    # Layout with two columns
    cols = st.columns(2)

    # Column 1: Stream user input
    with cols[0]:
        st.markdown("## 📈 Patient Data Analysis")
        st.markdown("---")
        st.markdown("### Real-time Parameter Processing")
        st.markdown("#### Your clinical parameters are being processed and analyzed below:")
        for word in stream_data():
            st.write(word)

    # SHAP Waterfall Plot
    fig, ax = plt.subplots()
    shap.plots.waterfall(
        shap.Explanation(
            values=shap_values_class_1,
            base_values=explainer.expected_value[1],
            data=sample_transformed.iloc[0],
            feature_names=sample_transformed.columns.tolist()
        ), show=False
    )
    fig.patch.set_facecolor("lightblue")
    fig.patch.set_alpha(0.3)
    ax.set_facecolor("#023047")
    ax.patch.set_alpha(0.5)

    # Column 2: SHAP Waterfall Plot
    with cols[1]:
        st.markdown("### 🔬 SHAP Clinical Feature Analysis")
        st.markdown(
            """
            **Clinical Interpretation Guide:**
            - 🟡 **Baseline Risk**: Expected population risk without considering individual parameters
            - 🟡 **Parameter Impact**: Each bar shows how your specific values affect diabetes risk
            - 🟡 **Final Assessment**: Combined baseline and individual factors determine your risk score
            
            **Professional Use:** This analysis assists healthcare providers in understanding which clinical parameters 
            are most significant for your individual diabetes risk profile.
            """
        )
        st.pyplot(fig)

    # SHAP Force Plot
    force_plot_html = shap.force_plot(
        base_value=explainer.expected_value[1],
        shap_values=shap_values_class_1,
        features=sample_transformed.iloc[0],
        feature_names=sample_transformed.columns.tolist()
    )

    # Explanation column
    st.markdown(
        """
        ### Column Explanations
        - 🟡 **Input Streaming**: Displays user inputs dynamically in real-time.
        - 🟡 **SHAP Waterfall Plot**: Visualizes how each feature contributes to the model prediction.
        - 🟡 **SHAP Force Plot**: Interactive plot showing positive/negative feature contributions.
        \n\n\n\n""",
        unsafe_allow_html=True,
    )

    # Add SHAP JS visualization
    force_plot_html = f"<head>{shap.getjs()}</head><body>{force_plot_html.html()}</body>"
    st.markdown("### SHAP Waterfall Plot")
    st.components.v1.html(force_plot_html, height=400)