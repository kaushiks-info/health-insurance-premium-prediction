import streamlit as st
from prediction_helper import predict

# --- PAGE SETUP ---
st.set_page_config(layout="wide", page_title="Health Insurance Premium Estimator")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* 1. LAYOUT WIDTH */
    .main .block-container {
        max_width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }

    /* 2. DARK BACKGROUND */
    .stApp {
        background-color: #050505;
    }

    /* 3. INPUT FIELDS */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div, 
    .stNumberInput > div > div > input {
        background-color: #0F1116 !important;
        color: #E0E0E0 !important;
        border: 1px solid #22262F !important;
        border-radius: 8px;
        height: 45px;
    }
    
    /* 4. SLIDERS */
    div[data-baseweb="slider"] > div > div > div > div {
        background-color: #00E5FF !important;
    }
    div[data-baseweb="slider"] > div > div > div {
        background-color: #1F2937 !important;
    }
    
    /* 5. LABELS */
    label, p {
        color: #9CA3AF !important;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* 6. BUTTON - OVERRIDE */
    div.stButton {
        width: 100% !important;
        padding: 0px !important;
        margin-top: 10px !important;
    }
    
    div.stButton > button {
        width: 100% !important;
        background: #00E5FF !important;
        border: none !important;
        padding: 15px !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        color: #FFFFFF !important;  /* WHITE TEXT */
        display: block !important;
        box-shadow: 0 4px 10px rgba(0, 229, 255, 0.3) !important;
    }

    div.stButton > button:hover {
        background: #00C7DD !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.6) !important;
        color: #FFFFFF !important;
    }
    
    /* 8. HEADERS */
    h2 { color: white; font-weight: 700; font-size: 28px; margin-bottom: 10px; }
    h4 { color: #00E5FF; font-weight: 600; font-size: 18px; padding-bottom: 10px; }
    
    /* 9. ALIGNMENT */
    div[data-testid="stVerticalBlock"] { gap: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- SUBTITLE & SIGNATURE ---
st.markdown("""
<h2>Health Insurance Premium Estimator</h2>
<div style='color:#9CA3AF; margin-top:-10px; margin-bottom:20px;'>
Instant, personalized premium estimates — powered by ML<br>
<span style='color:#6B7280;'>Built by Kaushik S.</span>
</div>
""", unsafe_allow_html=True)


# --- OPTIONS ---
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# --- COLUMNS ---
col_inputs, col_result = st.columns([3, 1], gap="large")

# === LEFT: INPUTS ===
with col_inputs:
    with st.container(border=True):
        st.markdown("<h4>Estimator Inputs</h4>", unsafe_allow_html=True)
        
        # Row 1
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<p>Age</p>", unsafe_allow_html=True)
            age = st.slider('Age', 18, 100, 24, label_visibility="collapsed")
        with c2:
            st.markdown("<p>Gender</p>", unsafe_allow_html=True)
            gender = st.selectbox('Gender', categorical_options['Gender'], label_visibility="collapsed")
        with c3:
            st.markdown("<p>Marital Status</p>", unsafe_allow_html=True)
            marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'], label_visibility="collapsed")
        with c4:
            st.markdown("<p>Dependants</p>", unsafe_allow_html=True)
            number_of_dependants = st.number_input('Dependants', 0, 20, 1, label_visibility="collapsed")

        # Row 2
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            st.markdown("<p>Genetical Risk</p>", unsafe_allow_html=True)
            genetical_risk = st.slider('Genetical Risk', 0, 5, 0, label_visibility="collapsed")
        with c6:
            st.markdown("<p>BMI Category</p>", unsafe_allow_html=True)
            bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'], label_visibility="collapsed")
        with c7:
            st.markdown("<p>Smoking Status</p>", unsafe_allow_html=True)
            is_smoker = st.toggle("Regular", value=False)
            smoking_status = "Regular" if is_smoker else "No Smoking"
        with c8:
            st.markdown("<p>Medical History</p>", unsafe_allow_html=True)
            medical_history = st.selectbox('Medical History', categorical_options['Medical History'], label_visibility="collapsed")

        # Row 3
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        c9, c10, c11, c12 = st.columns(4)
        with c9:
            st.markdown("<p>Region</p>", unsafe_allow_html=True)
            region = st.selectbox('Region', categorical_options['Region'], label_visibility="collapsed")
        with c10:
            st.markdown("<p>Income (Lakhs)</p>", unsafe_allow_html=True)
            income_lakhs = st.number_input('Income', 0, 200, 10, label_visibility="collapsed")
        with c11:
            st.markdown("<p>Insurance Plan</p>", unsafe_allow_html=True)
            insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'], label_visibility="collapsed")
        with c12:
            st.markdown("<p>Employment Status</p>", unsafe_allow_html=True)
            employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'], label_visibility="collapsed")


# === RIGHT: RESULT CARD ===
with col_result:
    pred_val = st.session_state.get('prediction', None)
    display_val = f"₹ {pred_val:,} / yr" if pred_val else "₹ 0 / yr"

    # HTML CARD
    html_code = f"""
<div style="background: linear-gradient(135deg, #0e7490 0%, #06b6d4 100%); border-radius: 12px; padding: 25px; min-height: 320px; width: 100%; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
<div>
<div style="color: white; font-size: 38px; font-weight: 700; text-align: center;">{display_val}</div>
<div style="color: #CFFAFE; font-size: 14px; text-align: center; margin-top: 5px;">Estimated Annual Premium</div>
</div>
<div style="width: 100%; height: 100px; opacity: 0.5;">
<svg viewBox="0 0 1440 320" preserveAspectRatio="none" style="width: 100%; height: 100%;">
<path fill="#CFFAFE" d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L0,320Z"></path>
</svg>
</div>
</div>
"""
    st.markdown(html_code, unsafe_allow_html=True)

    # BUTTON (Dynamic Label)
    button_label = "PREMIUM ESTIMATED" if pred_val else "ESTIMATE MY PREMIUM"

    if st.button(button_label):
        input_dict = {
            'Age': age, 'Number of Dependants': number_of_dependants, 'Income in Lakhs': income_lakhs,
            'Genetical Risk': genetical_risk, 'Insurance Plan': insurance_plan, 'Employment Status': employment_status,
            'Gender': gender, 'Marital Status': marital_status, 'BMI Category': bmi_category,
            'Smoking Status': smoking_status, 'Region': region, 'Medical History': medical_history
        }

        prediction = predict(input_dict)
        st.session_state['prediction'] = prediction
        st.rerun()
