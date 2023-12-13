# Run the script and use the serial monitor window.

# Use the following steps to Configure a Serila communication using with the STM32:

# 1-Initiate a project using CubeMX. Select your board, Set the clock rate...
# 2-Enable a UART communication and choose the appropriate baud rate (You can select 9600 B/s).
# 3-Connect the STM32 Board and Uplad the code.
# 4-Check the Port number, and adapt the Python script according to that number.(press Windows+x then select Device manager).
# 5-Run the Python Script to monitore the data stream using the Serial monitor view in VScode tab below (Don't forget to specify the port number and set the chosen baud rate in step2).
#  
# PS: Ensure that u have already enabled a UART communication between your PC and the STM32 trought the UART2 (the one connected
# to the JTAG debugger).