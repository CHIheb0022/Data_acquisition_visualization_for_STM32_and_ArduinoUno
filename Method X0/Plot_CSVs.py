import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def find_directory(directory_name):
    script_location = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(script_location):
        if directory_name in dirs:
            return os.path.join(root, directory_name)

# Get the current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create the path for 'Datasets_Fig'
dataset_folder = os.path.join(script_dir, 'Datasets_Fig')

# Create the "Datasets_Fig" folder if it doesn't exist
os.makedirs(dataset_folder, exist_ok=True)

# Search for Dataset_CSVs return path if exists. Raise an exception if it doesn't (to be handled when refining the code).
Dataset_CSVs_path = find_directory("Dataset_CSVs")

# Loop over all CSV files in the "Dataset_CSVs" folder
for file_name in os.listdir(Dataset_CSVs_path):
    if file_name.endswith(".csv"):
        # Construct the file path
        file_path = os.path.join(Dataset_CSVs_path, file_name)

        # Read the CSV file
        data = pd.read_csv(file_path)

        # Convert 'Timestamp (Unix)' to datetime object
        data['Timestamp (Unix)'] = pd.to_datetime(data['Timestamp (Unix)'])

        # Extract milliseconds part
        data['Milliseconds'] = data['Timestamp (Unix)'].dt.microsecond / 1000  # Convert microseconds to milliseconds

        # Convert datetime to numerical value for plotting
        data['Timestamp_Numerical'] = data['Timestamp (Unix)'].astype(np.int64) / 10**9  # Convert to seconds

        # Plot Acceleration
        plt.figure(figsize=(10, 8))  # Increase the figure size
        plt.subplots_adjust(hspace=0.5)  # Increase the vertical space between subplots
        plt.subplot(2, 1, 1)
        
        plt.plot(data['Timestamp_Numerical'], data['ax'], label='Ax')
        plt.plot(data['Timestamp_Numerical'], data['ay'], label='Ay')
        plt.plot(data['Timestamp_Numerical'], data['az'], label='Az')
        plt.title('Acceleration Data - ' + os.path.splitext(file_name)[0])
        plt.xlabel('Time (seconds)')
        plt.ylabel('Acceleration')
        plt.legend()

        # Plot Gyroscope (to be added later on)
        # plt.subplot(2, 1, 2)
        # plt.plot(data['Milliseconds'], data['Gx'], label='Gx')
        # plt.plot(data['Milliseconds'], data['Gy'], label='Gy')
        # plt.plot(data['Milliseconds'], data['Gz'], label='Gz')
        # plt.title('Gyroscope Data - ' + os.path.splitext(file_name)[0])
        # plt.xlabel('Time (Milliseconds)')
        # plt.ylabel('Angular Velocity')
        # plt.legend()

        # Save the plot
        save_path = os.path.join(dataset_folder, file_name.replace(".csv", ".png"))
        plt.savefig(save_path)
        plt.close()

print("Plots saved in the 'Datasets_Fig' folder.")
