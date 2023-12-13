# Use this script and you can monitor the data being displayed in the Terminal. 

# 1-Initiate a project using CubeMX.
# 2-Enable a UART communication.
# 3-Connect the STM32 Board and Uplad the code.
# 4-Check the Port number, and adapt the Python script according to that number.(press Windows+x then select Device manager).
# 5-Run the Python Script to monitore the data stream (in the console).
#  
# PS: Ensure that u have already enabled a UART communication between your PC and the STM32 trought the UART2 (the one connected
# to the JTAG debugger).

import serial
import time
import msvcrt # kbhit from the msvcrt module (which is Windows-specific). It allows you to check if a key has been pressed without blocking the execution. 
import threading


ser = serial.Serial('COM7', baudrate=9600, timeout=1)
time.sleep(1)

def startDataStream():
    ser.write(b'g')
    print("Data stream initiated. Press 's' to stop.")

def stopDataStream():
    ser.write(b's')
    print("Data stream stopped.")

def getValues():
    return ser.readline().decode('ascii')

def dataStreamThread():
    while data_stream_active:
        print(getValues())

data_stream_active = False 
# Thread module ensure mutuel exlusion acces between main process and thread dataStreamThread() over the boolean variable.

while True:
    userInput = input('Initiate Data Stream? (y/n)\n')
    
    if userInput.lower() == 'y' and not data_stream_active:
        startDataStream()
        data_stream_active = True

        # Start the data stream thread
        stream_thread = threading.Thread(target=dataStreamThread)
        stream_thread.start()

        # Keep waiting for 's' key to stop the data stream
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                
                if key == 's' and data_stream_active:
                    stopDataStream()
                    data_stream_active = False
                    break
    else:
        break  # Exit the loop if 'n' is entered

# I have concluded that the Python script is the key for a smooth commuinication.
# Where we can specify sart and stop points for streaming and just let the STM32
# stream contiounsly. I think we can ignore the development of the C code to adapt 
# a Specific scenario Beacause sending data that is not received here it's not a big issues.
# We specify when we want to cosider the transmitted data using the script. So we play on 
# the parameters of the python script.  