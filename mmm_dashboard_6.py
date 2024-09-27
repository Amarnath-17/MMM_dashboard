import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings

# Suppress the specific RuntimeWarning
warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in scalar divide")

# Sample data based on the image
kpi_data = {
    'Sales': 25.1,
    'Incremental Sales': 6.3,
    'Media Spends': 5.1,
    'Media ROI': 1.15
}

sales_trend = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Sales (000)$': [30, 40, 60, 40, 20, 30, 40, 70, 65, 60, 50, 80]
})

sales_contribution = pd.DataFrame({
    'Channel': ['Base sales', 'TV', 'Print', 'Social Media', 'YouTube'],
    'Percentage': [50, 15, 5, 19, 11]
})

drivers_of_sales = pd.DataFrame({
    'Driver': ['Base Sales', 'Offline Media', 'Online Media', 'Covid', 'Competitors', 'Price'],
    'Impact': [50, 15, 20, 10, -8, -3]
})

roi_data = pd.DataFrame({
    'Channel': ['TV', 'Print', 'Social Media', 'YouTube', 'Paid Search'],
    'Spend': [30, 5, 36, 23, 19],
    'ROI': [1.1, 0.5, 1.7, 1.0, 0.8]
})

# Updated sample data for budget optimization
budget_data = pd.DataFrame({
    'Channel': ['TV', 'Print', 'Social Media', 'YouTube', 'Paid Search'],
    'Current Budget': [500000, 200000, 300000, 250000, 150000],
    'Optimized Budget': [550000, 180000, 350000, 275000, 145000],
    'Base ROI': [1.9, 1.1, 1.7, 1.25, 0.95],
    'Saturation Point': [700000, 300000, 450000, 400000, 250000]  # Added saturation point for each channel
})

# Define channel-specific parameters for response curves
channel_params = {
    'TV': {'a': 0.8, 'b': 5, 'c': 0.7, 'd': 0.1},
    'Print': {'a': 0.5, 'b': 3, 'c': 1.0, 'd': 0.2},
    'Social Media': {'a': 1.2, 'b': 2, 'c': 1.5, 'd': 0.3},
    'YouTube': {'a': 1.0, 'b': 4, 'c': 0.8, 'd': 0.15},
    'Paid Search': {'a': 0.9, 'b': 3, 'c': 1.2, 'd': 0.25}
}

# Function to create KPI cards
def create_kpi_card(title, value, change):
    return go.Figure(go.Indicator(
        mode="number+delta",
        value=value,
        number={'prefix': "$", "font": {"size": 30}},
        delta={'position': "bottom", 'reference': value-change, 'relative': True},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 30}}
    ))

# Function to create sales trend chart
def create_sales_trend_chart(): 
    fig = px.line(sales_trend, x='Month', y='Sales (000)$', title='Sales Trend')
    fig.update_layout(height=400)
    return fig

# Function to create sales contribution pie chart
def create_sales_contribution_chart():
    fig = px.pie(sales_contribution, values='Percentage', names='Channel', title='Sales Contribution')
    fig.update_traces(hole=.4,textposition='inside', textinfo='percent+label',insidetextorientation='horizontal')
    fig.update_layout(showlegend=False,height=400)
    return fig

# Function to create drivers of sales bar chart
def create_drivers_of_sales_chart():
    drivers_of_sales["Color"] = np.where(drivers_of_sales["Impact"]<0, 'red', 'blue')
    fig = px.bar(drivers_of_sales, y='Driver', x='Impact', orientation='h', title='Drivers of Sales')
    fig.update_traces(marker_color=drivers_of_sales["Color"])
    fig.update_layout(height=400)
    return fig

# Function to create ROI bar chart
def create_roi_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=roi_data['Channel'], y=roi_data['Spend'], name='Spend'))
    fig.add_trace(go.Scatter(x=roi_data['Channel'], y=roi_data['ROI'], mode='lines+markers', name='ROI', yaxis='y2'))
    fig.update_layout(
        title='Return On Investment',
        yaxis=dict(title='Spend (000)$'),
        yaxis2=dict(title='ROI', overlaying='y', side='right'),
        height=400
    )
    return fig

