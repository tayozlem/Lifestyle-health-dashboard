import streamlit as st
import plotly.express as px
import pandas as pd

def render_geo_map(df: pd.DataFrame):
    st.subheader("Geographical Map")

    if "latitude" in df.columns and "longitude" in df.columns:
        sample = df.dropna(subset=["latitude", "longitude"])
        if not sample.empty:
            fig_points = px.scatter_geo(
                sample,
                lat="latitude",
                lon="longitude",
                hover_name="profession" if "profession" in df.columns else None,
                size="bmi (kg/cm²)" if "bmi (kg/cm²)" in df.columns else None,
                projection="natural earth",
                title="Geographical distribution (lat/lon)"
            )
            st.plotly_chart(fig_points, use_container_width=True)

    if "country" not in df.columns:
        st.info("Geo map için 'country' sütunu gerekli.")
        return None

    has_exercise = "exercise" in df.columns
    has_sleep_h = "sleep (h)" in df.columns
    has_sleep = "sleep" in df.columns
    has_sugar = "sugar_intake" in df.columns
    has_risk = "health_risk" in df.columns

    sleep_col = "sleep (h)" if has_sleep_h else ("sleep" if has_sleep else None)

    exercise_map = {"low": 1, "medium": 2, "high": 3}
    sugar_map = {"low": 1, "medium": 2, "high": 3}

    df = df.copy()
    df["exercise_num"] = df["exercise"].map(exercise_map)
    df["sugar_num"] = df["sugar_intake"].map(sugar_map)
    df[sleep_col] = pd.to_numeric(df[sleep_col], errors="coerce")
    df["health_risk_num"] = pd.to_numeric(df["health_risk"], errors="coerce")

    df_valid = df.dropna(subset=["exercise_num", "sugar_num", sleep_col, "health_risk_num", "country"])
    if df_valid.empty:
        st.warning("Geçerli satır kalmadı.")
        return None

    df_valid["lifestyle_score"] = df_valid["exercise_num"] + df_valid[sleep_col] - df_valid["sugar_num"]
    df_valid["is_high_risk"] = (df_valid["health_risk_num"] >= 3).astype(int)

    grouped = df_valid.groupby("country", as_index=False).agg(
        lifestyle_score=("lifestyle_score", "mean"),
        high_risk_share=("is_high_risk", "mean"),
        avg_sugar=("sugar_num", "mean"),
        avg_exercise=("exercise_num", "mean"),
        avg_sleep=(sleep_col, "mean"),
        count=("country", "size"),
    )

    grouped["lifestyle_score"] = grouped["lifestyle_score"].round(2)
    grouped["high_risk_share"] = (grouped["high_risk_share"] * 100).round(1)
    grouped["avg_sugar"] = grouped["avg_sugar"].round(2)
    grouped["avg_exercise"] = grouped["avg_exercise"].round(2)
    grouped["avg_sleep"] = grouped["avg_sleep"].round(2)

    metric = st.radio(
        "Select metric:",
        ("Lifestyle score", "High risk share (%)")
    )

    if metric == "Lifestyle score":
        fig = px.choropleth(
            grouped,
            locations="country",
            locationmode="country names",
            color="lifestyle_score",
            hover_name="country",
            hover_data={
                "lifestyle_score": True,
                "high_risk_share": True,
                "avg_sugar": True,
                "avg_exercise": True,
                "avg_sleep": True,
                "count": True,
            },
            color_continuous_scale="RdYlGn",
            projection="natural earth",
            title="Lifestyle Score by Country",
        )
    else:
        fig = px.choropleth(
            grouped,
            locations="country",
            locationmode="country names",
            color="high_risk_share",
            hover_name="country",
            hover_data={
                "high_risk_share": True,
                "lifestyle_score": True,
                "avg_sugar": True,
                "avg_exercise": True,
                "avg_sleep": True,
                "count": True,
            },
            color_continuous_scale="Reds",
            projection="natural earth",
            title="High Health Risk Share (%) by Country",
        )

    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, height=600)
    st.plotly_chart(fig, use_container_width=True)
    return fig