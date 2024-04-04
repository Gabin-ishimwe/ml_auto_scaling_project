import streamlit as st
from model import load_model
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def calculate_days_difference(start_date, end_date):
    # Calculate the number of days between start and end dates
    delta = end_date - start_date
    return delta.days

def main():
    st.title("ML Auto-scaling app")
    st.write("This app leverages machine learning to forecast the number of users, CPU utilization and request count based on the selected date range. Simply choose a start and end date, and click the 'Run Model' button to see the predictions.")
    # Set the date range to December of the current year
    current_year = datetime.now().year

    # Set the minimum and maximum date values for the date inputs
    min_date = pd.to_datetime(f'2024-03-29')
    max_date = pd.to_datetime(f'2024-04-29')

    start_date = st.date_input("Select start date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Select end date", min_value=min_date, max_value=max_date, value=max_date)

     # Check if start_date is greater than end_date
    if start_date > end_date:
        st.error("Error: Start date cannot be greater than end date. Please select a valid date range.")
   
    # Example: Display the selected date range
    st.write(f"Selected Date Range: {start_date} to {end_date}")
    
    # Calculate the number of days between selected dates
    days_difference = calculate_days_difference(start_date, end_date)
    st.write(f"Number of Days Between Selected Dates: {days_difference}")
    training_data_len = 24
    if st.button("Run prediction"):
        # Load the model
        model = load_model()
        computation = model.get_prediction(start=training_data_len, end=training_data_len + days_difference)
        predictions = computation.predicted_mean
         # Generate a time series of timestamps based on the selected date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        # Create a result DataFrame with timestamps and predictions
        result_data = {
            'timestamp': date_range,
            'Prediction': predictions.round(0)
        }
        predictions['timestamp'] = date_range
        predictions['CPU Utilization (%)'] = predictions['CPU Utilization (%)'].round(2)
        predictions['number_of_users'] = predictions['number_of_users'].round(0)
        predictions['request_count'] = predictions['request_count'].round(0)
        # predictions = predictions.round(2)
        # st.dataframe(predictions.set_index('timestamp'))
        print(predictions)
        # Streamlit app

        # Plot each column separately
        st.subheader('Number of Users Over Time')
        plt.figure(figsize=(10, 5))
        plt.plot(predictions['timestamp'], predictions['number_of_users'], marker='o')
        plt.xlabel('Date')
        plt.ylabel('Number of Users')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        st.subheader('Request Count Over Time')
        plt.figure(figsize=(10, 5))
        plt.plot(predictions['timestamp'], predictions['request_count'], marker='o', color='orange')
        plt.xlabel('Date')
        plt.ylabel('Request Count')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        st.subheader('CPU Utilization Over Time')
        plt.figure(figsize=(10, 5))
        plt.plot(predictions['timestamp'], predictions['CPU Utilization (%)'], marker='o', color='green')
        plt.xlabel('Date')
        plt.ylabel('CPU Utilization (%)')
        plt.xticks(rotation=45)
        st.pyplot(plt)

if __name__ == "__main__":
    main()