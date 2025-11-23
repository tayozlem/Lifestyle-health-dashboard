# charts/violin_plot.py
import streamlit as st
import plotly.express as px

def render_violin(df):
    st.subheader("Violin Plot — BMI distribution by Age Group")
    if "bmi (kg/cm²)" not in df.columns or "age_group" not in df.columns:
        st.warning("Violin plot için 'bmi (kg/cm²)' veya 'age_group' sütunu yok.")
        return None

    sample = df.dropna(subset=["bmi (kg/cm²)", "age_group"])
    if sample.empty:
        st.warning("Violin plot için yeterli veri yok.")
        return None

    fig = px.violin(sample, x="age_group", y="bmi (kg/cm²)", color="age_group",
                    box=True, points="all", hover_data=["profession"] if "profession" in df.columns else None,
                    title="BMI distribution by Age Group (Violin)")
    st.plotly_chart(fig, use_container_width=True)
    return fig
