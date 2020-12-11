# -*- coding: utf-8 -*-
#Time:2020-12-04

import matplotlib.pyplot as plt
import time
import numpy as np
from scipy import signal

class IIR2Filter:
    def __init__(self, b, a):
        self._b = b
        self._a = a
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        

    def filter(self, x):
        y= (self._b[1]*self._x1+self._b[2]*self._x2) + x*self._b[0] - (self._a[1]*self._y1+self._a[2]*self._y2)
        y = y/self._a[0]
        self._y2 = self._y1
        self._y1 = y
        self._x2 = self._x1
        self._x1 = x
        return y

class IIRFilter:
    def __init__(self, sos):
        self._iir2filter = []
        self._nsec = len(sos)
        for i in range(self._nsec):
            self._iir2filter.append(IIR2Filter(sos[i,0:3],sos[i,3:6]))
        

    def filter(self, x):
        tmp = x
        for i in range(self._nsec):
            y = self._iir2filter[i].filter(tmp)
            tmp = y
        return y
