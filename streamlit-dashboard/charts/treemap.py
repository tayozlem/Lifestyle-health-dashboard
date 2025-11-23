import plotly.express as px
import streamlit as st
import numpy as np

def render_treemap(filtered_df):

    # Custom exercise and sugar labels
    exercise_labels = {
        "none": "Those who do not exercise",
        "low": "Those who rarely exercise",
        "medium": "Those who exercise regularly",
        "high": "Those who exercise frequently"
    }

    sugar_labels = {
        "low": "Low Sugar Intake",
        "medium": "Moderate Sugar Intake",
        "high": "High Sugar Intake"
    }

    # Safe copy
    df = filtered_df.copy()
    df["exercise_label"] = df["exercise"].map(exercise_labels)
    df["sugar_label"]   = df["sugar_intake"].map(sugar_labels)

    # Group dataset
    treemap_data = (
        df.groupby(["exercise_label", "sugar_label"], as_index=False)
        .agg(
            count=("age", "size"),
            avg_bmi=("bmi (kg/cm²)", "mean")
        )
    )

    bmi_min = treemap_data["avg_bmi"].min()
    bmi_max = treemap_data["avg_bmi"].max()

    # Base treemap
    fig = px.treemap(
        treemap_data,
        path=["exercise_label", "sugar_label"],
        values="count",
        color="avg_bmi",
        color_continuous_scale=[
            [0.0, "#00a65a"],
            [0.25, "#a8d96f"],
            [0.5, "#fff176"],
            [0.75, "#f57c00"],
            [1.0, "#b71c1c"]
        ],
        range_color=(bmi_min, bmi_max),
        title="The Effect of Sugar Consumption and Exercise on BMI"
    )

    # -----------------------------------------------------------------------
    # ⭐ CUSTOMDATA → hover metni
    # -----------------------------------------------------------------------
    custom_hover_list = []

    for ex, sug, count, bmi in zip(
        treemap_data["exercise_label"],
        treemap_data["sugar_label"],
        treemap_data["count"],
        treemap_data["avg_bmi"]
    ):
        level1_text = (
            f"<b>This box represents the group of “{ex}”.</b><br>"
            f"There are <b>{count} people</b>.<br>"
            f"Average BMI: <b>{bmi:.2f}</b>"
        )

        level2_text = (
            f"<b>This box represents the group of “{ex}” and “{sug}”.</b><br>"
            f"There are <b>{count} people</b>.<br>"
            f"Average BMI: <b>{bmi:.2f}</b>"
        )

        custom_hover_list.append((level1_text, level2_text))

    assigned_hovers = []
    for node_id in fig.data[0]["ids"]:
        if "/" in node_id:
            ex, sug = node_id.split("/")
            idx = treemap_data[
                (treemap_data["exercise_label"] == ex) &
                (treemap_data["sugar_label"] == sug)
            ].index[0]
            assigned_hovers.append(custom_hover_list[idx][1])
        else:
            idx = treemap_data[
                treemap_data["exercise_label"] == node_id
            ].index[0]
            assigned_hovers.append(custom_hover_list[idx][0])

    fig.data[0].customdata = np.array(assigned_hovers, dtype=object)

    fig.update_traces(
        hovertemplate="%{customdata}<extra></extra>",
        texttemplate="<b>%{label}</b><br>%{value} people",
        textfont=dict(size=16, family="Segoe UI Semibold", color="white"),
        tiling=dict(pad=4)
    )

    # -----------------------------------------------------------------------
    # ⭐ Advanced Interaction Tools (Zoom, Pan, Autoscale…)
    # -----------------------------------------------------------------------
    fig.update_layout(
        dragmode="zoom",
        hovermode="closest",
        title_font=dict(size=24, family="Segoe UI Semibold", color="#1b2a49"),
        margin=dict(t=80, l=20, r=20, b=20),
        coloraxis_colorbar=dict(
            title="Average BMI (kg/cm²)",
            len=0.8,
            thickness=18
        )
    )

    config = {
        "displayModeBar": True,
        "scrollZoom": True,
        "displaylogo": False,
        "modeBarButtonsToAdd": [
            "zoom2d",
            "pan2d",
            "select2d",
            "lasso2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d"
        ]
    }

    # Display
    st.plotly_chart(fig, use_container_width=True, config=config)
