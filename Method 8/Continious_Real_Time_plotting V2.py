import time
import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class DualAxisAnimationPlot:

    def __init__(self, ax):
        self.ax = ax
        self.line_x, = self.ax.plot([], [], label='X-axis')
        self.line_y, = self.ax.plot([], [], label='Y-axis')
        self.dataList_x = []
        self.dataList_y = []
        self.timestamps = []

    def init(self):
        self.line_x.set_data([], [])
        self.line_y.set_data([], [])
        return self.line_x, self.line_y

    def animate(self, i, ser):
        ser.write(b'g')
        arduinoData_string = ser.readline().decode('ascii')

        try:
            x, y = map(float, arduinoData_string.strip().split(','))
            self.dataList_x.append(x)
            self.dataList_y.append(y)
            self.timestamps.append(datetime.datetime.now())
        except Exception as e:
            print(f"Error parsing data: {e}")
            pass

        self.dataList_x = self.dataList_x[-50:]
        self.dataList_y = self.dataList_y[-50:]
        self.timestamps = self.timestamps[-50:]

        x_data, y_data = zip(*zip(self.dataList_x, self.dataList_y))

        self.line_x.set_data(self.timestamps, x_data)
        self.line_y.set_data(self.timestamps, y_data)

        self.ax.relim()
        self.ax.autoscale_view()

        return self.line_x, self.line_y

    def getPlotFormat(self):
        self.ax.set_title("Arduino Data")
        self.ax.set_xlabel("Timestamp")
        self.ax.set_ylabel("Value")
        self.ax.legend()

fig, ax = plt.subplots()
dualAxisPlot = DualAxisAnimationPlot(ax)

ser = serial.Serial("COM7", 9600)
time.sleep(2)

ani = animation.FuncAnimation(fig, dualAxisPlot.animate, init_func=dualAxisPlot.init,
                              fargs=(ser,), interval=100, blit=True)

dualAxisPlot.getPlotFormat()
plt.show()

ser.close()
