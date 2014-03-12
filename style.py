#!/usr/bin/env python
import win32con
import win32gui

class window:
    BORDER =  "WS_BORDER"
    CLIENT_EDGE =  "WS_EX_CLIENTEDGE"
    STATIC_EDGE =  "WS_EX_STATIC_EDGE"
    TOOLWINDOW =  "WS_EX_TOOLWINDOW"
    SINGLE = "WS_SINGLE"
    OVERLAPPEDWINDOW =  "WS_OVERLAPPEDWINDOW"
    TABSTOP =  "WS_TABSTOP"
    VSCROLL =  "WS_VSCROLL"
    HSCROLL =  "WS_HSCROLL"
    TOPMOST =  "WS_EX_TOPMOST"
    MINIMIZEBOX = "WS_MINIMIZEBOX"
    SYSMENU = "WS_SYSMENU"
   
class edit:
    MULTILINE =  "ES_MULTILINE"
    NUMBER =  "ES_NUMBER"
    READONLY =  "ES_READONLY"
    UPPERCASE =  "ES_UPPERCASE"
    PASSWORD =  "ES_PASSWORD"
    LOWERCASE =  "ES_LOWERCASE"
    AUTO_HSCROLL =  "ES_AUTOHSCROLL"
    AUTO_VSCROLL =  "ES_AUTOVSCROLL"
    TEXT_ALIGN_CENTER = "ES_CENTER"
    TEXT_ALIGN_LEFT =  "ES_LEFT"
    TEXT_ALIGN_RIGHT =  "ES_RIGHT"
    WANT_RETURN =  "ES_WANTRETURN"
        
class listbox:
    COMBOBOX = "LBS_COMBOBOX"
    DROPDOWN = "CBS_DROPDOWN"
    DROPDOWNLIST = "CBS_DROPDOWNLIST"
    SIMPLE = "CBS_SIMPLE"
    HASSTRING = "CBS_HASSTRING"
    NOINTEGRALHEIGHT = "CBS_NOINTEGRALHEIGHT"
    OWNERDRAWVARIABLE = "CBS_OWNERDRAWVARIABLE"

class static:
    ETCHEDFRAME = "SS_ETCHEDFRAME"
    ETCHEDHORZ =  "SS_ETCHEDHORZ"
    ETCHEDVERT = "SS_ETCHEDVERT"
    GRAYFRAME = "SS_GRAYFRAME"
    GRAYRECT = "SS_GRAYRECT"
    ICON = "SS_ICON"
    LEFT = "SS_LEFT"
    LEFTNOWORDWRAP = "SS_LEFTNOWORDWRAP"
    NOPREFIX  = "SS_NOPREFIX"
    NOTIFY = "SS_NOTIFY"
    OWNERDRAW = "SS_OWNERDRAW"
    PATHELLIPSIS = "SS_PATHELLIPSIS"
    REALSIZEIMAGE = "SS_REALSIZEIMAGE"
    RIGHT = "SS_RIGHT"
    RIGHTJUST = "SS_RIGHTJUST"
    SIMPLE = "SS_SIMPLE"
    SUNKEN = "SS_SUNKEN"
    TYPEMASK = "SS_TYPEMASK"
    USERITEM = "SS_USERITEM"
    WHITEFRAME = "SS_WHITEFRAME"
    WHITERECT = "SS_WHITERECT"
    WORDELLIPSIS = "SS_WORDELLIPSIS"
    BITMAP = "SS_BITMAP"
    BLACKFRAME =  "SS_BLACKFRAME"
    BLACKRECT  =  "SS_BLACKRECT"
    CENTER   = "SS_CENTER"
    CENTERIMAGE =   "SS_CENTERIMAGE"
    ELLIPSISMASK =  "SS_ELLIPSISMASK"
    ENDELLIPSIS  =  "SS_ENDELLIPSIS"
    ENHMETAFILE  =  "SS_ENHMETAFILE"

class button:
    PUSHBUTTON = "BS_PUSHBUTTON"
    
class sizer:
    VEXPAND =  1
    HEXPAND =  2
    HALIGN_LEFT =  4
    VALIGN_TOP =  8
    HALIGN_CENTER =  16
    VALIGN_MIDDLE =  32
    VALIGN_BOTTOM =  64
    FIT_TO_PARENT =  128
    FIT_PARENT =  256
    HALIGN_RIGHT =  512



class Style:
    _style = []
    def __init__(self,parent):
        self.parent = parent
        
    def add(self,cls,style=None):
        if type(cls) == str:
            #finding class
            for i in (window,edit,listbox,static,button):
                for j in dir(i):
                    if getattr(i,j) == cls:
                        style = cls
                        cls = i
                        break
            
        elif type(cls) == int:
            for i in dir(sizer):
                if cls == getattr(sizer,i):
                    style = cls
                    cls = sizer
                    break
                
        assert(style)
                
        self._style.append((cls,style))
        if cls in (window,edit,listbox,static,button):
            if "hwnd" in dir(self.parent):
                if "_EX_" in style:
                    win32gui.SetWindowLong(self.parent.hwnd, GWL_EXSTYLE, 
                                           getattr(win32con,style))
                else:
                    win32gui.SetWindowLong( self.parent.hwnd, GWL_STYLE,
                                           getattr(win32con,style))
            else:
                if "_EX_" in style:
                    self.parent._startup_ex_style |= getattr(win32con,style)
                else:
                    self.parent._startup_style = (self.parent._startup_style | getattr(win32con,style))
                
    def remove(self,cls,style):
        
        try:
            del self._style[self._style.index((cls,style))]
            if cls in (window,edit,listbox,static,button):
                if "_EX_" in style:
                    style = win32gui.GetWindowLong(self.parent.hwnd,
                                                   GWL_EXSTYLE)
                    slong = getattr(win32con,style)
                    win32gui.SetWindowLong(self.parent.hwnd, GWL_EXSTYLE,
                                               style ^ slong)
                else:
                    style = win32gui.GetWindowLong(self.parent.hwnd,
                                                   GWL_STYLE)
                    slong = getattr(win32con,style)
                    win32gui.SetWindowLong(self.parent.hwnd, GWL_STYLE,
                                           style ^ slong)
        except ValueError, e:
            raise ValueError, "Style not setted."


