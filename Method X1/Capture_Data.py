# This script is a mature version where data collection is triggered when the user presses the space bar.
# This version ensures a parametrable window length and seamless data retrieval (regardless of the board in use).       
# In this version, I have included measurements from the gyroscope, so data has the following format (ax, ay, az, gx, gy, gz).
# All data collected using this script are from real-world examples. 
# I have added a sample number line to plot data against the sample number instead of time.


import os 
import serial
import time 
import csv 
import keyboard  # Import the keyboard library. Help recognize the button being pressed.

import serial.tools.list_ports

def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports

def findBoard():
    portsFound = get_ports()
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0, numConnection):
        port = portsFound[i]
        strPort = str(port)
        
        if ('Arduino' in strPort) or ('STMicroelectronics' in strPort): 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])  # Extract Port Number
            Board = (splitPort[2])

    return (commPort,Board)
 



connectPort,Board = findBoard()

if connectPort != 'None':
    ser = serial.Serial(connectPort, baudrate = 115200, timeout=1)
    print(f'Your {Board} Board is Connected to ' + connectPort)
else:
    print('Please connect your Board !')

# Ensure the "Dataset_CSVs" folder exists or create it
script_dir = os.path.dirname(os.path.realpath(__file__))
datasets_folder = os.path.join(script_dir, "Dataset_CSVs")
# Create the "Dataset_CSVs" folder if it doesn't exist
os.makedirs(datasets_folder, exist_ok=True)

# Get user input for the CSV file name
file_name = input("Enter a name for the CSV file (without extension): ")

# Create the full path for the CSV file
file_path = os.path.join(datasets_folder, f"{file_name}.csv")

# Open the CSV file for writing
with open(file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write a header to the CSV file
    csv_writer.writerow(["Timestamp (Unix)","Sample Nunmber", "ax", "ay", "az","gx", "gy", "gz"])

    try:
        print("Press the spacebar to start data capture...")
        keyboard.wait("space")  # Wait for the spacebar to be pressed

        start_time = time.time()
        sample_num = 0 # sample number 
        while time.time() - start_time <= 5:  # Capture data for 5 seconds
            sample_num += 1
            if ser.in_waiting > 0: 
                values = ser.readline().decode('ascii',errors='replace').strip().split(',')
                current_time = time.time()
                milliseconds = int((current_time % 1) * 1000)
                formatted_timestamp = time.strftime('%Y-%m-%d %H:%M:%S') + f'.{milliseconds:03d}'  # Format with milliseconds
                csv_writer.writerow([formatted_timestamp]+[sample_num]+ values)

    except KeyboardInterrupt:
        print("Data capture interrupted.")
    finally:
        # Close the serial connection
        ser.close()

print(f"Data captured and saved to '{file_path}'.")
