#!/usr/bin/env python

from wintk import *


class widget_wrapper(widget):

    classname = "widget_wrapper"

    WidgetName = ""
    Width = CW_USEDEFAULT
    Height = CW_USEDEFAULT
    DefaultSize = [-1,-1]

    def __init__(self,title = ""):

        self._connect_dict = {}
        self._evt_name = {}
        self._pre_init()
        self._register_wclass()
        
        self.create_widget(title)
        self.oldWinProc = win32gui.GetWindowLong(self.hwnd, GWL_WNDPROC)
        win32gui.SetWindowLong(self.hwnd, GWL_WNDPROC,self._event_dispacher)
        self.set_font(font.Font())
        
        self.init()
        self._post_init()
        
        
    def init(self):
        pass
    
    def set_text(self,text):
        win32gui.SetWindowText(self.hwnd,text)
    
    def _post_init(self):
        if self.DefaultSize[1] == -1:
            self.DefaultSize[1] = win32gui.GetTextExtentPoint32(win32gui.GetWindowDC(self.hwnd),win32gui.GetWindowText(self.hwnd))[1] + 2
        if self.DefaultSize[0] == -1:
            self.DefaultSize[0] = win32gui.GetTextExtentPoint32(win32gui.GetWindowDC(self.hwnd),win32gui.GetWindowText(self.hwnd))[0] + 2
        
        self.resize(self.DefaultSize)

    def create_widget(self,title):
        self.hwnd = win32gui.CreateWindowEx(self._startup_ex_style,self.WidgetName,title,
                        self._startup_style,0,0, self.Width, self.Height,0,0,
                        win32api.GetModuleHandle(None), None)
        

    def _register_wclass(self):

        #creating event table, to translating when debug
        for j in [i for i in dir(win32con)]:
            try:
                self._evt_name[getattr(win32con,j)] = j
            except:
                pass

    def _event_dispacher(self,hwnd,Message,lParam,hParam):
        if Message in self._evt_name:
            evt_name = self._evt_name[Message]
        else: evt_name = Message
            
        #print evt_name,Message,self.WidgetName, self._connect_dict

        flag = None
        if self.debug_events:
            if Message in self._evt_name:
                evt_name = self._evt_name[Message]
            else: evt_name = Message
            print "evt: ", evt_name, lParam, hParam
        
        if Message == WM_COMMAND:
            if hParam != self.hwnd:
                win32gui.SendMessage(hParam,WM_COMMAND,0,0)
            
        if Message in self._connect_dict:
            
            for i in self._connect_dict[Message]:
                flag = i[1](hwnd,lParam,hParam,*i[2])
        
        if flag == None:
            return win32gui.CallWindowProc(self.oldWinProc,hwnd,Message,lParam,hParam)
        else:
            return flag;
    