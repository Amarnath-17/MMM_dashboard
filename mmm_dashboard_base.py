import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(page_title="Marketing Mix Modeling Dashboard", layout="wide")

# Sample data
sales_data = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'sales': [30, 40, 20, 60, 25, 20, 45, 65, 65, 70, 50, 75]
})

contribution_data = pd.DataFrame({
    'channel': ['Base Sales', 'TV', 'Print', 'Social Media', 'YouTube'],
    'value': [60, 15, 5, 10, 10]
})

roi_data = pd.DataFrame({
    'channel': ['TV', 'Print', 'Social Media', 'YouTube', 'Paid Search'],
    'spend': [30, 5, 36, 23, 15],
    'roi': [1.5, 0.5, 2.2, 1.1, 0.7]
})

drivers_data = pd.DataFrame({
    'driver': ['Base Sales', 'Offline Media', 'Online Media', 'Covid', 'Competitors', 'Price'],
    'value': [60, 15, 12, 5, -3, 5]
})

# Dashboard title
st.title("MARKETING MIX MODELLING")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Timeframe", ["2023", "2022", "2021"])
with col2:
    region = st.selectbox("Region", ["US", "EU", "APAC"])
with col3:
    brand = st.selectbox("Brand", ["ABC", "XYZ", "123"])

# KPI metrics
st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sales", "$ 25.1M", "10%")
col2.metric("Incremental Sales", "$ 6.3M", "15%")
col3.metric("Media Spends", "$ 5.1M", "-5%")
col4.metric("Media ROI", "$ 1.15", "20%")

# Sales Trend
st.header("Sales Trend")
fig_sales = px.line(sales_data, x='month', y='sales', title='Sales Trend')
st.plotly_chart(fig_sales, use_container_width=True)

# Sales Contribution
st.header("Sales Contribution")
fig_contribution = px.pie(contribution_data, values='value', names='channel', title='Sales Contribution')
st.plotly_chart(fig_contribution, use_container_width=True)

# Return on Investment
st.header("Return on Investment")
fig_roi = go.Figure()
fig_roi.add_trace(go.Bar(x=roi_data['channel'], y=roi_data['spend'], name='Spend', marker_color='blue'))
fig_roi.add_trace(go.Bar(x=roi_data['channel'], y=roi_data['roi'], name='ROI', marker_color='green', yaxis='y2'))
fig_roi.update_layout(
    title='Return on Investment',
    yaxis=dict(title='Spend'),
    yaxis2=dict(title='ROI', overlaying='y', side='right')
)
st.plotly_chart(fig_roi, use_container_width=True)

# Drivers of Sales
st.header("Drivers of Sales")
fig_drivers = px.bar(drivers_data, x='value', y='driver', orientation='h', title='Drivers of Sales')
fig_drivers.update_traces(marker_color='purple')
st.plotly_chart(fig_drivers, use_container_width=True)

# Insights
st.header("Insights")
st.write("""
- Social Media spending during seasonal periods increased sales during Christmas by 2X
- Price increase in last quarter had a negative impact
- Cost per Million impressions for Digital partnership increased by 70%
- Launch of sub-brand ABC2 during summer increased the sales by 8%
""")