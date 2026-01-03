import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_bygender_df(df):
    bygender_df = (
        df
        .groupby("gender")
        .customer_id
        .nunique()
        .reset_index()
    )
    bygender_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bygender_df

def create_byage_df(df):
    byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    byage_df['age_group'] = pd.Categorical(byage_df['age_group'], ["Youth", "Adults", "Seniors"])
    
    return byage_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max", #mengambil tanggal order terakhir
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

all_df = pd.read_csv("Dashboard_Customers/all_data.csv")

datetime_columns = ["order_date", "delivery_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/mhvvn/dashboard_streamlit/refs/heads/main/img/tshirt.png", width=80)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
                (all_df["order_date"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bygender_df = create_bygender_df(main_df)
byage_df = create_byage_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header('My Collection Dashboard :sparkles:')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig = px.line(
    daily_orders_df,
    x="order_date",
    y="order_count",
    title="Daily Order Count",
    markers='o'
)

fig.update_traces(
    line=dict(
        width=2,
        color="#90CAF9"
    )
)
fig.update_layout(
    xaxis_title="Order Date",
    yaxis_title="Order Count"
)
st.plotly_chart(fig, width='stretch')

st.subheader("Best & Worst Performing Product")
best_product = sum_order_items_df.head(5)
worst_product = (
    sum_order_items_df
    .sort_values(by="quantity_x", ascending=True)
    .head(5)
)
col1, col2 = st.columns(2)

with col1:
    fig_best = px.bar(
        best_product,
        x="quantity_x",
        y="product_name",
        orientation="h",
        color="product_name",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_best.update_layout(
        title="Best Performing Product",  
        showlegend=True,
        xaxis_title="Quantity",
        yaxis_title="Product Name",
        height=400
    )
    st.plotly_chart(fig_best, width='stretch')

with col2:
    fig_worst = px.bar(
        worst_product,
        x="quantity_x",
        y="product_name",
        orientation="h",
        color="product_name",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_worst.update_layout(
        title="Worst Performing Product",
        showlegend=True,
        xaxis_title="Quantity",
        yaxis_title="Product Name",
        height=400
    )
    st.plotly_chart(fig_worst, width='stretch')

st.subheader("Customer Demographics")
col1, col2 = st.columns(2)

with col1:
    fig_gender = px.bar(
        bygender_df.sort_values(by="customer_count", ascending=False),
        x="gender",
        y="customer_count",
        color="gender",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_gender.update_layout(
        title="Number of Customer by Gender",
        showlegend=True,
        xaxis_title="Gender",
        yaxis_title="Customer Count",
        height=450
    )
    st.plotly_chart(fig_gender, width='stretch')

with col2:
    fig_age = px.bar(
        byage_df.sort_values(by="age_group", ascending=False),
        x="age_group",
        y="customer_count",
        color="age_group",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_age.update_layout(
        title="Number of Customer by Age",
        showlegend=True,
        xaxis_title="Age Group",
        yaxis_title="Customer Count",
        height=450
    )
    st.plotly_chart(fig_age, width='stretch')

fig_state = px.bar(
    bystate_df.sort_values(by="customer_count", ascending=False),
    x="customer_count",
    y="state",
    orientation="h",
    color="state",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_state.update_layout(
    title="Number of Customer by States",
    showlegend=True,
    xaxis_title="Customer Count",
    yaxis_title="State",
    height=400
)
st.plotly_chart(fig_state, width='stretch')

st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Recency (days)",
        value=round(rfm_df.recency.mean(), 1)
    )

with col2:
    st.metric(
        "Average Frequency",
        value=round(rfm_df.frequency.mean(), 2)
    )

with col3:
    st.metric(
        "Average Monetary",
        value=format_currency(rfm_df.monetary.mean(), "AUD", locale="es_CO")
    )

rfm_df["customer_id"] = rfm_df["customer_id"].astype(str)
col1, col2, col3 = st.columns(3)

with col1:
    top_recency = rfm_df.sort_values("recency", ascending=True).head(5)

    fig_recency = px.bar(
        top_recency,
        x="customer_id",
        y="recency",
        color_discrete_sequence=["#90CAF9"]
    )

    fig_recency.update_layout(
        title="Top 5 Customers by Recency",
        showlegend=False,
        xaxis_title="Customer ID",
        yaxis_title="Recency",        
        height=400
    )
    st.plotly_chart(fig_recency, width='stretch')

with col2:
    top_frequency = rfm_df.sort_values("frequency", ascending=False).head(5)

    fig_frequency = px.bar(
        top_frequency,
        x="customer_id",
        y="frequency",
        color_discrete_sequence=["#90CAF9"]
    )

    fig_frequency.update_layout(
        title="Top 5 Customers by Frequency",
        showlegend=False,
        xaxis_title="Customer ID",
        yaxis_title="Frequency",       
        height=400
    )
    st.plotly_chart(fig_frequency, width='stretch')

with col3:
    top_monetary = rfm_df.sort_values("monetary", ascending=False).head(5)

    fig_monetary = px.bar(
        top_monetary,
        x="customer_id",
        y="monetary",
        color_discrete_sequence=["#90CAF9"]
    )

    fig_monetary.update_layout(
        title="Top 5 Customers by Monetary",
        showlegend=False,
        xaxis_title="Customer ID",
        yaxis_title="Monetary",       
        height=400
    )
    st.plotly_chart(fig_monetary, width='stretch')

st.caption("Copyright (c) My Collection 2025")
