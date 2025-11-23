import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go


# ==========================================================
# 1) FEATURE GROUPING (Sleep & Health Risk) — FIXED VERSION
# ==========================================================
def preprocess_for_network(df):

    # Fill missing values BEFORE categorization
    df = df.copy()
    df["smoking"] = df["smoking"].fillna("Unknown").astype(str)
    df["alcohol"] = df["alcohol"].fillna("Unknown").astype(str)
    df["exercise"] = df["exercise"].fillna("Unknown").astype(str)

    # Sleep grouping
    sleep_bins = [0, 5, 7, 9, 50]
    sleep_labels = ["Low Sleep (0–5)", "Medium Sleep (6–7)", "Good Sleep (8–9)", "High Sleep (10+)"]

    df["sleep_group"] = pd.cut(
        df["sleep (h)"].fillna(0),   # fillna FIX
        bins=sleep_bins,
        labels=sleep_labels,
        include_lowest=True
    ).astype(str)   # convert categorical → string FIX

    # Health risk grouping
    risk_map = {
        1: "Low Risk",
        2: "Moderate Risk",
        3: "High Risk",
        4: "Very High Risk",
        5: "Extreme Risk"
    }

    df["risk_group"] = df["health_risk"].map(risk_map).fillna("Unknown").astype(str)

    return df[["smoking", "alcohol", "exercise", "sleep_group", "risk_group"]]


# ==========================================================
# 2) BUILD 5-LAYER NETWORK GRAPH
# ==========================================================
def build_health_network_graph(df):

    G = nx.Graph()

    layers = {
        "smoking": 0,
        "alcohol": 1,
        "exercise": 2,
        "sleep_group": 3,
        "risk_group": 4
    }

    # NODE CREATION
    for col, layer in layers.items():
        for val in df[col].unique():
            G.add_node(
                f"{col}:{val}",
                layer=layer,
                category=col,
                value=val
            )

    # EDGE CREATION (smoking → alcohol → exercise → sleep → risk)
    for _, row in df.iterrows():
        nodes = [
            f"smoking:{row['smoking']}",
            f"alcohol:{row['alcohol']}",
            f"exercise:{row['exercise']}",
            f"sleep_group:{row['sleep_group']}",
            f"risk_group:{row['risk_group']}"
        ]

        for u, v in zip(nodes, nodes[1:]):
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
            else:
                G.add_edge(u, v, weight=1)

    return G


# ==========================================================
# 3) REDUCED-OVERLAP 3D LAYOUT
# ==========================================================
def layered_layout_3d(G):

    pos = {}
    SPACING_X = 14
    SPACING_Y = 7
    SPACING_Z = 5

    for layer in range(5):
        layer_nodes = [n for n, d in G.nodes(data=True) if d["layer"] == layer]
        for i, node in enumerate(layer_nodes):
            pos[node] = (
                layer * SPACING_X,
                (i % 10) * SPACING_Y,
                (i // 10) * SPACING_Z
            )

    return pos


# ==========================================================
# 4) PLOTLY GRAPH
# ==========================================================
def nx_to_plotly_3d(G):

    pos = layered_layout_3d(G)

    # Edges
    edge_x, edge_y, edge_z = [], [], []
    for u, v, d in G.edges(data=True):
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode="lines",
        line=dict(color="rgba(70,70,70,0.65)", width=3),
        hoverinfo="none",
        name="Connections"
    )

    # Node Colors
    COLOR_MAP = {
        "smoking": "crimson",
        "alcohol": "mediumseagreen",
        "exercise": "royalblue",
        "sleep_group": "gold",
        "risk_group": "purple"
    }

    category_traces = []

    for category, color in COLOR_MAP.items():
        xs, ys, zs, sizes, customdata = [], [], [], [], []

        for n, d in G.nodes(data=True):
            if d["category"] == category:
                x, y, z = pos[n]
                xs.append(x)
                ys.append(y)
                zs.append(z)
                sizes.append(G.degree(n) * 4 + 18)
                customdata.append([d["value"], G.degree(n)])

        trace = go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode="markers",
            name=category,
            marker=dict(
                size=sizes,
                color=color,
                opacity=0.92,
                line=dict(color="black", width=1)
            ),
            customdata=customdata,
            hovertemplate="<b>%{customdata[0]}</b><br>"
                          "Connections: %{customdata[1]}<extra></extra>"
        )
        category_traces.append(trace)

    fig = go.Figure(data=[edge_trace] + category_traces)

    fig.update_layout(
        margin=dict(l=0, r=0, t=70, b=0),
        legend=dict(x=0.84, y=0.97, bgcolor="rgba(255,255,255,0.85)"),

        scene=dict(
            xaxis=dict(title="Lifestyle → Sleep → Risk"),
            yaxis=dict(title="Y"),
            zaxis=dict(title="Z"),
            aspectmode="manual",
            aspectratio=dict(x=4, y=2.2, z=2)
        ),

        scene_camera=dict(
            eye=dict(x=2.7, y=2.5, z=1.3)
        )
    )

    return fig


# ==========================================================
# 5) STREAMLIT RENDER
# ==========================================================
def render_network_diagram(df):
    st.subheader("🌐 3D Network — Lifestyle Factors → Sleep → Health Risk")
    processed_df = preprocess_for_network(df)
    G = build_health_network_graph(processed_df)
    fig = nx_to_plotly_3d(G)
    st.plotly_chart(fig, use_container_width=True)
