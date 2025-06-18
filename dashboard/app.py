import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

# Add src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from src.inference import load_model, predict  # Assumes src/inference.py exists

# Load model
model = load_model()

st.set_page_config(page_title="BreeBoost Fraud Predictor", layout="centered")
st.title("🚨 BreeBoost – Real-Time Fraud Detection")

# ... (imports and setup remain unchanged)

# ---------------- Load and Preprocess Data ---------------- #
@st.cache_data
def load_data():
    path = ROOT_DIR / "data" / "processed" / "paysim_cleaned.csv"
    df = pd.read_csv(path)
    if "isFraud" in df.columns:
        target = "isFraud"
    elif "fraud" in df.columns:
        target = "fraud"
    else:
        st.error("No fraud target column found.")
        st.stop()
    return df, target

df, target_col = load_data()

# ---------------- Correlation Analysis ---------------- #
st.subheader("📊 Feature Correlation with Fraud")
st.markdown("""
Understanding how each numerical feature correlates with fraud helps identify what characteristics are most predictive. 
A positive correlation means the feature tends to increase with fraud, while a negative one suggests the opposite.
""")

numeric_cols = df.select_dtypes(include="number")
corr_matrix = numeric_cols.corr()
fraud_corr = corr_matrix[[target_col]].drop(target_col, axis=0).sort_values(by=target_col, ascending=False)

fig, ax = plt.subplots(figsize=(4, len(fraud_corr) * 0.4))
sns.heatmap(fraud_corr, annot=True, cmap="coolwarm", ax=ax, cbar=True)
st.pyplot(fig, clear_figure=False)

# ---------------- Top Features Boxplots ---------------- #
st.subheader("📦 Top Feature Distributions")
st.markdown("""
Below are the top 3 features most correlated with fraud, visualized by how their values differ between fraudulent and non-fraudulent transactions. 
Boxplots highlight the distribution and range of values for each class.
""")

top_features = fraud_corr.abs().sort_values(by=target_col, ascending=False).head(3).index.tolist()
cols = st.columns(len(top_features))

for col, feature in zip(cols, top_features):
    with col:
        st.markdown(f"**{feature}**")
        fig, ax = plt.subplots(figsize=(3, 2))
        sns.boxplot(data=df, x=target_col, y=feature, ax=ax, palette="Set2")
        ax.set_xlabel("")
        ax.set_ylabel("")
        st.pyplot(fig, clear_figure=False)

# ---------------- Data Snapshot ---------------- #
st.subheader("🧾 Snapshot of First 100 Rows")
st.markdown("""
A preview of the dataset used to train and evaluate the fraud detection model.
This table includes the first 100 rows of processed transaction data.
""")
st.dataframe(df.head(100), use_container_width=True)

# ---------------- Fraud Prediction Form ---------------- #
st.markdown("---")
st.markdown("### 📝 Try It Yourself")
st.markdown("""
Enter transaction details to simulate and test how the model would classify a real-world transaction. 
This allows you to understand how different values influence the prediction.
""")

with st.form("fraud_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        step = st.number_input("Step", min_value=0, value=1)
        oldbalanceOrg = st.number_input("Old Balance (Origin)", value=5000.0)
        oldbalanceDest = st.number_input("Old Balance (Dest)", value=0.0)

    with col2:
        type_ = st.selectbox("Type", options=[0, 1])  # 0: PAYMENT, 1: TRANSFER (example)
        newbalanceOrig = st.number_input("New Balance (Origin)", value=4000.0)
        newbalanceDest = st.number_input("New Balance (Dest)", value=0.0)

    with col3:
        amount = st.number_input("Amount", min_value=0.0, value=1000.0)
        hour = st.slider("Hour of Day", 0, 23, 10)
        day = st.slider("Day of Month", 1, 31, 15)

    # Derived features
    errorBalanceOrig = oldbalanceOrg - newbalanceOrig - amount
    errorBalanceDest = newbalanceDest - oldbalanceDest - amount
    is_large_transaction = int(amount > 100000)

    submitted = st.form_submit_button("🚀 Predict Fraud")

if submitted:
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
    is_fraud = prediction[0] == 1 if hasattr(prediction, '__getitem__') else prediction > 0.5
    if is_fraud:
        st.error("🚨 Prediction: Fraud")
    else:
        st.success("✅ Prediction: Not Fraud")

    if fraud_proba is not None and len(fraud_proba) > 0:
        st.metric(label="Fraud Probability", value=f"{fraud_proba[0][1]:.4f}")
    else:
        st.metric(label="Fraud Probability", value="N/A")
