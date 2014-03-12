#!/usr/bin/env python

from widget_wrapper import *
import ctypes
class Label(widget_wrapper):
    #!/usr/bin/env python
# -*- encoding: utf-8 -*-
    sel = False;
    style = [style.static.CENTER,  style.sizer.FIT_PARENT, style.sizer.HALIGN_CENTER, style.sizer.VALIGN_MIDDLE]
    WidgetName = "Static"
    DefaultSize = [-1, -1]
    _focus_handle = []
    _text_color = 0x000000
    _text_brush = None
    #debug_events = True
    def init(self):

        win32gui.SendMessage(self.hwnd,EM_SETBKGNDCOLOR,0,win32gui.GetSysColorBrush(win32con.COLOR_3DFACE))
        if self.DefaultSize[1] == -1:
            self.DefaultSize[1] = win32gui.GetTextExtentPoint32(win32gui.GetWindowDC(self.hwnd),win32gui.GetWindowText(self.hwnd))[1] + 2
        
        self.resize(self.DefaultSize)
        self.connect(WM_PAINT,self.on_paint)
    def set_color(self,color):
        self._text_color = color
        win32gui.InvalidateRect(self.hwnd, self.get_client_rect(),True)
        win32gui.UpdateWindow(self.hwnd)
    
    def on_paint(self,hwnd,wParam,lParam):
        win32gui.SetTextColor(wParam,self._text_color)
    
