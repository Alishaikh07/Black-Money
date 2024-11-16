import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('Big_Black_Money_Dataset.csv')

# Title and Introduction
st.title("Big Black Money Insights")
st.write("An interactive dashboard to explore transactions, risk scores, and key insights.")

# Sidebar for Filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Originating Country", df['Country'].unique())
selected_transaction_type = st.sidebar.selectbox("Select Transaction Type", df['Transaction Type'].unique())
amount_range = st.sidebar.slider("Select Transaction Amount Range (USD)", 
                                  int(df['Amount (USD)'].min()), 
                                  int(df['Amount (USD)'].max()), 
                                  (10000, 1000000))

# Filter data based on selections
filtered_df = df[(df['Country'] == selected_country) &
                 (df['Transaction Type'] == selected_transaction_type) &
                 (df['Amount (USD)'].between(amount_range[0], amount_range[1]))]

# 1. Transaction Volume by Country
st.subheader("Transaction Volume by Country")
transaction_volume = df.groupby('Country')['Amount (USD)'].sum().reset_index()
st.bar_chart(transaction_volume.set_index('Country')['Amount (USD)'])

# 2. Risk Score Distribution
st.subheader("Risk Score Distribution")
st.write("Histogram of money laundering risk scores.")
# Using pandas to calculate histogram data
risk_score_counts = df['Money Laundering Risk Score'].value_counts().sort_index()
st.bar_chart(risk_score_counts)


# 3. Transaction Amount by Type
st.subheader("Transaction Amount by Type")
transaction_amount_type = df.groupby('Transaction Type')['Amount (USD)'].sum().reset_index()
st.bar_chart(transaction_amount_type.set_index('Transaction Type')['Amount (USD)'])

# 4. Shell Companies Involved
st.subheader("Shell Companies Involved by Industry")
shell_companies = df.groupby('Industry')['Shell Companies Involved'].sum().reset_index()
st.bar_chart(shell_companies.set_index('Industry')['Shell Companies Involved'])

# 5. Top Financial Institutions
st.subheader("Top Financial Institutions by Transaction Volume")
top_institutions = df.groupby('Financial Institution')['Amount (USD)'].sum().reset_index()
top_institutions = top_institutions.sort_values(by='Amount (USD)', ascending=False).head(10)
st.bar_chart(top_institutions.set_index('Financial Institution')['Amount (USD)'])

# 6. Risk Score Over Time
st.subheader("Risk Score Over Time")
df['Date of Transaction'] = pd.to_datetime(df['Date of Transaction'])
risk_score_time = df.groupby(pd.Grouper(key='Date of Transaction', freq='M'))['Money Laundering Risk Score'].mean().reset_index()
st.line_chart(risk_score_time.set_index('Date of Transaction')['Money Laundering Risk Score'])

# 7. High-Risk Transactions
st.subheader("High-Risk Transactions (Risk Score > 7)")
high_risk_transactions = df[df['Money Laundering Risk Score'] > 7]
st.write(high_risk_transactions[['Transaction ID', 'Country', 'Amount (USD)', 'Money Laundering Risk Score']])

# 8. Transactions by Tax Haven Countries
st.subheader("Transactions by Tax Haven Countries")
tax_haven_transactions = df.groupby('Tax Haven Country')['Amount (USD)'].sum().reset_index()
st.bar_chart(tax_haven_transactions.set_index('Tax Haven Country')['Amount (USD)'])

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_df)
