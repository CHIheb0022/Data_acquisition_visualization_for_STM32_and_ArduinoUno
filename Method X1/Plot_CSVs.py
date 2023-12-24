# In this version, I have incorporated gyro data (gx, gy, gz). So I have adapted the Plotting script accordingly.
# Unlike the previous versions, this script includes a boolean function "is_valid_line()" preventing corrupted data from being plotted.
# The philosophy here is to skip the corrupted lines. Another approach that could be implemented is to get the previous line data once 
# the current line is corrupted (I will try to find the hardware issues causing those corruptions).   
# Until now, the maximum number of corruptions I have encountered is 6.
# In this version, examples with the prefix v2 present the data plotted against the sample number.
# Unlike the previous version, the current update loops over the CSV files and checks if it has an associated image; if not, the script creates the corresponding image.


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

def is_valid_line(line):
    # Check if the line has the correct number of values separated by commas
    expected_values = 8  # Adjust the number based on your data structure
    values = line.strip().split(',')
    
    if len(values) == expected_values:
        return True
    else:
        return False

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
    if file_name.endswith(".csv") and file_name.replace(".csv", ".png") not in os.listdir(dataset_folder):
        # Construct the file path
        file_path = os.path.join(Dataset_CSVs_path, file_name)

        # Read the CSV file
        i = 0 # This counter is used to monitor the number of corrupted lines in each csv file  recently added.  
        valid_lines = []
        with open(file_path, 'r') as file:
            for line in file:
                if is_valid_line(line):
                    valid_lines.append(line)
                else : i+=1

        # Create a new CSV file with only valid lines
        valid_file_path = os.path.join(Dataset_CSVs_path, f"valid_{file_name}")
        with open(valid_file_path, 'w') as valid_file:
            valid_file.writelines(valid_lines)

        # Read the valid CSV file
        data = pd.read_csv(valid_file_path)

        # Convert 'Timestamp (Unix)' to datetime object
        data['Timestamp (Unix)'] = pd.to_datetime(data['Timestamp (Unix)'])

        # Extract milliseconds part
        data['Milliseconds'] = data['Timestamp (Unix)'].dt.microsecond / 1000  # Convert microseconds to milliseconds

        # Convert datetime to numerical value for plotting
        data['Timestamp_Numerical'] = data['Timestamp (Unix)'].astype(np.int64) / 10**9  # Convert to seconds

        # Plot Acceleration
        plt.figure(figsize=(10, 8))  # Increase the figure size
        plt.subplots_adjust(hspace=0.5)  # Increase the vertical space between subplots

        # Plot Acceleration (ax, ay, az)
        plt.subplot(2, 1, 1)
        plt.plot(data['Sample Nunmber'], data['ax'], label='Ax')
        plt.plot(data['Sample Nunmber'], data['ay'], label='Ay')
        plt.plot(data['Sample Nunmber'], data['az'], label='Az')
        plt.title('Acceleration Data - ' + os.path.splitext(file_name)[0])
        plt.xlabel('Samples')
        plt.ylabel('Acceleration')
        plt.legend()

        # Plot Gyroscope (gx, gy, gz)
        plt.subplot(2, 1, 2)
        plt.plot(data['Sample Nunmber'], data['gx'], label='Gx')
        plt.plot(data['Sample Nunmber'], data['gy'], label='Gy')
        plt.plot(data['Sample Nunmber'], data['gz'], label='Gz')
        plt.title('Gyroscope Data - ' + os.path.splitext(file_name)[0])
        plt.xlabel('Samples')
        plt.ylabel('Angular Velocity')
        plt.legend()

        # Save the plot
        save_path = os.path.join(dataset_folder, file_name.replace(".csv", ".png"))
        plt.savefig(save_path)
        plt.close()
        print(os.path.splitext(file_name)[0], f"Transformed to image successfuly with {i} corrupted lines.")
        # Remove the temporary valid file
        os.remove(valid_file_path)


print("Plots saved in the 'Datasets_Fig' folder.")


