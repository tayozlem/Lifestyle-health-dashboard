import plotly.express as px
import streamlit as st
import pandas as pd

def render_heatmap(filtered_df, selected_ages, category_order):

    valid_age_groups = filtered_df["age_group"].unique()
    valid_habits = filtered_df["habit_category"].unique()

    # Heatmap tamamen gerçek veriye göre oluşturulmalı
    heatmap_data = (
        filtered_df.groupby(["age_group", "habit_category"])["sleep (h)"]
        .mean()
        .reset_index()
        .rename(columns={"sleep (h)": "avg_sleep"})
    )

    heatmap_data = heatmap_data[
        (heatmap_data["age_group"].isin(valid_age_groups)) &
        (heatmap_data["habit_category"].isin(valid_habits))
    ]

    fig = px.density_heatmap(
        heatmap_data,
        x="age_group",
        y="habit_category",
        z="avg_sleep",

        # Kontrastlı renk skalası
        color_continuous_scale=[
            [0.0, "#1a9850"],
            [0.25, "#91cf60"],
            [0.5, "#f7e027"],
            [0.75, "#fc8d59"],
            [1.0, "#d73027"]
        ],

        title="How Smoking & Alcohol Habits Affect Sleep Across Age Groups",
        hover_data={
            "avg_sleep": ":.2f",
            "age_group": True,
            "habit_category": True
        }
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Age Range:</b> %{x}<br>"
            "<b>Habit Status:</b> %{y}<br>"
            "<b>Mean Sleep:</b> %{z:.2f} h<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Age Range",
        yaxis_title="Habit Status",
        title_font=dict(size=22, family="Segoe UI Semibold", color="#1b2a49"),
        margin=dict(t=80, l=60, r=40, b=60),

        coloraxis_colorbar=dict(
            title="Mean Sleep (h)",   
            thickness=18,
            len=0.75
        )
    )

    st.plotly_chart(fig, use_container_width=True)






