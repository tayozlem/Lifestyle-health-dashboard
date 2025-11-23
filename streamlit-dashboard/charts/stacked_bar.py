import plotly.express as px
import streamlit as st

def render_stacked_bar(filtered_df, selected_ages, category_order):

    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        return

    # ===============================================================
    # GROUPING – count + percentage
    # ===============================================================
    habit_counts = (
        filtered_df.groupby(["age_group", "habit_category"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )

    total_per_age = habit_counts.groupby("age_group")["count"].transform("sum")
    habit_counts["percentage"] = habit_counts["count"] / total_per_age * 100

    # ===============================================================
    # COLOR PALETTE
    # ===============================================================
    color_map = {
        "Alcohol Only": "#FFD54F",
        "Smoking Only": "#FF8C42",
        "Both (Smoking & Alcohol)": "#B71C1C",
        "None": "#66BB6A",
    }

    # ===============================================================
    # STACKED BAR → Y ekseni yüzdelik
    # Bar içi text → kişi sayısı
    # ===============================================================
    fig = px.bar(
        habit_counts,
        x="age_group",
        y="percentage",
        color="habit_category",
        title="<b>Percentage Distribution of Alcohol & Smoking Habits by Age Range</b>",
        category_orders={"habit_category": category_order, "age_group": selected_ages},
        color_discrete_map=color_map,
        height=650,
        text=habit_counts["count"].map(lambda x: f"{x} people")  # ⭐ sadece kişi sayısı
    )

    # ===============================================================
    # TEXT LABEL STYLE (Beautiful!)
    # ===============================================================
    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=14, color="black", family="Segoe UI"),
        hoverinfo="skip"   # default hover info’yu kapat
    )

    # ===============================================================
    # CUSTOM HOVER
    # ===============================================================
    for trace in fig.data:
        category = trace.name
        sub_df = habit_counts[habit_counts["habit_category"] == category]

        hovertext = [
            f"<b>Age Range:</b> {row['age_group']}<br>"
            f"<b>Habit Category:</b> {row['habit_category']}<br>"
            f"<b>Person Count:</b> {row['count']}<br>"
            f"<b>Percentage:</b> {row['percentage']:.1f}%"
            for _, row in sub_df.iterrows()
        ]

        trace.update(hovertemplate=hovertext)

    # ===============================================================
    # ELEGANT LAYOUT
    # ===============================================================
    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        bargap=0.06,
        xaxis_title="Age Range",
        yaxis_title="Percentage (%)",
        legend_title_text="Usage Category",
        title_font=dict(size=24, family="Segoe UI Semibold", color="#1b2a49"),
        xaxis=dict(showgrid=True, gridcolor="#efefef", title_font=dict(size=15)),
        yaxis=dict(showgrid=True, gridcolor="#efefef", title_font=dict(size=15)),
        margin=dict(t=80, l=50, r=50, b=60),
        hoverlabel=dict(bgcolor="white", font_size=14),
    )

    st.plotly_chart(fig, use_container_width=True)


