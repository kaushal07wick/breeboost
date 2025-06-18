import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the absolute path to the src directory
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from src.inference import load_model, predict  # from src/inference.py

# Load model
model = load_model()

st.set_page_config(page_title="BreeBoost Fraud Predictor", layout="centered")

st.title("🚨 BreeBoost – Real-Time Fraud Detection")

st.markdown("Enter transaction details to simulate and test fraud detection in real-time.")

# Input form
with st.form("fraud_form"):
    step = st.number_input("Step", min_value=0, value=1)
    type_ = st.selectbox("Type", options=[0, 1])  # 0: PAYMENT, 1: TRANSFER (as example)
    amount = st.number_input("Amount", min_value=0.0, value=1000.0)
    oldbalanceOrg = st.number_input("Old Balance (Origin)", value=5000.0)
    newbalanceOrig = st.number_input("New Balance (Origin)", value=4000.0)
    oldbalanceDest = st.number_input("Old Balance (Dest)", value=0.0)
    newbalanceDest = st.number_input("New Balance (Dest)", value=0.0)
    errorBalanceOrig = st.number_input("Error Balance (Orig)", value=oldbalanceOrg - newbalanceOrig - amount)
    errorBalanceDest = st.number_input("Error Balance (Dest)", value=newbalanceDest - oldbalanceDest - amount)
    is_large_transaction = int(amount > 100000)
    hour = st.slider("Hour of Day", 0, 23, 10)
    day = st.slider("Day of Month", 1, 31, 15)

    submitted = st.form_submit_button("🚀 Predict Fraud")

if submitted:
    # Create input DataFrame
    input_df = pd.DataFrame([{
        "step": step,
        "type": type_,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "errorBalanceOrig": errorBalanceOrig,
        "errorBalanceDest": errorBalanceDest,
        "is_large_transaction": is_large_transaction,
        "hour": hour,
        "day": day
    }])

    prediction, fraud_proba = predict(model, input_df)

    st.markdown("### 🧠 Prediction Result")

    # Interpret prediction
    is_fraud = prediction[0] == 1
    fraud_score = fraud_proba[0][1] if fraud_proba is not None and len(fraud_proba) > 0 else None

    # Prediction message
    if is_fraud:
        st.error("🚨 Prediction: Fraud")
    else:
        st.success("✅ Prediction: Not Fraud")

    # Conditional fraud probability styling
    if fraud_score is not None:
        if is_fraud and fraud_score > 0.5:
            st.markdown(f"""
                <div style='color:red; font-weight:bold; font-size:18px;'>
                    🔥 Fraud Probability: {fraud_score:.4f}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.metric(label="Fraud Probability", value=f"{fraud_score:.4f}")
    else:
        st.metric(label="Fraud Probability", value="N/A")

