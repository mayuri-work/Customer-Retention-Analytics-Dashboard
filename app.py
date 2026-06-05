import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Customer Retention Analytics",
    page_icon="🏦",
    layout="wide"
)

hide_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

st.markdown(hide_style, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;padding:20px'>
<h1>🏦 Customer Retention Analytics Dashboard</h1>
<h4>Engagement & Product Utilization Analysis</h4>
</div>
""", unsafe_allow_html=True)

df = pd.read_csv("European_Bank.csv")

st.sidebar.title("🔍 Filters")

selected_geo = st.sidebar.multiselect(
    "Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[
    (df["Geography"].isin(selected_geo))
    &
    (df["Gender"].isin(selected_gender))
]

total_customers = len(filtered_df)

churn_rate = (
    filtered_df["Exited"].sum()
    /
    len(filtered_df)
) * 100

active_customers = len(
    filtered_df[
        filtered_df["IsActiveMember"] == 1
    ]
)

avg_balance = filtered_df["Balance"].mean()

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col2.metric(
    "📉 Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "✅ Active",
    f"{active_customers:,}"
)

col4.metric(
    "💰 Avg Balance",
    f"{avg_balance:,.0f}"
)

st.success(f"""
### Dashboard Summary

• Total Customers: {total_customers:,}

• Churn Rate: {churn_rate:.2f}%

• Active Customers: {active_customers:,}

• Average Balance: {avg_balance:,.0f}
""")

st.markdown("## 🚀 Dashboard Features")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ✅ Customer Churn Analysis
    
    ✅ Engagement Analytics
    
    ✅ Product Utilization Analysis
    
    ✅ Customer Segmentation
    
    ✅ KPI Tracking
    """)

with col2:
    st.success("""
    ✅ Geography Insights
    
    ✅ High-Value Customer Detector
    
    ✅ Relationship Strength Panel
    
    ✅ Interactive Filters
    
    ✅ Business Intelligence Dashboard
    """)
    st.markdown("---")
st.header("⚠️ Customer Risk Analysis")

risk_df = filtered_df.copy()

risk_df["RiskLevel"] = "Medium"

risk_df.loc[
    (risk_df["IsActiveMember"] == 1) &
    (risk_df["NumOfProducts"] >= 2),
    "RiskLevel"
] = "Low"

risk_df.loc[
    (risk_df["IsActiveMember"] == 0) &
    (risk_df["NumOfProducts"] <= 1),
    "RiskLevel"
] = "High"

risk_counts = risk_df["RiskLevel"].value_counts()

fig = px.pie(
    values=risk_counts.values,
    names=risk_counts.index,
    title="Customer Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🚨 Top At-Risk Customers")

high_risk = risk_df[
    risk_df["RiskLevel"] == "High"
]

st.dataframe(
    high_risk[
        [
            "CustomerId",
            "Geography",
            "Age",
            "Balance",
            "NumOfProducts",
            "IsActiveMember",
            "Exited"
        ]
    ].head(20)
)

st.markdown("---")
st.header("👵 Age Group Analysis")

age_df = filtered_df.copy()

age_df["AgeGroup"] = pd.cut(
    age_df["Age"],
    bins=[18,30,40,50,100],
    labels=[
        "18-30",
        "31-40",
        "41-50",
        "51+"
    ]
)

age_churn = age_df.groupby(
    "AgeGroup"
)["Exited"].mean().reset_index()

fig = px.bar(
    age_churn,
    x="AgeGroup",
    y="Exited",
    title="Churn Rate by Age Group"
)

st.plotly_chart(fig, use_container_width=True)



tab1,tab2,tab3,tab4 = st.tabs([
    "📊 Overview",
    "👥 Engagement",
    "🎯 Segmentation",
    "💰 High Value"
])

