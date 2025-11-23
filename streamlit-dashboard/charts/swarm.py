import streamlit as st
import plotly.express as px
import pandas as pd

def render_swarm(df):
    st.subheader("Swarm / Strip Plot (Jittered)")
    # Varsayılan olarak bmi vs habit_category
    x_col = "habit_category" if "habit_category" in df.columns else None
    y_col = "bmi (kg/cm²)" if "bmi (kg/cm²)" in df.columns else None

    if x_col is None or y_col is None:
        st.warning("Swarm için 'habit_category' veya 'bmi (kg/cm²)' sütunlarından biri yok.")
        return None

    sample = df.dropna(subset=[x_col, y_col])
    if sample.empty:
        st.warning("Swarm plot için yeterli veri yok.")
        return None

    fig = px.strip(
        sample,
        x=x_col,
        y=y_col,
        color="age_group" if "age_group" in df.columns else None,
        hover_data=["profession"] if "profession" in df.columns else None,
        title=f"Swarm-like strip plot: {y_col} by {x_col}"
        # Eski Plotly versiyonunda 'jitter' ve 'stripmode' desteklenmiyor,
        # bu yüzden kaldırdık.
    )

    st.plotly_chart(fig, use_container_width=True)
    return fig

