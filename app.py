import streamlit as st
from model import load_model
import pandas as pd
from datetime import datetime

def calculate_days_difference(start_date, end_date):
    # Calculate the number of days between start and end dates
    delta = end_date - start_date
    return delta.days

def main():
    st.title("Time series Auto-scaling app")
    st.write("This app leverages machine learning to forecast the number of users and request count based on a user-input text and a selected date range. Simply enter some text, choose a start and end date, and click the 'Run Model' button to see the predictions.")
    # Set the date range to December of the current year
    current_year = datetime.now().year

    # Set the minimum and maximum date values for the date inputs
    min_date = pd.to_datetime(f'2023-12-05')
    max_date = pd.to_datetime(f'2023-12-31')

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
        predictions = predictions.round(0)
        st.dataframe(predictions.set_index('timestamp'))
        print(predictions)

if __name__ == "__main__":
    main()