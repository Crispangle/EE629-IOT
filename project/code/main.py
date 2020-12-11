# -*- coding: utf-8 -*-
#Time:2020-12-04

import matplotlib.pyplot as plt
import time
import numpy as np
from scipy import signal
from iir_filter import IIRFilter

import matplotlib.animation as animation

import webcam2rgb


class RealtimePlotWindow:

    def __init__(self, channel: str):
        # create a plot window
        self.fig, self.ax = plt.subplots()
        plt.title(f"Channel: {channel}")
        # that's our plotbuffer
        self.plotbuffer = np.zeros(500)
        # create an empty line
        self.line, = self.ax.plot(self.plotbuffer)
        # axis
        self.ax.set_ylim(0, 1)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []
        # add any initialisation code here (filters etc)
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)


    # updates the plot
    def update(self, data):
        # add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        # only keep the 500 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-500:]
        self.ringbuffer = []
        # set the new 500 points of channel 9
        self.line.set_ydata(self.plotbuffer)
        self.ax.set_ylim(0, max(self.plotbuffer)+1)
        return self.line,

    # appends data to the ringbuffer
    def addData(self, v):
        self.ringbuffer.append(v)


realtimePlotWindowWithoutFilter = RealtimePlotWindow("WithoutFilter")
realtimePlotWindowWithFilter = RealtimePlotWindow("WithFilter")
fs = 30
N = 10
fc = 5
sos = signal.butter(N, fc/(fs/2),'lowpass',output='sos')
iir = IIRFilter(sos)
cnt = 0
list_len = 10
g_list = []
#create callback method reading camera and plotting in windows
def hasData(retval, data):
    global g_list
    global cnt
    
    g = iir.filter(data[1])
    if len(g_list) < list_len:
        g_list.append(g)
    else:
        g_list.pop(0)
        g_list.append(g) 
    if (g - g_list[0]) < -40:
        g_list = []
        cnt = cnt + 1
        print(cnt)

    
    realtimePlotWindowWithFilter.addData(g)
    realtimePlotWindowWithoutFilter.addData(data[1])

        
#create instances of camera
camera = webcam2rgb.Webcam2rgb()
#start the thread and stop it when we close the plot windows
camera.start(callback = hasData, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")
plt.show()
#camera.stop()
print('finished')

