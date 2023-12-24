
import os
import serial
import time
import csv
import serial.tools.list_ports

def get_ports():

    ports = serial.tools.list_ports.comports() 
    return ports

    # This ports variable is a list of the available COM port.

def findSTM32():
    
    portsFound = get_ports()
    
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = portsFound[i]
        strPort = str(port)
        
        if 'STMicroelectronics' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0]) #Extract Port Number

    return commPort

connectPort = findSTM32()

if connectPort != 'None':
    ser = serial.Serial(connectPort,baudrate = 9600, timeout=1)
    print('Your STM32 Board is Connected to ' + connectPort)
else:
    print('Please connect your STM32 Board !')


# Function to start the data stream
def startDataStream():
    ser.write(b'g')
    print("Data stream initiated. Press 's' to stop.")

# Function to stop the data stream
def stopDataStream():
    ser.write(b's')
    print("Data stream stopped.")

# Function to get values from the serial port
def getValues():
    return ser.readline().decode('ascii')


# Ensure the "Dataset_CSVs" folder exists or create it

# Get the current script's directory
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

    userInput = input('Initiate Data Stream? (y/n)\n') 

    if userInput.lower() == 'y': 
        #Launch the stream and Trigger the chrono (timestamp).
        startDataStream()
    else:
        os.remove(file_path)
        print("Run the script ones you are ready\n")  

    try:
        start_time = time.time()

        # Write a header to the CSV file
        csv_writer.writerow(["Timestamp (Unix)", "ax", "ay", "az"])

        while True:
            current_time = time.time()
            if current_time - start_time >= 5:  # Capture data for 5 seconds
                stopDataStream()
                print(f"Data captured and saved to '{file_path}'.")
                break

            if ser.in_waiting > 0:
                values = getValues().strip().split(',')
                milliseconds = int((current_time % 1) * 1000)
                formatted_timestamp = time.strftime('%Y-%m-%d %H:%M:%S') + f'.{milliseconds:03d}'  # Format with milliseconds
                csv_writer.writerow([formatted_timestamp] + values)

    except KeyboardInterrupt:
        print("Data capture interrupted.")

# Close the serial connection
ser.close()