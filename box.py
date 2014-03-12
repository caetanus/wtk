#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wintk import *
#box coded by chico xavier thanks to akamaru for your help


    
    
class hbox:
    classname = "vbox"
    type = "box"
    border = 0
    parent = None
    childs = []
    rect = (0,0,0,0)

    _add_pending = []
    def __init__(self,*args,**kw):
        pass        
    
    def update_childs(self):
        rect = self.rect
        c = len(self.childs)
        ssize = self.get_client_size()
        for i in range(c):
            #l t r b
            
            l = (((ssize[0]/c) * i ) + self.border) + self.rect[0]
            t = rect[1] + self.border
            r = (((ssize[0]/c) * (i+1) ) - (self.border*2)) + self.rect[0]
            b = rect[3] - (self.border * 2)
            self.childs[i].rect = (l,t,r,b)
            self.childs[i].fit_to_parent()
    
    def fit_to_parent(self):
        if self.parent:
            psize = self.parent.get_client_size()
            ssize = list(self.get_size())
            x = self.parent.border
            y = self.parent.border
            ssize = (psize[0] - self.parent.border * 2, psize[1] - self.parent.border * 2)
            self.move_resize((x,y),ssize)
            self.update_childs()

    
    
    def add_pennding(self):
        self._add_pending = list(set(self._add_pending))
        try:
            for i in self._add_pending:
                self.add(i,True)
        finally:
            self._add_pending = []
    
    
        
    
    def add(self,widget,force = False):
        self.childs.append(bin(widget,self))
        widget.fit_to_parent()
        self.update_childs()
        
        if not win32gui.IsWindowVisible(self.get_hwnd()) and not force:
            self._add_pending.append(widget)
            return
            
        if widget.type == "widget":
            win32gui.SetWindowLong(widget.get_hwnd(), GWL_STYLE, WS_CHILD)
            win32gui.SetParent(widget.get_hwnd(),self.get_hwnd())


        
    def get_client_rect(self):
        return self.rect
        
    def get_rect(self):
        return self.rect 
    
    def get_size(self):
        r = self.rect 
        return (r[2]-r[0],r[3]-r[1])
    
    def get_client_size(self):
        return self.get_size()
        
    def get_pos(self):
        return self.rect[:2]
    
    
    def move_resize(self,xy,wh,repaint = True):
        args = list(xy) + list(wh)
        self.rect = args
        self.update_childs()
        
    def show(self,show=True):
        pass
    
    def get_hwnd(self):
        if not self.parent:
            return -1
        return self.parent.get_hwnd()
    
    def show_all(self):
        self.show()
        for i in self.childs:
            i.show_all()
    
class vbox(hbox):
    def update_childs(self):
        c = len(self.childs)
        for i in range(c):
            #l t r b
            t = (i/c + self.border) + self.rect[1]
            l = rect[0] + self.border
            b = ((i+1)/c - (self.border*2)) + self.rect[3]
            r = rect[2] - (self.border * 2)
            self.childs[i].rect = (l,t,r,b)
            self.childs[i].fit_to_parent()


class bin(hbox):
    
    parent = None
    child = None
    
    def __init__(self,child,parent):
        self.rect = (0,0,0,0)
        self.child = child
        self.child.parent = self
        self.parent = parent
        if widget.type == "widget":
            win32gui.SetWindowLong(child.get_hwnd(), GWL_STYLE, WS_CHILD)
            win32gui.SetParent(child.get_hwnd(),self.get_hwnd())
    
    def fit_to_parent(self):
        if self.child:
            self.child.fit_to_parent()

    
    def show_all(self):
        self.show()
        if self.child:
            self.child.show_all()
    
    def move_resize(self,xy,wh,repaint = True):
        args = list(xy) + list(wh)
        self.rect = args
        self.child.fit_to_parent()
