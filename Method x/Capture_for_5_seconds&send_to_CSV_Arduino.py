import os
import serial
import time
import csv

import serial.tools.list_ports

def get_ports():

    ports = serial.tools.list_ports.comports() 
    return ports

    # This ports variable is a list of the available COM port.

def findArduino():
    
    portsFound = get_ports()
    
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = portsFound[i]
        strPort = str(port)
        
        if 'Arduino' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0]) #Extract Port Number

    return commPort

connectPort = findArduino()

if connectPort != 'None':
    ser = serial.Serial(connectPort,baudrate = 115200, timeout=1)
    print('Your Arduino Board is Connected to ' + connectPort)
else:
    print('Please connect your Arduino Board !')

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
    csv_writer.writerow(["Timestamp (Unix)", "ax", "ay", "az"])

    try:

        start_time = time.time()

        while time.time() - start_time <= 5:  # Capture data for 5 seconds
            if ser.in_waiting > 0:
                values = ser.readline().decode('ascii').strip().split(',')
                current_time = time.time()
                milliseconds = int((current_time % 1) * 1000)
                formatted_timestamp = time.strftime('%Y-%m-%d %H:%M:%S') + f'.{milliseconds:03d}'  # Format with milliseconds
                csv_writer.writerow([formatted_timestamp] + values)

    except KeyboardInterrupt:
        print("Data capture interrupted.")
    finally:
        # Close the serial connection
        ser.close()

print(f"Data captured and saved to '{file_path}'.")