# Updated function to create response curve
def create_response_curve(channel):
    params = channel_params[channel]
    x = np.linspace(0, 10, 100)
    
    # S-shaped curve function (combination of logistic and diminishing returns)
    y = params['a'] * (1 - np.exp(-params['c'] * x)) / (1 + np.exp(-params['d'] * (x - params['b'])))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Response Curve'))
    
    # Add current spend point
    current_spend = budget_data.loc[budget_data['Channel'] == channel, 'Current Budget'].iloc[0] / 100000  # Scale down for better visualization
    current_response = params['a'] * (1 - np.exp(-params['c'] * current_spend)) / (1 + np.exp(-params['d'] * (current_spend - params['b'])))
    fig.add_trace(go.Scatter(x=[current_spend], y=[current_response], mode='markers', name='Current Spend',
                             marker=dict(size=10, color='red', symbol='star')))
    
    # Add optimal spend point
    optimal_spend = budget_data.loc[budget_data['Channel'] == channel, 'Optimized Budget'].iloc[0] / 100000  # Use optimized budget from data
    optimal_response = params['a'] * (1 - np.exp(-params['c'] * optimal_spend)) / (1 + np.exp(-params['d'] * (optimal_spend - params['b'])))
    fig.add_trace(go.Scatter(x=[optimal_spend], y=[optimal_response], mode='markers', name='Optimal Spend',
                             marker=dict(size=10, color='green', symbol='diamond')))
    
    fig.update_layout(
        title=f'{channel} Response Curve',
        xaxis_title='Spend (100k$)',
        yaxis_title='Response',
        height=400,
        showlegend=True
    )
    return fig

def calculate_response(channel, budget):
    params = channel_params[channel]
    spend = budget / 100000  # Convert to the same scale as the response curve
    response = params['a'] * (1 - np.exp(-params['c'] * spend)) / (1 + np.exp(-params['d'] * (spend - params['b'])))
    return response

def calculate_channel_roi(channel, current_budget, new_budget):
    current_response = calculate_response(channel, current_budget)
    new_response = calculate_response(channel, new_budget)
    
    current_roi = current_response / current_budget * 1000000
    new_roi = new_response / new_budget * 1000000 if new_budget != 0 else 0
    return current_roi, new_roi


# Function to create budget optimization chart
def create_budget_optimization_chart():
    fig = go.Figure()
    for budget_type in ['Current Budget', 'Optimized Budget']:
        fig.add_trace(go.Bar(
            x=budget_data['Channel'],
            y=budget_data[budget_type],
            name=budget_type
        ))
    fig.update_layout(
        title='Current vs Optimized Budget by Channel',
        barmode='group',
        yaxis_title='Budget ($)',
        height=400
    )
    return fig


# Updated function to calculate ROI based on budget changes
def calculate_roi(budget_changes):
    channel_rois = {}
    for channel, change in budget_changes.items():
        current_budget = budget_data.loc[budget_data['Channel'] == channel, 'Current Budget'].iloc[0]
        new_budget = current_budget * (1 + change/100)
        channel_rois[channel] = calculate_channel_roi(channel, new_budget)
    overall_roi = sum(channel_rois.values()) / len(channel_rois)
    return channel_rois, overall_roi

# Function to reset budgets
def reset_budgets():
    for channel in budget_data['Channel']:
        st.session_state.budget_changes[channel] = 0

