import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Sales Performance Dashboard",
                   layout="wide")

# -------------------------------------------------------
# LOAD DATA (Safe Path)
# -------------------------------------------------------
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_path = os.path.join(project_root, "data", "Superstore.csv")

    df = pd.read_csv(file_path, encoding="latin1")
    df["Profit Margin"] = df["Profit"] / df["Sales"]
    return df

df = load_data()

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------
st.sidebar.title("📊 Dashboard Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------
st.title("📈 Superstore Sales Performance Dashboard")
st.markdown("Advanced Business Intelligence Dashboard")

# -------------------------------------------------------
# ADVANCED KPIs
# -------------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
avg_order_value = total_sales / total_orders if total_orders > 0 else 0
profit_margin = (total_profit / total_sales) if total_sales > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🧾 Total Orders", total_orders)
col4.metric("💵 Avg Order Value", f"${avg_order_value:,.2f}")
col5.metric("📊 Profit Margin", f"{profit_margin:.2%}")

st.markdown("---")

# -------------------------------------------------------
# SALES BY REGION
# -------------------------------------------------------
st.subheader("🌍 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().sort_values()

fig1, ax1 = plt.subplots()
sns.barplot(x=region_sales.values,
            y=region_sales.index,
            ax=ax1)
ax1.set_xlabel("Sales")
ax1.set_ylabel("Region")

st.pyplot(fig1)

# -------------------------------------------------------
# CATEGORY PERFORMANCE
# -------------------------------------------------------
st.subheader("🏷 Category Performance")

category_perf = filtered_df.groupby("Category")[["Sales", "Profit"]].sum()

fig2, ax2 = plt.subplots()
category_perf.plot(kind="bar", ax=ax2)
st.pyplot(fig2)

# -------------------------------------------------------
# TOP 10 SUB-CATEGORIES
# -------------------------------------------------------
st.subheader("🏆 Top 10 Sub-Categories by Profit")

top_subcat = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots()
sns.barplot(x=top_subcat.values,
            y=top_subcat.index,
            ax=ax3)

st.pyplot(fig3)

# -------------------------------------------------------
# DISCOUNT IMPACT
# -------------------------------------------------------
st.subheader("🔥 Discount vs Profit Analysis")

fig4, ax4 = plt.subplots()
sns.scatterplot(data=filtered_df,
                x="Discount",
                y="Profit",
                alpha=0.6,
                ax=ax4)

st.pyplot(fig4)

# -------------------------------------------------------
# DOWNLOAD REPORT
# -------------------------------------------------------
st.markdown("---")
st.subheader("📥 Download Filtered Report")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv",
)

st.markdown("Built with Streamlit • Pandas • Seaborn")
