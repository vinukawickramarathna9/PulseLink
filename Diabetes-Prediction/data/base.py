st_style = """
<style>
/* Hide Streamlit UI elements */
#MainMenu, footer, header { visibility: hidden; }
div.block-container { padding-top: 1rem; }
button[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* CareSync Design System Variables */
:root {
    --primary-blue: #3b82f6;
    --primary-blue-dark: #1d4ed8;
    --secondary-blue: #2563eb;
    --secondary-blue-dark: #1e40af;
    --text-primary: #1f2937;
    --text-black: #000000;
    --bg-white: white;
    --bg-gray-light: #f8fafc;
    --border-gray: #e5e7eb;
    --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Global theme */
.stApp {
    background-color: var(--bg-white) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-family) !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, p, div, span {
    color: var(--text-primary) !important;
    font-family: var(--font-family) !important;
}

/* Sidebar styling */
.stSidebar, .stSidebar > div, .stSidebar .stMarkdown,
.css-1d391kg, .css-1lcbmhc, .css-17eq0hr {
    background-color: var(--bg-white) !important;
}

.css-1d391kg {
    border-right: 2px solid var(--primary-blue) !important;
}

.stSidebar .stMarkdown, .stSidebar .stText, .stSidebar p, 
.stSidebar div, .stSidebar span, .stSidebar label {
    color: var(--text-black) !important;
    font-family: var(--font-family) !important;
}

.stSidebar .stNumberInput > div, .stSidebar .stSelectbox > div {
    background-color: var(--bg-white) !important;
}

.stSidebar .stNumberInput label, .stSidebar .stSelectbox label {
    color: var(--text-black) !important;
    font-weight: 500 !important;
}

/* Button styling */
.stButton button, .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: var(--font-family) !important;
    transition: all 0.2s ease !important;
}

.stButton button:hover, .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--secondary-blue-dark) 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

/* Input fields */
.stNumberInput input, .stSelectbox select, .stSlider {
    background-color: var(--bg-white) !important;
    color: var(--text-black) !important;
    border: 2px solid var(--border-gray) !important;
    border-radius: 8px !important;
    font-family: var(--font-family) !important;
}

.stNumberInput input:focus, .stSelectbox select:focus {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Charts and components */
.stPlotlyChart {
    background-color: var(--bg-white) !important;
    border-radius: 12px !important;
    border: 2px solid var(--border-gray) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: var(--bg-gray-light) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--primary-blue) !important;
    border-radius: 8px !important;
    font-family: var(--font-family) !important;
}

.streamlit-expanderContent {
    background-color: var(--bg-white) !important;
    border: 2px solid var(--border-gray) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* Alert messages */
.stSuccess {
    background-color: #f0f9ff !important;
    color: var(--text-primary) !important;
    border-left: 4px solid var(--primary-blue) !important;
}

.stError {
    background-color: #fef2f2 !important;
    color: var(--text-primary) !important;
    border-left: 4px solid #ef4444 !important;
}

.stWarning {
    background-color: #fffbeb !important;
    color: var(--text-primary) !important;
    border-left: 4px solid #f59e0b !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-gray-light) !important;
    border-radius: 8px !important;
    border: 2px solid var(--border-gray) !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-primary) !important;
    font-family: var(--font-family) !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--primary-blue) !important;
    color: white !important;
}
</style>
"""

footer = """
    <style>
    .footer {
        position: relative;
        left: 0;
        width: 100%;
        background: white;
        text-align: center;
        padding: 16px;
        font-size: 14px;
        color: #1f2937;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.1);
        border-top: 2px solid #3b82f6;
        margin-top: 40px;
    }
    .footer-brand {
        display: inline-flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .footer-heart {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 6px;
        padding: 4px;
        margin-right: 8px;
        font-size: 12px;
    }
    .footer-title {
        font-weight: bold;
        color: #1f2937;
        margin: 0 8px 0 0;
    }
    .footer-subtitle {
        color: #3b82f6;
        font-size: 12px;
        font-weight: 500;
    }
    .footer-divider {
        border-top: 1px solid #e5e7eb;
        margin: 12px 0 8px 0;
        padding-top: 8px;
    }
    .footer-description {
        color: #4b5563;
        margin-bottom: 8px;
    }
    </style>
    <div class="footer">
        <div class="footer-brand">
            <div class="footer-heart">❤️</div>
            <span class="footer-title">CareSync</span>
            <span class="footer-subtitle">Healthcare Management</span>
        </div>
        <div class="footer-description">
            Professional Diabetes Risk Assessment | Clinical Decision Support System
        </div>
        <div class="footer-divider">
            © 2025 CareSync Healthcare Management System. All rights reserved.
        </div>
    </div>
    """


