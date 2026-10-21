
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from pathlib import Path

st.set_page_config(
    page_title="SupplyShield AI",
    page_icon="🛡️",
    layout="wide"
)


# Futuristic glassmorphism theme
st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at top left, rgba(34, 211, 238, 0.10), transparent 38%), linear-gradient(135deg, #060918 0%, #101a36 52%, #24113f 100%);
    color: #f1f5ff;
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(255, 255, 255, 0.09),
        rgba(100, 116, 255, 0.045)
    );
    border: 1px solid rgba(103, 232, 249, 0.22);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.22), 0 0 18px rgba(34, 211, 238, 0.07);
    backdrop-filter: blur(12px);
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
h1, h2, h3 {
    color: #a5b4fc !important;
}

p, label, [data-testid="stCaptionContainer"] {
    color: #d5def5;
}

div[data-testid="stDataFrame"],
div[data-testid="stPlotlyChart"] {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(140, 160, 255, 0.16);
    border-radius: 16px;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

MODEL_PATH = Path(__file__).parent / "models" / "supplier_risk_model.joblib"
saved_data = joblib.load(MODEL_PATH)
model = saved_data["model"]


st.markdown("""
<div style="
    padding: 30px;
    border-radius: 22px;
    background: linear-gradient(120deg,
        rgba(99, 102, 241, 0.22),
        rgba(34, 211, 238, 0.10),
        rgba(168, 85, 247, 0.18));
    border: 1px solid rgba(165, 180, 252, 0.28);
    margin-bottom: 24px;
">
    <div style="
        color: #67e8f9;
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 700;
    ">INTELLIGENT SUPPLY CHAIN MONITORING</div>
    <h1 style="
        font-size: 42px;
        margin: 12px 0 4px 0;
        color: #f5f3ff;
    ">🛡️ SupplyShield AI</h1>
    <div style="
        font-size: 20px;
        color: #c4b5fd;
        font-weight: 600;
    ">Predict. Prevent. Protect.</div>
    <p style="
        margin-top: 12px;
        margin-bottom: 0;
        color: #dbeafe;
    ">Predict supplier disruption. Identify inventory risks.
    Recommend proactive recovery strategies.</p>
</div>
""", unsafe_allow_html=True)


# Sample supplier data with AI predictions
data = pd.DataFrame({
    "Supplier": [
        "Alpha Components",
        "Nova Materials",
        "Prime Logistics",
        "Vertex Electronics",
        "Apex Industries"
    ],
    "lead_time_days": [5, 14, 7, 12, 3],
    "supplier_delay_rate": [0.10, 0.75, 0.25, 0.60, 0.05],
    "order_volume": [300, 800, 450, 700, 200],
    "inventory_days": [20, 3, 12, 5, 30],
    "weather_risk": [0.10, 0.80, 0.20, 0.70, 0.10],
    "transport_risk": [0.15, 0.70, 0.25, 0.65, 0.10]
})

features = [
    "lead_time_days",
    "supplier_delay_rate",
    "order_volume",
    "inventory_days",
    "weather_risk",
    "transport_risk"
]

data["Delay Risk (%)"] = (
    model.predict_proba(data[features])[:, 1] * 100
).round(1)

data["Delivery Delay (days)"] = data["lead_time_days"]

data["Inventory Status"] = data["inventory_days"].apply(
    lambda days: "Critical" if days <= 3
    else "Low" if days <= 7
    else "Healthy"
)

# Overall supply-chain health indicator
high_risk_count = int((data["Delay Risk (%)"] >= 65).sum())

if high_risk_count >= 3:
    health_status = "CRITICAL"
    health_color = "#fb7185"
    health_message = "Multiple suppliers require immediate attention."
elif high_risk_count >= 1:
    health_status = "NEEDS ATTENTION"
    health_color = "#fbbf24"
    health_message = "At least one supplier requires preventive action."
else:
    health_status = "HEALTHY"
    health_color = "#22d3ee"
    health_message = "No suppliers currently meet the high-risk threshold."

st.markdown(f"""
<div style="
    padding: 18px 22px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid {health_color}66;
    margin: 12px 0 22px 0;
">
    <div style="font-size:12px; letter-spacing:2px; color:#cbd5e1;">
        SUPPLY CHAIN HEALTH STATUS
    </div>
    <div style="font-size:26px; font-weight:800; color:{health_color}; margin-top:6px;">
        ● {health_status}
    </div>
    <div style="color:#e2e8f0; margin-top:5px;">
        {health_message}
    </div>
</div>
""", unsafe_allow_html=True)

# Prototype disclaimer for judges
st.markdown("""
<div style="
    background: rgba(148, 163, 184, 0.10);
    border: 1px solid rgba(148, 163, 184, 0.30);
    border-radius: 12px;
    padding: 12px 16px;
    color: #cbd5e1;
    font-size: 13px;
">
<strong>Prototype Notice:</strong> SupplyShield AI demonstrates
supplier delay-risk analysis using sample data. Predictions are
experimental and should be validated with real operational data
before business decisions are made. This prototype is not connected
to a live SAP system.
</div>
""", unsafe_allow_html=True)

# Executive summary for judges
st.markdown("""
<h3 style="color:#a5b4fc;">📋 Executive Summary</h3>
""", unsafe_allow_html=True)

avg_risk = float(data["Delay Risk (%)"].mean())
critical_inventory = int(
    (data["Inventory Status"] == "Critical").sum()
)

st.info(
    f"SupplyShield AI is monitoring {len(data)} suppliers. "
    f"The average predicted delay risk is {avg_risk:.1f}%, "
    f"and {high_risk_count} supplier(s) meet the high-risk threshold. "
    f"There are {critical_inventory} critical-inventory item(s). "
    "Review the recovery planner to explore preventive actions."
)

st.download_button(
    label="📄 Download Executive Summary",
    data=(
        f"SupplyShield AI — Executive Summary\n\n"
        f"Suppliers monitored: {len(data)}\n"
        f"Average predicted delay risk: {avg_risk:.1f}%\n"
        f"High-risk suppliers: {high_risk_count}\n"
        f"Critical inventory items: {critical_inventory}\n\n"
        "Note: This is a prototype using sample data."
    ),
    file_name="SupplyShield_Executive_Summary.txt",
    mime="text/plain",
    use_container_width=True
)

# Summary metrics

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🏭 Suppliers Monitored", len(data))
col2.metric("🚨High-Risk Suppliers",
    int((data["Delay Risk (%)"] >= 65).sum())
)
col3.metric(
    "Critical Inventory Items",
    int((data["Inventory Status"] == "Critical").sum())
)

col4.metric(
    "Average Delay Risk",
    f'{data["Delay Risk (%)"].mean():.1f}%'
)

col5.metric(
    "Medium-Risk Suppliers",
    int((
        (data["Delay Risk (%)"] >= 40) &
        (data["Delay Risk (%)"] < 65)
    ).sum())
)


st.divider()

# Supplier risk chart

st.markdown("""
<h2 style="
    color: #67e8f9;
    font-size: 25px;
    font-weight: 700;
    border-left: 4px solid #a78bfa;
    padding-left: 12px;
    margin-top: 20px;
">
    Supplier Risk Overview
</h2>
""", unsafe_allow_html=True)



fig = px.bar(
    data,
    x="Supplier",
    y="Delay Risk (%)",
    color="Delay Risk (%)",
    color_continuous_scale=[
        [0, "#22d3ee"],
        [0.5, "#818cf8"],
        [1, "#c084fc"]
    ],
    range_y=[0, 100],
    text="Delay Risk (%)"
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e0e7ff",
    title_font_color="#a5b4fc",
    xaxis=dict(
        title="Supplier",
        gridcolor="rgba(165,180,252,0.10)"
    ),
    yaxis=dict(
        title="Delay Risk (%)",
        gridcolor="rgba(165,180,252,0.15)"
    ),
    coloraxis_colorbar=dict(
        title="Risk %",
        tickfont=dict(color="#e0e7ff"),
        title_font_color="#e0e7ff"
    )
)

fig.update_traces(
    textposition="outside",
    textfont=dict(color="#f5f3ff"),
    marker_line_color="rgba(255,255,255,0.25)",
    marker_line_width=1
)


fig.update_layout(
    xaxis_title="Supplier",
    yaxis_title="Delay risk (%)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,13,32,0.35)",
    font=dict(
        color="#cbd5e1",
        family="Arial"
    ),
    title_font=dict(
        color="#a5b4fc",
        size=18
    ),
    xaxis=dict(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.10)"
    ),
    yaxis=dict(
        gridcolor="rgba(148,163,184,0.12)",
        zerolinecolor="rgba(148,163,184,0.10)",
        ticksuffix="%"
    ),
    margin=dict(l=15, r=15, t=25, b=15)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<h3 style="color:#a5b4fc; margin-top:24px;">
    📊 Supply Chain Risk Distribution
</h3>
""", unsafe_allow_html=True)

risk_counts = pd.Series({
    "Low Risk": int((data["Delay Risk (%)"] < 40).sum()),
    "Medium Risk": int((
        (data["Delay Risk (%)"] >= 40) &
        (data["Delay Risk (%)"] < 65)
    ).sum()),
    "High Risk": int((data["Delay Risk (%)"] >= 65).sum())
})

risk_fig = px.pie(
    names=risk_counts.index,
    values=risk_counts.values,
    hole=0.65,
    color=risk_counts.index,
    color_discrete_map={
        "Low Risk": "#22d3ee",
        "Medium Risk": "#a78bfa",
        "High Risk": "#fb7185"
    }
)

risk_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e0e7ff",
    legend_title_text="Risk Level"
)

risk_fig.update_traces(
    textinfo="label+percent",
    marker_line_color="rgba(255,255,255,0.2)",
    marker_line_width=2
)

st.plotly_chart(risk_fig, use_container_width=True)


# Supplier table
st.subheader("Supplier Intelligence")


risk_filter = st.selectbox(
    "Filter suppliers",
    ["All", "High Risk", "Medium Risk", "Low Risk"]
)



filtered = data.copy()

if risk_filter == "High Risk":
    filtered = data[data["Delay Risk (%)"] >= 65]

elif risk_filter == "Medium Risk":
    filtered = data[
        (data["Delay Risk (%)"] >= 40) &
        (data["Delay Risk (%)"] < 65)
    ]

elif risk_filter == "Low Risk":
    filtered = data[data["Delay Risk (%)"] < 40]



st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="📥 Download Supplier Risk Report",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="SupplyShield_Supplier_Risk_Report.csv",
    mime="text/csv",
    use_container_width=True
)



# Automated alerts

st.markdown("""
<h2 style="
    color: #f0abfc;
    font-size: 25px;
    font-weight: 700;
    border-left: 4px solid #22d3ee;
    padding-left: 12px;
    margin-top: 28px;
">
    🚨 Risk Alerts
</h2>
""", unsafe_allow_html=True)


for _, supplier in data.iterrows():
    if supplier["Delay Risk (%)"] >= 65:
        st.warning(
            f'{supplier["Supplier"]}: '
            f'{supplier["Delay Risk (%)"]}% delay risk. '
            "Review inventory and alternative suppliers."
        )

st.info(
    "Prototype notice: Current supplier risk scores are "
    "sample values, not predictions from a trained AI model."
)

# AI Recovery Planner
st.divider()


st.markdown("""
<h2 style="
    color: #67e8f9;
    font-size: 28px;
    font-weight: 700;
    border-left: 4px solid #a78bfa;
    padding-left: 14px;
    margin-top: 20px;
">
    🛡️ AI Recovery Planner
</h2>
""", unsafe_allow_html=True)

st.write(
    "Use the supplier's AI-predicted delay risk to plan "
    "a recovery strategy before a shortage occurs."
)

selected_supplier = st.selectbox(
    "Select a supplier to plan recovery",
    data["Supplier"].tolist()
)

supplier_row = data[
    data["Supplier"] == selected_supplier
].iloc[0]

risk = float(supplier_row["Delay Risk (%)"])


st.markdown("""
<h3 style="color:#a5b4fc;">🔍 Why is this supplier at risk?</h3>
""", unsafe_allow_html=True)

reason_col1, reason_col2, reason_col3 = st.columns(3)

reason_col1.metric(
    "Lead Time",
    f'{supplier_row["lead_time_days"]} days'
)

reason_col2.metric(
    "Supplier Delay Rate",
    f'{supplier_row["supplier_delay_rate"]}%'
)

reason_col3.metric(
    "Inventory Coverage",
    f'{supplier_row["inventory_days"]} days'
)

st.markdown("""
<h3 style="color:#a5b4fc;">📊 Supplier Risk Indicators</h3>
""", unsafe_allow_html=True)

factor_data = pd.DataFrame({
    "Indicator": [
        "Lead Time",
        "Supplier Delay Rate",
        "Inventory Coverage"
    ],
    "Value": [
        float(supplier_row["lead_time_days"]),
        float(supplier_row["supplier_delay_rate"]),
        float(supplier_row["inventory_days"])
    ]
})

factor_fig = px.bar(
    factor_data,
    x="Indicator",
    y="Value",
    color="Indicator",
    color_discrete_sequence=[
        "#22d3ee", "#a78bfa", "#f472b6"
    ],
    text="Value"
)

factor_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e0e7ff",
    showlegend=False,
    xaxis_title="",
    yaxis_title="Recorded Value",
    yaxis=dict(gridcolor="rgba(165,180,252,0.15)")
)

factor_fig.update_traces(textposition="outside")

st.plotly_chart(factor_fig, use_container_width=True)


st.markdown(f"""
<div style="
    padding: 22px;
    border-radius: 18px;
    background: linear-gradient(120deg,
        rgba(34, 211, 238, 0.12),
        rgba(139, 92, 246, 0.18));
    border: 1px solid rgba(103, 232, 249, 0.30);
    margin: 12px 0 20px 0;
">
    <div style="
        color: #c4b5fd;
        font-size: 14px;
        letter-spacing: 1px;
    ">AI-PREDICTED DELAY RISK</div>
    <div style="
        color: #67e8f9;
        font-size: 42px;
        font-weight: 800;
        margin-top: 6px;
    ">{risk:.1f}%</div>
    <div style="
        color: #dbeafe;
        font-size: 13px;
    ">Model-estimated risk for the selected supplier</div>
</div>
""", unsafe_allow_html=True)


st.subheader("Recommended Recovery Strategy")


if risk >= 65:
    st.markdown(f"""
    <div style="
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(244,63,94,0.16), rgba(139,92,246,0.12));
        border: 1px solid rgba(251,113,133,0.45);
        margin-top: 12px;
    ">
        <div style="color:#fda4af;font-size:13px;letter-spacing:2px;">
            CRITICAL RISK • IMMEDIATE ACTION
        </div>
        <h3 style="color:#fecdd3;margin-bottom:8px;">
            🚨 High Risk Detected
        </h3>
        <p style="color:#f1f5f9;">
            Activate an alternative supplier to reduce disruption exposure.
        </p>
        <p style="color:#e2e8f0;">
            <b>Next steps:</b> Check available inventory and transfer stock if possible.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif risk >= 40:
    st.markdown("""
    <div style="
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(251,191,36,0.12), rgba(139,92,246,0.12));
        border: 1px solid rgba(251,191,36,0.4);
        margin-top: 12px;
    ">
        <div style="color:#fcd34d;font-size:13px;letter-spacing:2px;">
            PREVENTIVE ACTION
        </div>
        <h3 style="color:#fde68a;margin-bottom:8px;">
            ⚠️ Medium Risk Detected
        </h3>
        <p style="color:#f1f5f9;">
            Prepare a backup plan before the risk escalates.
        </p>
        <p style="color:#e2e8f0;">
            <b>Next steps:</b> Check inventory and contact the supplier to confirm delivery.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(34,211,238,0.12), rgba(139,92,246,0.12));
        border: 1px solid rgba(103,232,249,0.35);
        margin-top: 12px;
    ">
        <div style="color:#67e8f9;font-size:13px;letter-spacing:2px;">
            NORMAL MONITORING
        </div>
        <h3 style="color:#a5f3fc;margin-bottom:8px;">
            ✅ Low Risk Detected
        </h3>
        <p style="color:#f1f5f9;">
            Continue monitoring the supplier's delivery performance.
        </p>
        <p style="color:#e2e8f0;">
            <b>Next steps:</b> Track delivery status and maintain suitable inventory.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<h3 style="color:#a5b4fc; margin-top:28px;">
    ✅ Recovery Action Checklist
</h3>
<p style="color:#cbd5e1;">
    Track the actions taken for the selected supplier.
</p>
""", unsafe_allow_html=True)

action_key = f"recovery_{selected_supplier}"

st.checkbox(
    "Review current inventory levels",
    key=f"{action_key}_inventory"
)

st.checkbox(
    "Contact supplier to confirm delivery",
    key=f"{action_key}_contact"
)

st.checkbox(
    "Evaluate alternative suppliers",
    key=f"{action_key}_alternative"
)

st.checkbox(
    "Document recovery decisions",
    key=f"{action_key}_document"
)


st.markdown("""
<div style="
    margin-top: 40px;
    padding: 20px;
    text-align: center;
    border-top: 1px solid rgba(165,180,252,0.25);
">
    <div style="
        color: #a5b4fc;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 2px;
    ">🛡️ SupplyShield AI</div>
    <p style="color: #94a3b8; font-size: 12px;">
        Predict. Prevent. Protect. · AI-Powered Supply Chain Resilience
    </p>
    <p style="color: #64748b; font-size: 11px;">
        Prototype demonstration · Predictions use synthetic training data
    </p>
</div>
""", unsafe_allow_html=True)