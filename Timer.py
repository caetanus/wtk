#!/usr/bin/env python
import win32gui
import win32api
import win32event
from win32con import *
import ctypes
import threading 

class Timer:
    def __init__(self,interval,callback,*args,**kw):
        global timer_event;
        self._callback = callback
        self.interval = interval
        self._timer = threading.Timer(interval,self.callback,*args,**kw)
        self._timer.start()
    
    def callback(self,*args,**kw):
        if self._callback(*args,**kw):
            del self._timer 
            self._timer = threading.Timer(self.interval,self.callback,*args,**kw)
            self._timer.start()
        