# Main app
def main():
    st.set_page_config(layout="wide")
    st.title("Media Mix Modeling Dashboard")
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox("Timeframe", ["2023", "2022", "2021"])
    with col2:
        region = st.selectbox("Region", ["US", "EU", "APAC"])
    with col3:
        brand = st.selectbox("Brand", ["ABC", "XYZ", "123"])

    # Initialize session state for budget changes if not already done
    if 'budget_changes' not in st.session_state:
        st.session_state.budget_changes = {channel: 0 for channel in budget_data['Channel']}

    # Initialize a flag for reset button
    if 'reset_clicked' not in st.session_state:
        st.session_state.reset_clicked = False

    tab1, tab2 = st.tabs(["KPIs", "Optimizer and Simulator"])        

    with tab1:
        #st.header("Key Performance Indicators")
        st.header("Key Metrics")

        col1, col2, col3, col4 = st.columns(4)
        #with col1:
        #    st.plotly_chart(create_kpi_card("Sales", kpi_data['Sales'], 2.3), use_container_width=True)
        #with col2:
        #    st.plotly_chart(create_kpi_card("Incremental Sales", kpi_data['Incremental Sales'], 0.7), use_container_width=True)
        #with col3:
        #    st.plotly_chart(create_kpi_card("Media Spends", kpi_data['Media Spends'], -0.4), use_container_width=True)
        #with col4:
        #    st.plotly_chart(create_kpi_card("Media ROI", kpi_data['Media ROI'], 0.19), use_container_width=True)

        col1.metric("Sales", "$ 25.1M", "10.2%")
        col2.metric("Incremental Sales", "$ 6.3M", "15.6%")
        col3.metric("Media Spends", "$ 5.1M", "-5.1%")
        col4.metric("Media ROI", "$ 1.15", "8.5%")    

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_sales_trend_chart(), use_container_width=True)
            st.plotly_chart(create_drivers_of_sales_chart(), use_container_width=True)
        with col2:
            st.plotly_chart(create_sales_contribution_chart(), use_container_width=True)
            st.plotly_chart(create_roi_chart(), use_container_width=True)

        st.subheader("Insights")
        st.write("* Social Media spending during seasonal periods increased sales during Christmas by 2X")
        st.write("* Price increase in last quarter had a negative impact")
        st.write("* Cost per Million impressions for Digital partnership increased by 70%")
        st.write("* Launch of sub-brand ABC2 during summer increased the sales by 8%")

    with tab2:
        st.header("Optimizer and Simulator")
        col1, col2 = st.columns(2)
        with col1:
            channel = st.selectbox("Select Channel", list(channel_params.keys()))
            st.plotly_chart(create_response_curve(channel), use_container_width=True)

        with col2:
            st.subheader("Budget Optimization")
            st.plotly_chart(create_budget_optimization_chart(), use_container_width=True)

        # Budget Simulator Section
        st.subheader("Budget Simulator")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("Adjust budget for each channel (up to ±20%):")
        with col2:
            if st.button("Reset Budgets"):
                for channel in budget_data['Channel']:
                    st.session_state.budget_changes[channel] = 0
                st.rerun()
        
        total_current_budget = sum(budget_data['Current Budget'])
        total_new_budget = 0
        total_current_roi = 0
        total_new_roi = 0
        # total_new_roi = total_current_roi + total_new_budget
        for channel in budget_data['Channel']:
            current_budget = budget_data.loc[budget_data['Channel'] == channel, 'Current Budget'].iloc[0]
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                budget_change = st.slider(f"{channel} Budget Change (%)", 
                                          min_value=-20, max_value=20, 
                                          value=st.session_state.budget_changes[channel],
                                          key=f"slider_{channel}")
                st.session_state.budget_changes[channel] = budget_change
            
            new_budget = current_budget * (1 + budget_change/100)
            
            with col2:
                st.write(f"Current: ${current_budget:,.0f}")
                st.write(f"Simulated: ${new_budget:,.0f}")
            
            current_roi, new_roi = calculate_channel_roi(channel, current_budget, new_budget)
            
            with col3:
                st.write(f"Current ROI: {current_roi:.2f}")
            
            with col4:
                st.write(f"New ROI: {new_roi:.2f}")
            
            total_new_budget += new_budget
            total_current_roi += current_roi
            total_new_roi += new_roi
        
        st.subheader("Overall Impact")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Budget", f"${total_new_budget:,.0f}", 
                      f"{((total_new_budget - total_current_budget) / total_current_budget) * 100:.1f}%")
        with col2:
            overall_roi_change = ((total_new_roi - total_current_roi) / total_current_roi) * 100 if total_current_roi != 0 else 0
            st.metric("Overall ROI", f"{total_new_roi / len(budget_data):.2f}", f"{overall_roi_change:+.1f}%")        
        
        
        

if __name__ == "__main__":
    main()