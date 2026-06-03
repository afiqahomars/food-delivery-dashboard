import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Set a clean Seaborn theme for all plots
sns.set_theme(style="whitegrid")

# ----------------- DISPLAY CHARTS -----------------

### OBJECTIVE 1: Seaborn Line Chart
st.header("Objective 1: Total Tip Amount by Day of the Week")
if not filtered_df.empty:
    tip_by_day = filtered_df.groupby('order_day_of_week')['tip_amount'].sum().reset_index()
    
    # Create the figure
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    
    # Plot using Seaborn lineplot
    sns.lineplot(
        data=tip_by_day, 
        x='order_day_of_week', 
        y='tip_amount', 
        marker='o', 
        color='royalblue', 
        linewidth=2.5, 
        ax=ax1
    )
    
    ax1.set_title("Total Tips Given Across Days of the Week", fontsize=12, pad=10)
    ax1.set_xlabel('Order Day of Week', fontsize=10)
    ax1.set_ylabel('Total Tip Amount ($)', fontsize=10)
    ax1.set_xticks(tip_by_day['order_day_of_week'])
    
    st.pyplot(fig1)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# Layout columns for Objectives 2 and 3 to sit side-by-side
col1, col2 = st.columns(2)

### OBJECTIVE 2: Seaborn Bar Chart
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
        
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        
        # Plot using Seaborn barplot
        sns.barplot(
            data=cancel_counts, 
            x='prep_time_bin', 
            y='cancel_count', 
            color='coral', 
            edgecolor='black', 
            alpha=0.85, 
            ax=ax2
        )
        
        ax2.set_title("Order Cancellations by Preparation Time Bracket", fontsize=11, pad=10)
        ax2.set_xlabel('Preparation Time Bin', fontsize=10)
        ax2.set_ylabel('Number of Cancellations', fontsize=10)
        ax2.tick_params(axis='x', rotation=15)
        
        st.pyplot(fig2)
    else:
        st.warning("No data available.")

### OBJECTIVE 3: Seaborn Scatter Plot
with col2:
    st.header("Objective 3: Tips vs Final Amount Paid")
    if not filtered_df.empty:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        
        # Sample data dynamically based on filtered size to prevent overcrowding points
        sample_size = min(500, len(filtered_df))
        scatter_sample = filtered_df.sample(sample_size, random_state=42)
        
        # Plot using Seaborn scatterplot
        sns.scatterplot(
            data=scatter_sample, 
            x='final_amount_paid', 
            y='tip_amount', 
            hue='festival_or_weekend_flag',
            style='order_day_of_week',
            palette='Set1',
            alpha=0.8,
            ax=ax3
        )
        
        ax3.set_title("Relationship: Customer Spending vs Tips Given", fontsize=11, pad=10)
        ax3.set_xlabel('Final Amount Paid ($)', fontsize=10)
        ax3.set_ylabel('Tip Amount ($)', fontsize=10)
        ax3.legend(title='Legend Categories', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        
        st.pyplot(fig3)
    else:
        st.warning("No data available.")
