import win32gui
import win32con
import win32api
import exceptions
import win32process
from win32con import *
import ctypes
user32 = ctypes.windll.user32

class Font:
    def __init__(self,Default=True):
        self.handle = win32gui.GetStockObject(ANSI_VAR_FONT)