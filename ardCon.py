import serial

import matplotlib.pyplot as plt
plt.ion()

ser = serial.Serial('/dev/ttyUSB0', 9600)


def serOut(ser):
    tmp = ser.read()
    a = tmp
    while(tmp != '\n'):
        tmp = ser.read()
        a += tmp
    b = a.split('\r')[0]
    b = b.split(',')
    return b[0], b[1]


class DynamicUpdate():
    # Suppose we know the x range
    min_x = 0
    max_x = 20

    def on_launch(self):
        # Set up plot
        self.figure, self.ax = plt.subplots(
            # subplot_kw=dict(projection='polar')
        )
        self.lines, = self.ax.plot([], [], '-')
        # Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        #self.ax.set_xlim(self.min_x, self.max_x)
        #self.ax.set_ylim(self.min_x, self.max_x)
        # Other stuff
        self.ax.grid()

    def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        # Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    # Example
    def __call__(self):
        import numpy as np
        import time
        self.on_launch()
        xdata = []
        ydata = []
        i = 0
        for x in np.arange(0, 100000, 1):

            x0, y0 = serOut(ser)

            if(len(x0) <= 6):
                if(y0 != '' and x0 != ''):
                    print(x0, y0)
                    xdata.append(float(x0))
                    ydata.append(float(y0))
                    self.on_running(xdata, ydata)
        return xdata, ydata

d = DynamicUpdate()
d()
