import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Correct the path to point to the dataset in the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
dataset_path = os.path.join(root_dir, 'notebooks/vehicles_us.csv')

print("Root Directory:", root_dir)
print("Dataset Path:", dataset_path)

df = pd.read_csv(dataset_path, encoding='utf-8')

# Data cleaning
# Get rid of old columns used for SDA
columns_to_remove = ['mileage_segment', 'days_listed_bin', 'car_age']
df = df.drop(columns=columns_to_remove, errors='ignore')
# price
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to numeric, setting invalid parsing as NaN
df['price'] = df['price'].fillna(0)  # Replace NaNs with 0 or another appropriate value
df['price'] = df['price'].astype('float').fillna(0)  # Replace NaNs with 0

# Making model year column look correct:
df['model_year'] = df['model_year'].astype(str).str.split('.').str[0]
df = df[df['model_year'].str.isdigit()]
df['model_year'] = df['model_year'].astype(str)

# Making all unique values in column condition more professional:
df['condition'] = df['condition'].replace('like new', 'nearly new')

# Changing cylinders column to integer:
df['cylinders'] = df['cylinders'].fillna(0).astype(int)

# Changing odometer column to integer:
df['odometer'] = df['odometer'].astype('Int64')

# changing four wheel drive column to Boolean:
df['is_4wd'] = df['is_4wd'].fillna(pd.NA).astype('boolean')

# Streamlit App Title
st.title("Vehicle Data Analysis")

# Sidebar for User Inputs
st.sidebar.header("Filters")

import streamlit as st
import pandas as pd

# Sample DataFrame setup (for testing, remove this in your actual code)
# df = pd.read_csv('vehicles_us.csv')

# Ensure columns are correctly typed
df['cylinders'] = df['cylinders'].fillna(0).astype(int)

# Model Year Filter
model_years = sorted(df['model_year'].dropna().unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Model Year", options=["All"] + model_years)

# Filter the DataFrame based on user input
filtered_df = df if selected_year == "All" else df[df['model_year'] == selected_year]

# Four-Wheel Drive Filter
four_wheel_drive_options = ["All", True, False]
selected_4wd = st.sidebar.selectbox("Select Four-Wheel Drive", options=four_wheel_drive_options)

# Filter the DataFrame based on user input
if selected_4wd != "All":
    filtered_df = filtered_df[filtered_df['is_4wd'] == selected_4wd]


# Number of Cylinders Filter
cylinder_options = sorted(df['cylinders'].dropna().unique())
selected_cylinders = st.sidebar.selectbox("Select Number of Cylinders", options=["All"] + list(cylinder_options))

# Filter the DataFrame based on number of cylinders
if selected_cylinders != "All":
    filtered_df = filtered_df[filtered_df['cylinders'] == selected_cylinders]

# Fuel option Filter
fuel_options = sorted(df['fuel'].dropna().unique())
selected_fuel = st.sidebar.selectbox("Select Fuel Type", options=["All"] + list(fuel_options))

# Filter the DataFrame based on type of fuel
if selected_fuel != "All":
    filtered_df = filtered_df[filtered_df['fuel'] == selected_fuel]

# Fuel option Filter
condition_options = sorted(df['condition'].dropna().unique())
selected_condition = st.sidebar.selectbox("Select Condition", options=["All"] + list(condition_options))

# Filter the DataFrame based on type of fuel
if selected_condition != "All":
    filtered_df = filtered_df[filtered_df['condition'] == selected_condition]

st.write(filtered_df)


st.sidebar.header("Visualizations")
# Define the options for the selectbox
plot_options = ["Average Price by Condition", "Price vs. Mileage", "Average price by Fuel type"]

# Create a selectbox for the user to choose a plot
plot_option = st.sidebar.selectbox("Choose a Plot", options=plot_options)

# Debug: Show the selected plot option
st.write(f"Selected Plot Option: {plot_option}")
if plot_option == "Average Price by Condition":
    # Plot average price by condition
    avg_price_condition = df.groupby('condition')['price'].mean().sort_values()
    fig = px.bar(avg_price_condition, x=avg_price_condition.index, y=avg_price_condition.values, labels={'x': 'Condition', 'y': 'Average Price'})
    st.plotly_chart(fig)
elif plot_option == "Price vs. Mileage":
    # Plot price vs. mileage
    fig = px.histogram(df, x='odometer', y='price', title='Price vs. Mileage')
    st.plotly_chart(fig)
elif plot_option == "Average price by Fuel type":
    # Plot average price by fuel type
    avg_price_fuel = df.groupby('fuel')['price'].mean().sort_values()
    fig = px.bar(avg_price_fuel, x=avg_price_fuel.index, y=avg_price_fuel.values, labels={'x': 'Fuel', 'y': 'Average Price'})
    st.plotly_chart(fig)
else:
    st.write("Select a valid plot option.")