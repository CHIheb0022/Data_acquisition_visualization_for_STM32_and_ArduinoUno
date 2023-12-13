
import serial
import time

ser = serial.Serial('COM7', baudrate=9600, timeout=1)


def stopDataStream():
    ser.write(b's')
    print("Data stream stopped.")

def getValues():
    return ser.readline().decode('ascii')

data_stream_active = True

try:
    start_time = time.time()

    while data_stream_active:
        current_time = time.time()
        
        ser.write(b'g')
        
        if current_time - start_time >= 5:  # Capture data for 5 seconds
            stopDataStream()
            data_stream_active = False
            break

        if ser.in_waiting > 0:
            print(getValues())

except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")


# In the next version consider trigering the sarting time using a button 
# The sate of the button will be sent over uart abd retrived here and the time 
# The button change it's sate we lunch the plotting.