﻿# -*- coding: utf-8 -*-
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
        self.fs = 30
        freqs = np.fft.fftfreq(self.plotbuffer.size,1.0/self.fs)
        self.line, = self.ax.plot(freqs,self.plotbuffer)
        # axis
        self.ax.set_ylim(0, 1)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []
        # add any initialisation code here (filters etc)
        
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1)


    # updates the plot
    def update(self, data):
        # add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        # only keep the 500 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-500:]
        #analyze spectrum
        
        plotbuffer_freq = abs(np.fft.fft(self.plotbuffer))
    
        
        self.ringbuffer = []
        # set the new 500 points of channel 9
        self.line.set_ydata(plotbuffer_freq)
        
        self.ax.set_ylim(0, max(plotbuffer_freq)+1)
        return self.line,

    # appends data to the ringbuffer
    def addData(self, v):
        self.ringbuffer.append(v)


realtimePlotWindowBlue = RealtimePlotWindow("Blue")
realtimePlotWindowGreen = RealtimePlotWindow("Green")
realtimePlotWindowRed = RealtimePlotWindow("Red")

#create callback method reading camera and plotting in windows
def hasData(retval, data):
    
    b = data[0]
    g = data[1]
    r = data[2]
   
    
    realtimePlotWindowBlue.addData(b)
    realtimePlotWindowGreen.addData(g)
    realtimePlotWindowRed.addData(r)

        
#create instances of camera
camera = webcam2rgb.Webcam2rgb()
#start the thread and stop it when we close the plot windows
camera.start(callback = hasData, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")
plt.show()
#camera.stop()
print('finished')

