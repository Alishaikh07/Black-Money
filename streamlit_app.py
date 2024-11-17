import streamlit as st
import pandas as pd
import altair as alt
st.sidebar.image("C:/Users/user/live project of masai unit 2/Black Money.png",use_container_width=True)

# Load dataset
df = pd.read_csv('Big_Black_Money_Dataset.csv')

# Convert 'Date of Transaction' to datetime
df['Date of Transaction'] = pd.to_datetime(df['Date of Transaction'])

# Title and Introduction
st.title("Big Black Money Insights 💰")
st.write("Explore transactions, risk scores, and uncover insights interactively.")

# Sidebar for Filters
st.sidebar.header("Filters")

# Country Filter
selected_country = st.sidebar.multiselect(
    "Select Originating Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

# Transaction Type Filter
selected_transaction_type = st.sidebar.multiselect(
    "Select Transaction Type",
    options=df['Transaction Type'].unique(),
    default=df['Transaction Type'].unique()
)

# Amount range slider
amount_range = st.sidebar.slider(
    "Select Transaction Amount Range (USD)",
    int(df['Amount (USD)'].min()),
    int(df['Amount (USD)'].max()),
    (10000, 1000000)
)

# Date range filter
min_date = df['Date of Transaction'].min()
max_date = df['Date of Transaction'].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date.date(), max_date.date()],
    min_value=min_date.date(),
    max_value=max_date.date()
)

# Risk Score slider
risk_score_range = st.sidebar.slider(
    "Select Risk Score Range",
    int(df['Money Laundering Risk Score'].min()),
    int(df['Money Laundering Risk Score'].max()),
    (1, 10)
)

# Real-time filtered data
filtered_df = df[
    (df['Country'].isin(selected_country)) &
    (df['Transaction Type'].isin(selected_transaction_type)) &
    (df['Amount (USD)'].between(amount_range[0], amount_range[1])) &
    (df['Date of Transaction'] >= pd.to_datetime(start_date)) &
    (df['Date of Transaction'] <= pd.to_datetime(end_date)) &
    (df['Money Laundering Risk Score'].between(risk_score_range[0], risk_score_range[1]))
]

# Sidebar for Graph Selection
st.sidebar.header("Graph Options")
graph_type = st.sidebar.selectbox(
    "Select Graph Type",
    options=[
        "Bar Chart - Transaction Type Distribution",
        "Line Chart - Risk Score Over Time",
        "Scatter Plot - Amount vs. Risk Score",
        "Area Chart - Cumulative Amount Over Time",
        "Histogram - Transaction Amount Distribution"
    ]
)

# Display filtered data table interactively
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

# Display Graphs Dynamically
st.subheader("Visualization")

if graph_type == "Bar Chart - Transaction Type Distribution":
    if not filtered_df.empty:
        bar_chart = alt.Chart(filtered_df).mark_bar().encode(
            x='Transaction Type:N',
            y='count():Q',
            color='Transaction Type:N',
            tooltip=['Transaction Type', 'count()']
        )
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.write("No data available for this filter.")

elif graph_type == "Line Chart - Risk Score Over Time":
    if not filtered_df.empty:
        risk_score_time = filtered_df.groupby(pd.Grouper(key='Date of Transaction', freq='M'))['Money Laundering Risk Score'].mean().reset_index()
        line_chart = alt.Chart(risk_score_time).mark_line().encode(
            x='Date of Transaction:T',
            y='Money Laundering Risk Score:Q',
            tooltip=['Date of Transaction', 'Money Laundering Risk Score']
        )
        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.write("No data available for this filter.")

elif graph_type == "Scatter Plot - Amount vs. Risk Score":
    if not filtered_df.empty:
        scatter_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Amount (USD)',
            y='Money Laundering Risk Score',
            color='Country',
            tooltip=['Transaction ID', 'Amount (USD)', 'Money Laundering Risk Score', 'Country']
        ).interactive()
        st.altair_chart(scatter_chart, use_container_width=True)
    else:
        st.write("No data available for this filter.")

elif graph_type == "Area Chart - Cumulative Amount Over Time":
    if not filtered_df.empty:
        filtered_df['Cumulative Amount'] = filtered_df['Amount (USD)'].cumsum()
        area_chart = alt.Chart(filtered_df).mark_area(opacity=0.5).encode(
            x='Date of Transaction:T',
            y='Cumulative Amount:Q',
            tooltip=['Date of Transaction', 'Cumulative Amount']
        ).interactive()
        st.altair_chart(area_chart, use_container_width=True)
    else:
        st.write("No data available for this filter.")

elif graph_type == "Histogram - Transaction Amount Distribution":
    if not filtered_df.empty:
        hist_values = filtered_df['Amount (USD)']
        histogram = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('Amount (USD):Q', bin=alt.Bin(maxbins=30)),
            y='count():Q',
            tooltip=['Amount (USD)', 'count()']
        )
        st.altair_chart(histogram, use_container_width=True)
    else:
        st.write("No data available for this filter.")

# Download filtered data
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_data.csv',
    mime='text/csv'
)
