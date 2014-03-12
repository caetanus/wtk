#!/usr/bin/env python

import window
import Label
import box
import Button
import Edit
import socket
import combobox

i = 0

w = window.Window("teste de toolkit")
b = Button.Button("isso")
e = Edit.Edit("teste")
c = combobox.ComboBox()
hb = box.hbox()
import Timer
#w.debug_events = True
l = Label.Label("oi mundo")

def clicked(*args):
    print "hey, stop clicking me"

def clicked2(*args):
    w.MsgBox("Hey, stop clicking me 2!")

def timer():
    global i
    i += 1
    l.set_text("timer was called %d times" % i)
    return True

def clicked3(*args):
    Timer.Timer(1,timer)

def no_focus(*args):
    return False
    
b.debug_events = True
import win32con


b.connect(win32con.WM_COMMAND,clicked)
b.connect(win32con.WM_SETFOCUS,no_focus)
w.connect(win32con.WM_LBUTTONDOWN,clicked3)

print hb.parent 
w.add(hb)
print hb.parent
hb.add(b)
hb.add(e)
hb.add(l)
hb.add(c)

c.debug_events = True

w.show_all()
c.append("oi mundo")
c.insert("ae galera!")
c.insert("ae galera!")
#e.insert("ae galera!")
#e.insert("ae galera!")
#e.insert("ae galera!")

#e.select(0)
#window.main()

s = socket.socket()
s.bind(("0.0.0.0",6666))
s.listen(0)
def on_socket(self):
    global s
    print "temos um eventinho!"

w.io_add_watch(s,on_socket)

window.win32gui.PumpMessages()
