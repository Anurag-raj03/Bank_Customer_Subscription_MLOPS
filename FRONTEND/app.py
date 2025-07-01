import streamlit as st
import requests

st.set_page_config(page_title="Bank Marketing Predictor", layout="centered")
st.title("📊 Bank Marketing Prediction & Explanation")

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "last_record" not in st.session_state:
    st.session_state.last_record = None
if "explanation" not in st.session_state:
    st.session_state.explanation = None

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
    data = {
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
        response = requests.post("http://backend:8000/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            st.session_state.prediction_result = result.get("prediction", None)
            st.session_state.last_record = result.get("last_inserted_record", None)
        else:
            st.error(f"Prediction failed: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to the backend: {e}")

# Show prediction result
if st.session_state.prediction_result is not None:
    st.success(f"🎯 Predicted Outcome: {st.session_state.prediction_result}")

# Show debug/DB insertion status
if st.session_state.last_record is not None:
    st.markdown("### ✅ Debug Info: Last Inserted Record")
    st.code(st.session_state.last_record)

# Optional: Call /explain endpoint if needed
if st.button("🧠 Show Explanation"):
    try:
        explain_response = requests.post("http://backend:8000/explain", json=data)
        if explain_response.status_code == 200:
            explanation = explain_response.json().get("explanation", None)
            st.session_state.explanation = explanation
            st.markdown("### Explanation")
            st.info(explanation)
        else:
            st.error("Explanation failed.")
    except Exception as e:
        st.error(f"Explanation error: {e}")
