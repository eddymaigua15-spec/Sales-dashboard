import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Performance Intelligence Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.sidebar.header("Filters")

product_filter = st.sidebar.multiselect(
    "Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered = df[(df["Product"].isin(product_filter)) & (df["Region"].isin(region_filter))]

total_sales = filtered["Sales"].sum()
total_units = filtered["Units"].sum()
avg_sales = filtered["Sales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"KES {total_sales:,.0f}")
col2.metric("Total Units", f"{total_units:,.0f}")
col3.metric("Average Sale", f"KES {avg_sales:,.0f}")

st.line_chart(filtered.groupby("Date")["Sales"].sum())
st.bar_chart(filtered.groupby("Product")["Sales"].sum())
st.bar_chart(filtered.groupby("Region")["Sales"].sum())