with tab1:

    col1,col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            filtered_df,
            x="Exited",
            color="Exited",
            title="Customer Churn Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.histogram(
            filtered_df,
            x="Geography",
            color="Exited",
            title="Geography vs Churn",
            barmode="group"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab2:

    engagement_ratio = (
        len(
            filtered_df[
                (filtered_df["IsActiveMember"]==1)
                &
                (filtered_df["Exited"]==0)
            ]
        )
        /
        len(
            filtered_df[
                filtered_df["IsActiveMember"]==1
            ]
        )
    ) * 100

    st.metric(
        "Engagement Retention Ratio",
        f"{engagement_ratio:.2f}%"
    )

    fig = px.histogram(
        filtered_df,
        x="IsActiveMember",
        color="Exited",
        title="Customer Activity vs Churn",
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    product_depth = filtered_df[
        filtered_df["Exited"]==0
    ]["NumOfProducts"].mean()

    st.metric(
        "Product Depth Index",
        f"{product_depth:.2f}"
    )

    fig = px.bar(
        filtered_df.groupby(
            "NumOfProducts"
        )["Exited"].mean().reset_index(),
        x="NumOfProducts",
        y="Exited",
        title="Product Count vs Churn Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab3:

    mean_balance = filtered_df["Balance"].mean()
    mean_salary = filtered_df["EstimatedSalary"].mean()

    loyal = len(
        filtered_df[
            (filtered_df["IsActiveMember"]==1)
            &
            (filtered_df["NumOfProducts"]>=2)
        ]
    )

    at_risk = len(
        filtered_df[
            (filtered_df["IsActiveMember"]==0)
            &
            (filtered_df["NumOfProducts"]<=1)
        ]
    )

    premium = len(
        filtered_df[
            (filtered_df["Balance"]>mean_balance)
            &
            (filtered_df["EstimatedSalary"]>mean_salary)
        ]
    )

    silent = len(
        filtered_df[
            (filtered_df["Balance"]>mean_balance)
            &
            (filtered_df["IsActiveMember"]==0)
        ]
    )

    growth = len(
        filtered_df[
            (filtered_df["IsActiveMember"]==1)
            &
            (filtered_df["NumOfProducts"]==1)
        ]
    )

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("Loyal", loyal)
    c2.metric("At Risk", at_risk)
    c3.metric("Premium", premium)
    c4.metric("Silent Churn", silent)
    c5.metric("Growth", growth)

    segment_df = pd.DataFrame({
        "Segment":[
            "Loyal",
            "At Risk",
            "Premium",
            "Silent Churn",
            "Growth"
        ],
        "Count":[
            loyal,
            at_risk,
            premium,
            silent,
            growth
        ]
    })

    fig = px.pie(
        segment_df,
        values="Count",
        names="Segment",
        title="Customer Segment Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab4:

    st.markdown("---")
    st.header("📦 Product Count Filter")

    product_threshold = st.slider(
    "Select Minimum Number of Products",
    min_value=1,
    max_value=4,
    value=2
    )

    product_customers = filtered_df[
    filtered_df["NumOfProducts"] >= product_threshold
    ]

    st.metric(
    "Customers Matching Product Criteria",
    len(product_customers)
    )

    st.dataframe(
    product_customers[
        [
            "CustomerId",
            "Geography",
            "Gender",
            "NumOfProducts",
            "Balance",
            "EstimatedSalary",
            "Exited"
        ]
    ].head(20)
    )
    balance_threshold = st.slider(
        "Balance Threshold",
        0,
        int(filtered_df["Balance"].max()),
        100000
    )

    salary_threshold = st.slider(
        "Salary Threshold",
        0,
        int(filtered_df["EstimatedSalary"].max()),
        100000
    )

    high_value = filtered_df[
        (filtered_df["Balance"]>=balance_threshold)
        &
        (filtered_df["EstimatedSalary"]>=salary_threshold)
    ]

    st.metric(
        "High Value Customers",
        len(high_value)
    )

    st.dataframe(high_value)

    temp = filtered_df.copy()

    temp["RelationshipScore"] = (
        temp["IsActiveMember"]*40 +
        (temp["NumOfProducts"]>=2)*25 +
        temp["HasCrCard"]*15 +
        (temp["Tenure"]>5)*20
    )

    st.metric(
        "Relationship Strength Index",
        f"{temp['RelationshipScore'].mean():.2f}"
    )

st.markdown("---")
st.header("🔍 Customer Search")

customer_id = st.number_input(
    "Enter Customer ID",
    value=int(filtered_df["CustomerId"].iloc[0])
)

customer = filtered_df[
    filtered_df["CustomerId"] == customer_id
]

if not customer.empty:
    st.dataframe(customer)
else:
    st.warning("Customer not found")

st.markdown("---")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_customers.csv",
    mime="text/csv"
)

st.markdown("---")
st.header("📌 Executive Summary")

st.success("""
• Churn Rate: 20.37%

• Engagement Retention Ratio: 85.73%

• Product Depth Index: 1.54

• High-Balance Disengagement Rate: 49.05%

• Credit Card Stickiness Score: 79.82%

• Relationship Strength Index: 52.46

Key Recommendation:
Focus retention efforts on high-value inactive customers and increase product adoption among active customers.
""")
