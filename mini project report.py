import streamlit as st
import pandas as pd
import plotly.express as px

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Food Delivery Analytics Dashboard")

# Title of the Dashboard
st.title("🍔 Food Delivery Analytics Interactive Dashboard")
st.markdown("---")

# Load the cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("food_delivery_analytics_cleaned.csv")

df = load_data()

# ----------------- SIDEBAR INTERACTIVITY -----------------
st.sidebar.header("Dashboard Filters")

# Filter 1: City Tier Selection
city_options = df['city_tier'].unique().tolist()
selected_cities = st.sidebar.multiselect("Select City Tier(s):", options=city_options, default=city_options)

# Filter 2: Day of Week Selection
day_options = sorted(df['order_day_of_week'].unique().tolist())
selected_days = st.sidebar.multiselect("Select Order Day(s) of Week:", options=day_options, default=day_options)

# Apply filters to the dataframe
filtered_df = df[
    (df['city_tier'].isin(selected_cities)) & 
    (df['order_day_of_week'].isin(selected_days))
]

# Set Seaborn theme
sns.set_theme(style="whitegrid")

# ----------------- DISPLAY CHARTS -----------------

### OBJECTIVE 1: Line Chart
st.header("Objective 1: Total Tip Amount by Day of the Week")
if not filtered_df.empty:
    tip_by_day = filtered_df.groupby('order_day_of_week')['tip_amount'].sum().reset_index()
    
    # Create Plotly line chart
    fig1 = px.line(
        tip_by_day, 
        x='order_day_of_week', 
        y='tip_amount', 
        markers=True,
        labels={'order_day_of_week': 'Order Day of Week', 'tip_amount': 'Total Tip Amount ($)'},
        template='whitegrid'
    )
    # Customize line color and style
    fig1.update_traces(line=dict(color='royalblue', width=2.5))
    
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# Layout columns for Objectives 2 and 3 to sit side-by-side
col1, col2 = st.columns(2)

### OBJECTIVE 2: Bar Chart
with col1:
    st.header("Objective 2: Cancelled Orders vs Prep Time")
    if not filtered_df.empty:
        bins = [0, 10, 20, 30, 40, 50, 60]
        labels = ['0-10 min', '10-20 min', '20-30 min', '30-40 min', '40-50 min', '50-60 min']
        
        # Avoid SettingWithCopyWarning by creating an explicit copy
        sub_df = filtered_df.copy()
        sub_df['prep_time_bin'] = pd.cut(sub_df['preparation_time_minutes'], bins=bins, labels=labels)
        
        cancelled_df = sub_df[sub_df['cancellation_flag'] == True]
        cancel_counts = cancelled_df['prep_time_bin'].value_counts().reindex(labels).reset_index()
        cancel_counts.columns = ['prep_time_bin', 'cancel_count']
        
        # Create Plotly bar chart
        fig2 = px.bar(
            cancel_counts,
            x='prep_time_bin',
            y='cancel_count',
            labels={'prep_time_bin': 'Preparation Time Bin', 'cancel_count': 'Number of Cancellations'},
            template='whitegrid'
        )
        # Match your original coral palette styling
        fig2.update_traces(marker_color='coral', marker_line_color='black', marker_line_width=1, opacity=0.85)
        
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data available.")
### OBJECTIVE 3: Scatter Plot
with col2:
    st.header("Objective 3: Tips vs Final Amount Paid")
    if not filtered_df.empty:
        # Sample data dynamically based on filtered size to prevent overcrowding points
        sample_size = min(500, len(filtered_df))
        scatter_sample = filtered_df.sample(sample_size, random_state=42)
        
        # Create Plotly scatter plot
        fig3 = px.scatter(
            scatter_sample, 
            x='final_amount_paid', 
            y='tip_amount', 
            color='festival_or_weekend_flag',
            symbol='order_day_of_week',
            labels={
                'final_amount_paid': 'Final Amount Paid ($)', 
                'tip_amount': 'Tip Amount ($)',
                'festival_or_weekend_flag': 'Festival/Weekend',
                'order_day_of_week': 'Day of Week'
            },
            opacity=0.8,
            color_discrete_sequence=px.colors.qualitative.Set1,  # Matches Seaborn's Set1
            template='whitegrid'
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No data available.")
