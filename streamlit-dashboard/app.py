# LIFESTYLE & HEALTH ANALYTICS DASHBOARD 
import streamlit as st
import pandas as pd



# MODULE IMPORTS

from charts.stacked_bar import render_stacked_bar
from charts.treemap import render_treemap
from charts.heatmap import render_heatmap
from charts.multi_sankey import render_age_bmi_risk_sankey
from charts.geo_map import render_geo_map
from charts.histogram import render_histogram
from charts.network_diagram import render_network_diagram
from charts.swarm import render_swarm
from charts.violin_plot import render_violin
from ml_model import render_ml_model



# 1️⃣ PAGE CONFIGURATION
st.set_page_config(
    page_title="Lifestyle & Health Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏥 Lifestyle & Health Analytics Dashboard")


# 2️⃣ DATA LOADING & CLEANING
@st.cache_data
def load_data():
    df = pd.read_csv("Lifestyle_and_Health_Risk_Prediction_Synthetic_Dataset.csv")

    df.rename(columns={
        "weight": "weight (kg)",
        "height": "height (cm)",
        "bmi": "bmi (kg/cm²)",
        "sleep": "sleep (h)"
    }, inplace=True)

    return df


df = load_data()


# 3️⃣ FEATURE ENGINEERING — SCALING FIXES

risk_map = {
    "low": 1,
    "medium": 2,
    "moderate": 2,
    "high": 3,
    "very_high": 4,
    "extreme": 5
}
df["health_risk"] = df["health_risk"].map(risk_map)
df["age"] = df["age"].clip(lower=18, upper=80)

bins = [18, 25, 35, 45, 55, 65, 80]
labels = ["18–25", "26–35", "36–45", "46–55", "56–65", "66–80"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, include_lowest=True)

df["sleep (h)"] = df["sleep (h)"].clip(lower=3, upper=10)
df["bmi (kg/cm²)"] = df["bmi (kg/cm²)"].clip(lower=11, upper=51)

def categorize(row):
    if row["smoking"] == "yes" and row["alcohol"] == "yes":
        return "Both (Smoking & Alcohol)"
    elif row["smoking"] == "yes":
        return "Smoking Only"
    elif row["alcohol"] == "yes":
        return "Alcohol Only"
    else:
        return "None"

df["habit_category"] = df.apply(categorize, axis=1)
category_order = ["Alcohol Only", "Smoking Only", "Both (Smoking & Alcohol)", "None"]


# 4️⃣ SIDEBAR FILTERS — MODERN UI

with st.sidebar:

    st.markdown("""
        <div style="
            background-color:#f1f5f9;
            padding:15px;
            border-radius:10px;
            border:1px solid #e2e8f0;
            margin-bottom:20px;">
            <h3 style="margin:0; color:#334155;">🔎 Filter Panel</h3>
            <p style="font-size:13px; color:#475569; margin-top:8px;">
                Refine the dataset using demographic, lifestyle and biometric filters.
            </p>
        </div>
    """, unsafe_allow_html=True)

    if "selected_ages" not in st.session_state:
        st.session_state.selected_ages = labels
    if "selected_professions" not in st.session_state:
        st.session_state.selected_professions = sorted(df["profession"].dropna().unique().tolist())
    if "selected_married" not in st.session_state:
        st.session_state.selected_married = ["yes", "no"]
    if "selected_exercise" not in st.session_state:
        st.session_state.selected_exercise = sorted(df["exercise"].dropna().unique().tolist())
    if "selected_sugar" not in st.session_state:
        st.session_state.selected_sugar = sorted(df["sugar_intake"].dropna().unique().tolist())
    if "selected_habits" not in st.session_state:
        st.session_state.selected_habits = category_order


    st.markdown("""<h4 style="margin-top:20px; color:#1e293b;">👤 Demographics</h4>""",
                unsafe_allow_html=True)

    selected_ages = st.multiselect(
        "Age Groups",
        labels,
        default=st.session_state.selected_ages
    )

    selected_professions = st.multiselect(
        "Profession",
        sorted(df["profession"].dropna().unique().tolist()),
        default=st.session_state.selected_professions
    )

    selected_married = st.multiselect(
        "Marital Status",
        ["yes", "no"],
        default=st.session_state.selected_married
    )

    st.markdown("""<h4 style="margin-top:25px; color:#1e293b;">⚖️ Body & Health Metrics</h4>""",
                unsafe_allow_html=True)

    min_bmi, max_bmi = st.slider(
        "BMI Range", min_value=11.0, max_value=51.0, value=(11.0, 51.0), step=0.5
    )

    min_weight, max_weight = st.slider(
        "Weight (kg)",
        min_value=float(df["weight (kg)"].min()),
        max_value=float(df["weight (kg)"].max()),
        value=(float(df["weight (kg)"].min()), float(df["weight (kg)"].max())),
        step=1.0
    )

    min_height, max_height = st.slider(
        "Height (cm)",
        min_value=float(df["height (cm)"].min()),
        max_value=float(df["height (cm)"].max()),
        value=(float(df["height (cm)"].min()), float(df["height (cm)"].max())),
        step=1.0
    )

    min_sleep, max_sleep = st.slider(
        "Sleep Duration (h)", min_value=3.0, max_value=10.0, value=(3.0, 10.0), step=0.5
    )

    st.markdown("""<h4 style="margin-top:25px; color:#1e293b;">🏃 Lifestyle</h4>""",
                unsafe_allow_html=True)

    selected_exercise = st.multiselect(
        "Exercise Frequency",
        sorted(df["exercise"].dropna().unique().tolist()),
        default=st.session_state.selected_exercise
    )

    selected_sugar = st.multiselect(
        "Sugar Intake Level",
        sorted(df["sugar_intake"].dropna().unique().tolist()),
        default=st.session_state.selected_sugar
    )

    selected_habits = st.multiselect(
        "Lifestyle Habits",
        category_order,
        default=st.session_state.selected_habits
    )

# 5️⃣ DATA FILTERING

filtered_df = df[
    (df["age_group"].isin(selected_ages)) &
    (df["profession"].isin(selected_professions)) &
    (df["married"].isin(selected_married)) &
    (df["exercise"].isin(selected_exercise)) &
    (df["sugar_intake"].isin(selected_sugar)) &
    (df["habit_category"].isin(selected_habits)) &
    (df["bmi (kg/cm²)"] >= min_bmi) & (df["bmi (kg/cm²)"] <= max_bmi) &
    (df["weight (kg)"] >= min_weight) & (df["weight (kg)"] <= max_weight) &
    (df["height (cm)"] >= min_height) & (df["height (cm)"] <= max_height) &
    (df["sleep (h)"] >= min_sleep) & (df["sleep (h)"] <= max_sleep)
]

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")
    st.stop()


# 6️⃣ VISUALIZATIONS

render_stacked_bar(filtered_df, selected_ages, category_order)
render_treemap(filtered_df)
render_heatmap(filtered_df, selected_ages, category_order)
render_age_bmi_risk_sankey(filtered_df)
render_geo_map(filtered_df)
render_histogram(filtered_df)
render_network_diagram(filtered_df)
render_swarm(filtered_df)
render_violin(filtered_df)
render_ml_model(filtered_df)




# 7️⃣ RAW DATA
st.markdown("---")
st.subheader("📊 Raw Data (Filtered Results)")
hide_cols = ["country", "age_group", "habit_category"]
visible_df = filtered_df.drop(columns=hide_cols, errors="ignore")
st.dataframe(visible_df, use_container_width=True)






