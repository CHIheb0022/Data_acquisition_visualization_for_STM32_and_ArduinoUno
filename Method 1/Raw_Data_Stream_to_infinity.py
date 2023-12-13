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

ser = serial.Serial('COM7', baudrate = 9600, timeout=1) 
# Check the Serial Port "COMX" where you have connected your STM32 board.

while 1:

    STM32Data = ser.readline().decode('ascii') # The data is received in binary format. we must decode to ascii.
    print(STM32Data)

ser.close()