import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from charts.health_importance import render_health_importance

# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------
RISK_COLOR = {
    "Low": "#7dd3fc",
    "High": "#ef4444",
}

AGE_COLOR = "#c7d2fe"
BMI_COLOR = "#c7d2fe"

AGE_ORDER = ["18–25", "26–35", "36–45", "46–55", "56–65", "66–80"]
BMI_ORDER = ["Underweight", "Normal", "Overweight", "Obese"]

BMI_RANGE_TEXT = {
    "Underweight": "< 18.5",
    "Normal": "18.5 – 24.9",
    "Overweight": "25 – 29.9",
    "Obese": "≥ 30"
}


# ---------------------------------------------------------
# NORMALIZER
# ---------------------------------------------------------
def scale_values(values):
    v = np.array(values, dtype=float)
    if v.max() == v.min():
        return np.ones_like(v)
    return 1 + (v - v.min()) / (v.max() - v.min()) * 5


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------
def render_age_bmi_risk_sankey(filtered_df):

    df = filtered_df.copy()

    tab1, tab2 = st.tabs(["📊 Age–BMI → Risk Sankey", "💡 Feature Importance (RF)"])

    # ====================================================================================
    # TAB 1 — SANKEY
    # ====================================================================================
    with tab1:

        df["risk_label"] = df["health_risk"].apply(lambda x: "Low" if x <= 1.5 else "High")

        def bmi_cat(v):
            if v < 18.5: return "Underweight"
            elif v < 25: return "Normal"
            elif v < 30: return "Overweight"
            else: return "Obese"

        df["bmi_cat"] = df["bmi (kg/cm²)"].apply(bmi_cat)

        # AVAILABLE NODES
        age_nodes = [a for a in AGE_ORDER if a in df["age_group"].unique()]
        bmi_nodes = [b for b in BMI_ORDER if b in df["bmi_cat"].unique()]
        risk_nodes = ["Low", "High"]

        nodes = age_nodes + risk_nodes + bmi_nodes
        idx = {n: i for i, n in enumerate(nodes)}

        # ---------------------------------------------------------
        # AGE → RISK
        # ---------------------------------------------------------
        df1 = df.groupby(["age_group", "risk_label"]).size().reset_index(name="count")
        df1 = df1[df1["age_group"].isin(age_nodes)]

        src1 = [idx[a] for a in df1["age_group"]]
        tgt1 = [idx[r] for r in df1["risk_label"]]
        val1 = df1["count"].tolist()
        col1 = [RISK_COLOR[r] for r in df1["risk_label"]]
        hov1 = [f"{a} → {r}<br><b>{c}</b> people"
                for a, r, c in zip(df1["age_group"], df1["risk_label"], df1["count"])]

        # ---------------------------------------------------------
        # BMI → RISK
        # ---------------------------------------------------------
        df2 = df.groupby(["bmi_cat", "risk_label"]).size().reset_index(name="count")
        df2 = df2[df2["bmi_cat"].isin(bmi_nodes)]

        src2 = [idx[b] for b in df2["bmi_cat"]]
        tgt2 = [idx[r] for r in df2["risk_label"]]
        val2 = df2["count"].tolist()
        col2 = [RISK_COLOR[r] for r in df2["risk_label"]]
        hov2 = [f"{b} → {r}<br><b>{c}</b> people"
                for b, r, c in zip(df2["bmi_cat"], df2["risk_label"], df2["count"])]

        # Normalize
        scaled_vals = scale_values(val1 + val2)

        sources = src1 + src2
        targets = tgt1 + tgt2
        values = scaled_vals.tolist()
        link_colors = col1 + col2
        link_hover = hov1 + hov2

        # ---------------------------------------------------------
        # NODE HOVERS
        # ---------------------------------------------------------
        node_hover_text = []

        # Age nodes
        for age in age_nodes:
            g = df[df["age_group"] == age]
            total = len(g)
            low = len(g[g["risk_label"] == "Low"])
            high = len(g[g["risk_label"] == "High"])

            node_hover_text.append(
                f"<b>Age Group:</b> {age}<br>"
                f"Total People: {total}<br>"
                f"Low Risk: {low} ({(low/total*100):.1f}%)<br>"
                f"High Risk: {high} ({(high/total*100):.1f}%)"
            )

        # Risk nodes
        for r in risk_nodes:
            total = len(df[df["risk_label"] == r])
            node_hover_text.append(f"<b>{r} Risk</b><br>Total People: {total}")

        # BMI nodes
        for b in bmi_nodes:
            g = df[df["bmi_cat"] == b]
            total = len(g)
            low = len(g[g["risk_label"] == "Low"])
            high = len(g[g["risk_label"] == "High"])

            node_hover_text.append(
                f"<b>BMI Group:</b> {b}<br>"
                f"BMI Range: {BMI_RANGE_TEXT[b]}<br>"
                f"Total People: {total}<br>"
                f"Low Risk: {low} ({(low/total*100):.1f}%)<br>"
                f"High Risk: {high} ({(high/total*100):.1f}%)"
            )

        # ---------------------------------------------------------
        # NODE POSITIONS
        # ---------------------------------------------------------
        age_y = np.linspace(0.12, 0.88, len(age_nodes)).tolist()
        risk_y = [0.20, 0.50]
        bmi_y = [0.15, 0.35, 0.55, 0.75][:len(bmi_nodes)]

        xs = [0.03] * len(age_nodes) + [0.45, 0.45] + [0.88] * len(bmi_nodes)
        ys = age_y + risk_y + bmi_y

        node_colors = (
            [AGE_COLOR] * len(age_nodes) +
            [RISK_COLOR["Low"], RISK_COLOR["High"]] +
            [BMI_COLOR] * len(bmi_nodes)
        )

        # ---------------------------------------------------------
        # FIGURE (NO FONT INSIDE NODE — FIXED!)
        # ---------------------------------------------------------
        fig = go.Figure(
            data=[
                go.Sankey(
                    arrangement="snap",
                    node=dict(
                        pad=12,
                        thickness=20,
                        label=nodes,
                        color=node_colors,
                        line=dict(color="rgba(0,0,0,0.25)", width=0.6),
                        x=xs,
                        y=ys,
                        customdata=node_hover_text,
                        hovertemplate="%{customdata}<extra></extra>",
                    ),
                    link=dict(
                        source=sources,
                        target=targets,
                        value=values,
                        color=link_colors,
                        hovertemplate=link_hover,
                    ),
                )
            ]
        )

        # Global font control → **NODE LABELS DAHİL HER ŞEY SİYAH**
        fig.update_layout(
            title="<b>Effect of Age & BMI on Health Risk</b>",
            font=dict(size=15, family="Arial Black", color="black"),
            height=680,
            margin=dict(l=20, r=20, t=50, b=20),
        )

        st.plotly_chart(fig, use_container_width=True)

    # ====================================================================================
    # TAB 2
    # ====================================================================================
    with tab2:
        st.plotly_chart(render_health_importance(df), use_container_width=True)
