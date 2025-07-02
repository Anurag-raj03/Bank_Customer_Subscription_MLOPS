import streamlit as st
import requests

st.set_page_config(page_title="Bank Marketing Predictor", layout="centered")
st.title("📊 Bank Marketing Prediction & Explanation")

# Initialize session state
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "last_input_data" not in st.session_state:
    st.session_state.last_input_data = None

with st.form("user_form"):
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    job = st.selectbox("Job", [
        'management', 'technician', 'entrepreneur', 'blue-collar', 'unknown',
        'retired', 'admin.', 'services', 'self-employed', 'unemployed', 'housemaid',
        'student'
    ])
    marital = st.selectbox("Marital Status", ['married', 'single', 'divorced'])
    education = st.selectbox("Education", ['tertiary', 'secondary', 'unknown', 'primary'])
    default = st.selectbox("Default Credit?", ['no', 'yes'])
    balance = st.number_input("Balance", value=1000)
    housing = st.selectbox("Housing Loan", ['yes', 'no'])
    loan = st.selectbox("Personal Loan", ['no', 'yes'])
    contact = st.selectbox("Contact Communication", ['unknown', 'cellular', 'telephone'])
    day = st.number_input("Last Contact Day", min_value=1, max_value=31, value=15)
    month = st.selectbox("Last Contact Month", [
        'may', 'jun', 'jul', 'aug', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'sep'
    ])
    duration = st.number_input("Contact Duration (sec)", value=300)
    campaign = st.number_input("Number of Contacts During Campaign", value=1)
    pdays = st.number_input("Days Since Last Contact", value=-1)
    previous = st.number_input("Number of Contacts Before Campaign", value=0)
    poutcome = st.selectbox("Previous Campaign Outcome", ['unknown', 'failure', 'other', 'success'])

    submitted = st.form_submit_button("🔍 Predict")

if submitted:
    input_data = {
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "balance": balance,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "day": day,
        "month": month,
        "duration": duration,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "poutcome": poutcome
    }

    try:
        response = requests.post("http://backend:8000/explain", json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.session_state.prediction_result = result.get("prediction")
            st.session_state.explanation = result.get("explanation")
            st.session_state.last_input_data = input_data
        else:
            st.error(f"Prediction failed: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")

# Display results
if st.session_state.prediction_result is not None:
    st.success(f"🎯 Predicted Outcome: {st.session_state.prediction_result}")

    if st.button("🧠 Show Explanation"):
        if st.session_state.explanation:
            st.markdown("### Explanation")
            st.info(st.session_state.explanation)
        else:
            try:
                last_data = st.session_state.get("last_input_data")
                if last_data:
                    exp_response = requests.post("http://backend:8000/explain", json=last_data)
                    if exp_response.status_code == 200:
                        explanation_text = exp_response.json().get("explanation")
                        st.session_state.explanation = explanation_text
                        st.markdown("### Explanation")
                        st.info(explanation_text)
                    else:
                        st.error(f"Explanation request failed: {exp_response.text}")
                else:
                    st.warning("No saved input data found for explanation.")
            except Exception as e:
                st.error(f"Explanation error: {e}")
