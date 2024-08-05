import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Correct the path to point to the dataset in the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
dataset_path = os.path.join(root_dir, 'vehicles_us.csv')

print("Root Directory:", root_dir)
print("Dataset Path:", dataset_path)

df = pd.read_csv(dataset_path)

# Streamlit App Title
st.title("Vehicle Data Analysis")

# Sidebar for User Inputs
st.sidebar.header("Filters")

# Add filters for the app (example filters)
model_years = sorted(df['model_year'].dropna().unique().astype('int64'), reverse=True)
selected_year = st.sidebar.selectbox("Select Model Year", options=model_years)

# Filter the DataFrame based on user input
filtered_df = df[df['model_year'] == selected_year]

# Display the filtered data
st.write(f"Displaying data for model year {selected_year}:")
st.write(filtered_df)

# Add filter for four-wheel drive
# Filter options for boolean values
four_wheel_drive_options = [True, False]

# Add filter for four-wheel drive
selected_4wd = st.sidebar.selectbox("Select Four-Wheel Drive", options=["All"] + four_wheel_drive_options)

# Filter the DataFrame based on user input
if selected_4wd != "All":
    filtered_df = filtered_df[filtered_df['is_4wd'] == selected_4wd]



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