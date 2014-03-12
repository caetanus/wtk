#!/usr/bin/env python

from widget_wrapper import *
import ctypes
class ComboBox(widget_wrapper):
    

    style = [style.window.VSCROLL,
             style.listbox.DROPDOWN,
	     style.listbox.NOINTEGRALHEIGHT,
             style.sizer.FIT_PARENT,
             style.sizer.HEXPAND, style.sizer.VALIGN_BOTTOM,
             style.edit.TEXT_ALIGN_CENTER]
    WidgetName = "ComboBox"
    DefaultSize = [300, 300]
    dropdown_list_size = 6
    

    def __getitem__(self,index):
        d = ctypes.c_buffer(256)
        win32gui.SendMessage(self.hwnd,CB_GETLBTEXT,index,d)
        return d.value
        
    def __setitem__(self,index,data):
        win32gui.SendMessage(self.hwnd,CB_SETITEMDATA,index,string)
    
    def select(self,index):
        win32gui.SendMessage(self.hwnd, CB_SETCURSEL, index, 0 )
        win32gui.SendMessage(self.hwnd, WM_COMMAND, 0, 0)
    
    
    def move_resize(self,xy,wh,repaint = True):
        tl = win32gui.GetTextExtentPoint32(win32gui.GetWindowDC(self.hwnd),"I gonna kill my lady")[1] + 1
        widget_wrapper.move_resize(self, xy, (wh[0], wh[1]+tl*self.dropdown_list_size), repaint)
        
    def remove(self,index):
        win32gui.SendMessage(self.hwnd,CB_DELETESTRING,index,0)
        
        
    def clear(self):
        win32gui.SendMessage(self.hwnd,CB_RESETCONTENT,0,0)
        
    def append(self,data):
        win32gui.SendMessage(self.hwnd,CB_ADDSTRING,0,data)
            
    def count(self):
    #    return len(self)
            
    #def __len__(self):
        return win32gui.SendMessage(self.hwnd,CB_GETCOUNT,0,0);
    
    def get_active(self):
        return win32gui.SendMessage(self.hwnd,CB_GETCURSEL,0,0)
            

    def insert(self,string):
        win32gui.SendMessage(self.hwnd,CB_INSERTSTRING,0,string)
        
