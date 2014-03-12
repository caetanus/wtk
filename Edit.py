#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from widget_wrapper import *

class Edit(widget_wrapper):
    style = [style.edit.AUTO_HSCROLL, style.window.BORDER, style.window.CLIENT_EDGE,
             style.sizer.FIT_PARENT, style.sizer.HALIGN_CENTER, style.sizer.VALIGN_MIDDLE, style.edit.TEXT_ALIGN_CENTER]
    WidgetName = "EDIT"
    DefaultSize = [300, -1]
    def init(self):
        if self.DefaultSize[1] == -1:
            self.DefaultSize[1] = win32gui.GetTextExtentPoint32(win32gui.GetWindowDC(self.hwnd),"Ky")[1] + 2
        
        self.resize(self.DefaultSize)
        print win32gui.GetTextExtentPoint32(win32gui.GetWindowDC(self.hwnd),win32gui.GetWindowText(self.hwnd))