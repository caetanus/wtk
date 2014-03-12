#!/usr/bin/env python
# -*- encoding: utf-8 -*-

 
try: import winxpgui as win32gui
except: import win32gui
import win32con
import win32api
import exceptions
import win32process
import win32file
from win32con import *
import ctypes
user32 = ctypes.windll.user32
import style
import font

import sys
#print sorted([getattr(win32con,i) for i in  dir(win32con) if i.startswith('WM')])
#[0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7, 8, 8, 10, 11, 12, 13, 14, 15, 16, 17,
#18, 19, 20, 21, 22, 24, 26, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39,
#40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 57, 61, 65, 68, 70, 71, 72, 74,
#75, 78, 80, 81, 82, 83, 84, 85, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
#133, 134, 135, 136, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 256, 256,
#257, 258, 259, 260, 261, 262, 263, 264, 269, 270, 271, 271, 272, 273, 274, 275,
#276, 277, 278, 279, 287, 288, 289, 290, 291, 292, 293, 294, 306, 307, 308, 309,
#310, 311, 312, 512, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 522,
#528, 529, 530, 531, 532, 533, 534, 536, 537, 544, 545, 546, 547, 548, 549, 550,
#551, 552, 553, 560, 561, 562, 563, 564, 641, 642, 643, 644, 645, 646, 648, 656,
#657, 673, 675, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780,
#781, 782, 783, 784, 785, 786, 791, 792, 856, 863, 864, 895, 896, 911, 1024, 1024,
#1025, 1025, 1026, 1027, 1028, 1029, 1030, 1125, 1126, 32768]

#event numbers printed, I think it is a signed short int, so the events above 20k
#is freelly to use.

WM_SOCKET = (WM_USER+1)
CB_SETMINVISIBLE = 0x1701
EM_SETBKGNDCOLOR  = WM_USER + 67

def MsgBox(text,caption="",style="alert", parent = None):
    styles = {
        "alert": MB_ICONERROR,
        "warning": MB_ICONEXCLAMATION,
        "info": MB_ICONINFORMATION
    }

    assert((style in styles.keys()))
    style = styles[style]
    if parent == None:
        parent = 0
    else:
        parent = parent.hwnd 
    win32gui.MessageBox(parent,text,caption,style | MB_OK)#, win32api.MAKELANGID(LANG_NEUTRAL,SUBLANG_DEFAULT))
    

