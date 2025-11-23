import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


def render_health_importance(filtered_df):

    df = filtered_df.copy()

    # ================================================
    # 1) FEATURE Engineering — ALWAYS FILTERED DF
    # ================================================
    df["habit_combined"] = df.apply(
        lambda r:
            "Both Smoking+Alcohol" if r["smoking"]=="yes" and r["alcohol"]=="yes" else
            "Smoking Only" if r["smoking"]=="yes" else
            "Alcohol Only" if r["alcohol"]=="yes" else
            "None",
        axis=1
    )

    features = [
        "exercise",
        "sleep (h)",
        "sugar_intake",
        "habit_combined",
        "married",
        "bmi (kg/cm²)",
        "age",
    ]

    # ================================================
    # 2) X, y
    # ================================================
    X = df[features].copy()
    y = df["health_risk"].copy()

    # Eğer y tek sınıfsa RandomForest eğitilemez → fallback
    if len(y.unique()) < 2:
        fallback = pd.DataFrame({
            "Feature": features,
            "Importance": [0]*len(features),
        })
        fig = px.bar(
            fallback,
            x="Importance",
            y="Feature",
            orientation="h",
            title="⚠ Not enough variation in Health Risk for model training",
            color="Importance",
            color_continuous_scale=["#cbd5e1", "#334155"],
        )
        return fig

    # ================================================
    # 3) LABEL ENCODING (Safe encoding per filtered_df)
    # ================================================
    for col in X.columns:
        if X[col].dtype == "object":
            le = LabelEncoder()
            try:
                X[col] = le.fit_transform(X[col])
            except:
                # Very rare fallback
                X[col] = X[col].astype("category").cat.codes

    # ================================================
    # 4) RANDOM FOREST WITH SAFE SETTINGS
    # ================================================
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        random_state=42
    )
    model.fit(X, y)

    # ================================================
    # 5) Feature Importances
    # ================================================
    importances = model.feature_importances_

    result = pd.DataFrame({
        "Feature": features,
        "Importance": importances
    }).sort_values("Importance", ascending=True)

    # Pretty feature names for display
    name_map = {
        "exercise": "Exercise Level",
        "sleep (h)": "Sleep Duration (h)",
        "sugar_intake": "Sugar Intake",
        "habit_combined": "Smoking + Alcohol Status",
        "married": "Marital Status",
        "bmi (kg/cm²)": "BMI",
        "age": "Age"
    }
    result["Feature"] = result["Feature"].replace(name_map)

    # ================================================
    # 6) Plot (Modern, clean, filtered-aware)
    # ================================================
    fig = px.bar(
        result,
        x="Importance",
        y="Feature",
        orientation="h",
        title="🌲 Health Risk — Feature Importance (Filtered Data)",
        color="Importance",
        color_continuous_scale=["#dbeafe", "#1e3a8a"],  # soft blue → deep blue
    )

    fig.update_layout(
        height=520,
        title_font=dict(size=24, family="Segoe UI Semibold", color="#1e293b"),
        xaxis_title="Importance Score",
        yaxis_title="Features",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=60, r=40, t=80, b=40),
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>"
    )

    return fig





