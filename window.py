from wintk import *

import ctypes
user32 = ctypes.windll.Kernel32
import sys

import time
def get_argv_0():
    cl = win32api.GetCommandLine()
    r = ''
    if cl[0] in ("'",'"'):
        for i in cl[1:]:
            if i in ("'",'"'):
                break
            r += i
    else:
        r = cl.split()[0]
    return r

class Window(widget):
    classname = "Window"
    style = [style.window.OVERLAPPEDWINDOW]
    default_size = [500,300]
    def init(self, title="teste"):
        
        self.hwnd = win32gui.CreateWindowEx(self._startup_ex_style, self.wclass,
            title, self._startup_style, CW_USEDEFAULT,
            CW_USEDEFAULT, self.default_size[0],self.default_size[1], 0, 0,
        win32api.GetModuleHandle(None), None)
        self.connect(WM_DESTROY, self.quit)
        self.set_font(font.Font())
        self.set_client_size(self.default_size)

    def __del__(self):
        self.close()
    
    def set_title(self,text):
        self.set_text(text)
    
    def get_titlebar_size(self):
        s = self.get_size()
        c = self.get_client_size()[:2]
        return (s[0] - c[0], s[1] - c[1])
        
        
    def set_client_size(self,wh):
        wh = (wh[0],wh[1] + self.get_titlebar_size()[1])
        self.resize(wh)
    
    def create_wclass(self,title="",classname="WinTK"):
        self.container = []
        wc = win32gui.WNDCLASS()
        wc.style = 0 
        wc.lpfnWndProc = { }
        wc.cbWndExtra = 0
        wc.hInstance = win32api.GetModuleHandle(None)
        icon =  win32gui.ExtractIcon(0,get_argv_0(),0)
        if icon:
            wc.hIcon = icon#win32gui.LoadIcon(0,icon)
        else:
            wc.hIcon = win32gui.LoadIcon(0,IDI_APPLICATION)
        wc.hCursor = win32gui.LoadCursor(0, IDC_ARROW)
        wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
        wc.lpszClassName = classname
        self.wc = wc
    

        
    def MsgBox(self,text,caption="",style="alert"):
        MsgBox(text,caption,style,self)

        
    def quit(self,*args):
        
        win32gui.DestroyWindow(self.hwnd)
        win32gui.PostQuitMessage(0)