class widget:
    classname = "widget"
    type = "widget"
    border = 0
    parent = None
    child = None
    debug_events = False
    _startup_style = 0
    _startup_ex_style = 0
    _evt_name = {}
    _connect_id = 1
    
    _add_pending = []
    def __init__(self,*args,**kw):
        self._connect_dict = {}
        self.create_wclass()
        self._pre_init()
        self._register_wclass()
        
        self.init(*args,**kw)
        self._post_init()
        
    def io_add_watch(self,socket,callback):
        global WM_SOCKET
        win32file.WSAAsyncSelect(socket,self.hwnd, WM_SOCKET,
                                 win32file.FD_ACCEPT | win32file.FD_CLOSE
                                 | win32file.FD_READ)
        self._s_callback = callback
    
    def init(self,*args,**kw):
        
        raise NotImplementedError, "This is a virtual widget, can't initalize itself"
    
    def _post_init(self):
        pass
    
    def _pre_init(self):
        s = style.Style(self)
        for i in self.style:
            s.add(i)
        self.style = s
    
    def create_wclass(self):
        raise NotImplementedError, "To create a widget, you need to create a wclass method"

    def _register_wclass(self):
        global WM_SOCKET
        wproc = {}
        #creating event table, to translating when debug
        for j in [i for i in dir(win32con) if i.startswith("WM_")]:
            try:
                self._evt_name[getattr(win32con,j)] = j
                wproc[getattr(win32con,j)] = self._event_dispacher
            except:
                pass
        wproc[WM_SOCKET] = self._event_dispacher

        self.wc.lpfnWndProc = self._event_dispacher
        self.wclass = win32gui.RegisterClass(self.wc)
        del self.wc
    
    def _event_dispacher(self,hwnd,Message,lParam,hParam):
        global WM_SOCKET
        
        if Message == WM_SOCKET:
            self._s_callback()
        
        flag = False
        if Message in self._evt_name:
            evt_name = self._evt_name[Message]
        else: evt_name = Message
        
        if Message == WM_SIZE:
            self._on_resize()
        
        if Message == WM_COMMAND:
            if hParam != self.hwnd:
                win32gui.SendMessage(hParam,WM_COMMAND,0,0)
            
        if Message == WM_SHOWWINDOW and lParam == 1:
            try:
                self.add_pennding()
            except:
                pass
            
        if self.debug_events:

            print "evt: %X" % self.hwnd, evt_name, Message, lParam, hParam
        
        if Message in self._connect_dict:
            for i in self._connect_dict[Message]:
                flag = i[1](hwnd,lParam,hParam,*i[2])
                
        if not flag:
            return win32gui.DefWindowProc(hwnd,Message,lParam,hParam)
        else: return flag;
    


    def connect(self, event, callback, *args):
        if event in self._connect_dict:
            self._connect_dict[event].append([self._connect_id, callback,args])
        else:
            self._connect_dict[event] = [[self._connect_id, callback,args]]
        r = self._connect_id
        self._connect_id += 1
        return r
    
    def disconnect(self,id):
        for i in self._connect_dict.keys():
            for j in xrange(i):
                if id == i[j][0]:
                    del i[j]
                    return
    
    def fit_to_parent(self):
        if self.parent:
            psize = self.parent.get_client_size()
            plt = self.parent.get_client_rect()[:2]
            ssize = list(self.get_size())

            if (style.sizer, style.sizer.FIT_TO_PARENT) in self.style._style:
                x = self.parent.border + plt[0]
                y = self.parent.border + plt[1]
                ssize = (psize[0] - self.parent.border * 2, psize[1] - self.parent.border * 2)
            else:
                #Vertical Resizing
                if (style.sizer, style.sizer.VALIGN_MIDDLE) in self.style._style:
                    y = ((psize[1] - ssize[1]) / 2) + plt[1]
                elif (style.sizer, style.sizer.VALIGN_TOP) in self.style._style:
                    y = self.parent.border + plt[1]
                elif (style.sizer, style.sizer.VALIGN_BOTTOM) in self.style._style:
                    y = psize[1] - self.parent.border - ssize[1] + plt[1]
                elif (style.sizer, style.sizer.VEXPAND) in self.style._style:
                    y = self.parent.border + plt[1]
                    ssize[1] = psize[1] - self.parent.border * 2
                    
                #Horizontal Resizing
                if (style.sizer, style.sizer.HALIGN_CENTER) in self.style._style:
                    x = (psize[0] - ssize[0]) / 2 + plt[0]
                elif (style.sizer, style.sizer.HALIGN_LEFT) in self.style._style:
                    x = self.parent.border + plt[0]
                elif (style.sizer, style.sizer.HALIGN_RIGHT) in self.style._style:
                    x = psize[0] - self.parent.border - ssize[0] + plt[0]
                elif (style.sizer, style.sizer.HEXPAND) in self.style._style:
                    x = self.parent.border + plt[0]
                    ssize[0] = psize[0] - self.parent.border * 2
                    
            self.move_resize((x,y),ssize)
    
    def fit_to_child(self):
        if self.child:
            v, h = self.child.get_size()
            self.child.move((self.border,self.border))
            self.resize(v + self.border, h + self.border)
    
    def _on_resize(self):
        if self.child:
            self.child.fit_to_parent()
        if self.parent:
            self.parent.fit_to_child()
    
    def add_pennding(self):
        self._add_pending = list(set(self._add_pending))
        try:
            for i in self._add_pending:
                self.add(i,True)
        finally:
            self._add_pending = []
        
    
    def add(self,widget,force = False):
        self.child = widget
        widget.parent = self
        widget.fit_to_parent()
        if not win32gui.IsWindowVisible(self.hwnd) and not force:
            self._add_pending.append(widget)
            return

        if self.child:
            raise OverflowError, "não é possível adicionar mais de um widget a um widget."
            
        if widget.type == "widget":
            win32gui.SetWindowLong(widget.hwnd, GWL_STYLE, WS_CHILD)
            win32gui.SetParent(widget.hwnd,self.hwnd)

    def get_text(self):
        return win32gui.GetWindowText(self.hwnd)
    
    def set_text(self,text):
        win32gui.SetWindowText(self.hwnd,text)
    
    def get_hwnd(self):
        return self.hwnd
        
    def get_client_rect(self):
        return win32gui.GetClientRect(self.hwnd)
        
    def get_rect(self):
        return win32gui.GetWindowRect(self.hwnd)
    
    def get_size(self):
        r = self.get_rect()
        return (r[2]-r[0],r[3]-r[1])
    
    def get_client_size(self):
        return self.get_client_rect()[2:]
        
    def get_pos(self):
        return self.get_rect()[:2]
    
    def move(self,xy,repaint = True):
        self.move_resize(xy,self.get_size(),repaint)
    
    def resize(self,wh,repaint = True):
        self.move_resize(self.get_pos(),wh,repaint)
    
    def move_resize(self,xy,wh,repaint = True):
        args = list(xy) + list(wh) + [repaint]
        win32gui.MoveWindow(self.hwnd,*args)

    #def move_resize(self,rect,repaint = True):
    #    self.move_resize(self,rect[:2],(rect[2]-rect[0],rect[3]-rect[1]),repaint);
        
    def show(self,show=True):
        win32gui.ShowWindow(self.hwnd,show)
    
    def show_all(self):
        self.show()
        if self.child:
            self.child.show_all()
    
    def set_font(self,font):
        win32gui.SendMessage(self.hwnd,WM_SETFONT,font.handle)
    
    
    def close(self):
        win32gui.DestroyWindow(self.hwnd)
            