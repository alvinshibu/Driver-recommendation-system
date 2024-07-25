import streamlit as st
import pandas as pd
from datetime import datetime

# Load the dataset from a specified file path
@st.cache_data
def load_data():
    file_path = 'driver_personal_assistance_dataset.csv'
    df = pd.read_csv(file_path)
    df['availability_start_time'] = pd.to_datetime(df['availability_start_time'], format='%H:%M:%S').dt.time
    df['availability_end_time'] = pd.to_datetime(df['availability_end_time'], format='%H:%M:%S').dt.time
    return df

def find_suitable_driver(df, task_type, availability_start_time):
    # Convert availability_start_time to datetime for comparison
    availability_start_time = datetime.strptime(availability_start_time, '%H:%M:%S').time()

    # Filter the dataframe based on task_type and availability_start_time
    suitable_drivers = df[
        (df['task_type'] == task_type) &
        (df['availability_start_time'] <= availability_start_time) &
        (df['availability_end_time'] >= availability_start_time)
    ]

    return suitable_drivers[['driver_id', 'availability_start_time', 'availability_end_time', 'day_off', 'task_type']]

# Main app
st.title('Driver Assistance Recommendation System')

# Load the data
df = load_data()

# User inputs
task_type_input = st.selectbox('Select Task Type', df['task_type'].unique())
availability_start_time_input = st.text_input('Enter Availability Start Time (HH:MM:SS)', '09:00:00')

if st.button('Find Suitable Driver'):
    suitable_drivers = find_suitable_driver(df, task_type_input, availability_start_time_input)
    if suitable_drivers.empty:
        st.write('No suitable drivers found.')
    else:
        st.write('Suitable Drivers:', suitable_drivers)
