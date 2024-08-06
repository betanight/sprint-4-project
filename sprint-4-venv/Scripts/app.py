import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Correct the path to point to the dataset in the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
dataset_path = os.path.join(root_dir, 'notebooks/vehicles_us.csv')

print("Root Directory:", root_dir)
print("Dataset Path:", dataset_path)

df = pd.read_csv(dataset_path)

# Data cleaning
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

# Display the filtered data
st.write(f"Displaying data for model year {selected_year} and four-wheel drive status {selected_4wd}:")
st.write(filtered_df)

# Example Plot
st.sidebar.header("Visualizations")
plot_option = st.sidebar.selectbox("Choose a Plot", ["Average Price by Condition", "Price vs. Mileage"])

if plot_option == "Average Price by Condition":
    # Plot average price by condition
    avg_price_condition = df.groupby('condition')['price'].mean().sort_values()
    fig = px.bar(avg_price_condition, x=avg_price_condition.index, y=avg_price_condition.values, labels={'x': 'Condition', 'y': 'Average Price'})
    st.plotly_chart(fig)
elif plot_option == "Price vs. Mileage":
    # Plot price vs. mileage
    fig = px.scatter(df, x='odometer', y='price', title='Price vs. Mileage')
    st.plotly_chart(fig)