import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


def render_ml_model(df):
    st.subheader("Health Risk Classification Model")

    # ==============================
    # 1) Select features
    # ==============================
    features = ["age", "bmi (kg/cm²)", "sleep (h)", "exercise", "smoking", "alcohol"]
    target = "health_risk"

    ml_df = df[features + [target]].dropna()

    # ==============================
    # 2) Encode categorical features
    # ==============================
    encoder = LabelEncoder()

    for col in ["exercise", "smoking", "alcohol"]:
        ml_df[col] = encoder.fit_transform(ml_df[col].astype(str))

    X = ml_df[features]
    y = ml_df[target].astype(int)

    # ==============================
    # 3) Create classification labels
    # ==============================
    # 1 = Low, 2 = Medium, 3+ = High
    y_class = y.copy()
    y_class[y <= 1] = 0       # Low
    y_class[y == 2] = 1       # Medium
    y_class[y >= 3] = 2       # High

    class_labels = {0: "Low", 1: "Medium", 2: "High"}

    # ==============================
    # 4) Train-test split
    # ==============================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.25, random_state=42
    )

    # ==============================
    # 5) Train classification model
    # ==============================
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    

    # ==============================
    # 7) User Input For Prediction
    # ==============================
    st.write("### 🎯 Predict Your Health Risk")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 18, 80, 30)
        bmi = st.slider("BMI", 11.0, 51.0, 25.0)
        sleep = st.slider("Sleep (h)", 3.0, 10.0, 7.0)

    with col2:
        exercise = st.selectbox("Exercise", df["exercise"].unique())
        smoking = st.selectbox("Smoking", df["smoking"].unique())
        alcohol = st.selectbox("Alcohol", df["alcohol"].unique())

    # Encode categorical inputs
    ex_enc = encoder.fit_transform(df["exercise"].astype(str)).tolist().index(
        encoder.transform([exercise])[0]
    )
    sm_enc = encoder.fit_transform(df["smoking"].astype(str)).tolist().index(
        encoder.transform([smoking])[0]
    )
    al_enc = encoder.fit_transform(df["alcohol"].astype(str)).tolist().index(
        encoder.transform([alcohol])[0]
    )

    user_data = [[age, bmi, sleep, ex_enc, sm_enc, al_enc]]

    # ========== TAHMİN ET BUTONU ==========
    if st.button("🔮 Tahmin Et"):
        pred_class = model.predict(user_data)[0]
        pred_label = class_labels[pred_class]

        st.success(f"📌 **Predicted Health Risk: {pred_label}**")

    # ==============================
    #  Evaluation
    # ==============================
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    st.write("### 📊 Model Accuracy")
    st.write(f"**Accuracy:** {accuracy:.2f}")
