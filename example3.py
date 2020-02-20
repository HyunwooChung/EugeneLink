import sys
import time
import ctypes
from ctypes import *
from ctypes.wintypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from win32 import win32gui
import win32gui,win32con
import win32ui
import win32api
import win32process
from ctypes.wintypes import HWND


form_class = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        time.sleep(1)
        #title = win32gui.GetWindowText(hwnd)
        hwnd = win32gui.GetForegroundWindow()
        print('1 :', hwnd)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()

    hwnd = win32gui.GetForegroundWindow()
    print('11 :', hwnd)

    l = win32ui.FindWindow(None, u"MainWindow")
    window_handle = l.GetSafeHwnd()
    print('22 :', window_handle)

    window_handle = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
    print('33 :', window_handle)

    window_handle = win32gui.GetForegroundWindow()
    print('44 :', window_handle)

    #window_handle5 = POINTER(HANDLE())
    window_handle = win32gui.GetForegroundWindow()
    print('55 :', window_handle)

    window_handle = win32ui.GetMainFrame().GetSafeHwnd()
    print('66 :', window_handle)


    app.exec_()

