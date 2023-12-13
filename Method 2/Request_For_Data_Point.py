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

userInput = input('Initiate Data Stream? (y/n)\n')

if userInput.lower() == 'y':
    startDataStream()

    while True:
        
        # Check if the user wants to stop the data stream
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 's':
                stopDataStream()
                print(getValues())# Get last values then break
                break
            
            print(getValues())

ser.close()