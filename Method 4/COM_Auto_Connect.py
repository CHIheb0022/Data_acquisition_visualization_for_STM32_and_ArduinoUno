import serial.tools.list_ports

def get_ports():

    ports = serial.tools.list_ports.comports() 
    return ports
    
    # This ports variable is a list of the available COM port in the following foramt : 
    # COM# - Connected board/Device (COM#)
    # Here are some examples:
    # COM7 - STMicroelectronics STlink Virtual com Port (COM7)
    # COM4 - Arduino uno (COM4)

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
    print('Connection Issue!')

print('DONE')