head = """
    <div style="display: flex; 
    justify-content: center; 
    align-items: center; 
    margin-bottom: 20px; 
    padding: 20px;
    background: white;
    border-bottom: 2px solid #3b82f6;">
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
        color: white; 
        border-radius: 12px; 
        padding: 8px; 
        margin-right: 12px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">
            ❤️
        </div>
        <div>
            <h1 style="font-size: 36px; 
            font-weight: bold; 
            color: #1f2937; 
            margin: 0; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                CareSync
            </h1>
            <p style="font-size: 14px; 
            color: #3b82f6; 
            margin: 0; 
            font-weight: 500;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                Diabetes Risk Assessment
            </p>
        </div>
    </div>
    <div style="text-align: center; 
    font-size: 18px; 
    color: #1f2937; 
    margin-bottom: 40px; 
    padding: 20px;
    background: white;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        Professional AI-powered diabetes risk assessment and clinical decision support platform
    </div>
    """

mrk = """
<div style="background: white; 
color: #1f2937; 
margin-bottom: 50px;
padding: 20px;
max-width: 300px;
text-align: center;
border-radius: 12px; 
border: 2px solid {};
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="color: {}; font-weight: bold; margin-bottom: 8px;">
        {}
    </div>
</div>
"""


about_diabets = """
## What is diabetes?

**Diabetes** is a chronic health condition that affects how your body turns food into energy. It is characterized by high levels of glucose (sugar) in the blood, which occurs because the body either doesn’t produce enough insulin, doesn’t use insulin effectively, or both.

### **Types of Diabetes**:
1. **Type 1 Diabetes**:
   - An autoimmune condition where the immune system attacks and destroys insulin-producing cells in the pancreas.
   - Typically diagnosed in children and young adults.
   - Requires daily insulin injections to manage blood sugar.

2. **Type 2 Diabetes**:
   - The body becomes resistant to insulin, or the pancreas doesn’t produce enough insulin.
   - Often linked to lifestyle factors like obesity, physical inactivity, and poor diet, but genetics also play a role.
   - Managed through lifestyle changes, medications, and sometimes insulin.

3. **Gestational Diabetes**:
   - Occurs during pregnancy when the body cannot make enough insulin to support the increased demand.
   - Usually resolves after childbirth, but it increases the risk of developing type 2 diabetes later in life.

### **Symptoms of Diabetes**:
- Frequent urination
- Excessive thirst
- Extreme hunger
- Fatigue
- Blurred vision
- Slow-healing wounds
- Unexplained weight loss (especially in type 1 diabetes)

### **Complications of Untreated Diabetes**:
- Heart disease
- Kidney damage
- Vision loss (diabetic retinopathy)
- Nerve damage (diabetic neuropathy)
- Increased risk of infections

### **Management**:
- **Diet**: Eating a balanced diet, avoiding high-sugar foods.
- **Exercise**: Regular physical activity to improve insulin sensitivity.
- **Medications**: Insulin therapy or oral diabetes medications.
- **Monitoring**: Regularly checking blood glucose levels.
"""


warn = """
**Important Medical Disclaimer:** This AI-powered assessment tool is designed for educational and informational purposes only. 
The predictions and recommendations provided should not replace professional medical advice, diagnosis, or treatment. 
Please consult with qualified healthcare professionals for comprehensive medical evaluation and personalized treatment plans. 
CareSync Healthcare Management System emphasizes the importance of professional medical supervision for all health-related decisions.
"""