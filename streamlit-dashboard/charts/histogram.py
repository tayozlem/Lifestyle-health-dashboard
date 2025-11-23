
import streamlit as st
import plotly.express as px

def render_histogram(df):
    st.subheader("Histogram — Age distribution / BMI distribution")

    # İki küçük histogram gösterimi yan yana
    cols = st.columns(2)
    with cols[0]:
        if "age" in df.columns:
            fig_age = px.histogram(df.dropna(subset=["age"]), x="age", nbins=20, title="Age distribution")
            st.plotly_chart(fig_age, use_container_width=True)
        else:
            st.info("Age sütunu bulunamadı.")

    with cols[1]:
        if "bmi (kg/cm²)" in df.columns:
            fig_bmi = px.histogram(df.dropna(subset=["bmi (kg/cm²)"]), x="bmi (kg/cm²)", nbins=20, title="BMI distribution")
            st.plotly_chart(fig_bmi, use_container_width=True)
        else:
            st.info("BMI sütunu bulunamadı.")
    return True
