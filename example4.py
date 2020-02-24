import sys
import time
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import win32con
import win32gui
import win32api
import win32ui

class MyWindow(object):
    def __init__(self):
        print('start')

    def OpenWindow(self):
        self.visible = 0
        message_map = {
            win32con.WM_DESTROY: self.onDestroy,
            win32con.WM_USER + 20: self.onDestroy,
            win32con.WM_LBUTTONUP: self.onDestroy,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "MainWindow"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = self.WindowProcdure
        classAtom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "MainWindow", style,
                                  0, 0, 310, 250,
                                  0, 0, hinst, None)

        self.pfirm = win32gui.CreateWindow("Button", "확인", win32con.WS_CHILD | win32con.BS_PUSHBUTTON, \
                                           10, 10, 60, 25, self.hwnd, hinst, 0, None)

        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.ShowWindow(self.pfirm, win32con.SW_SHOW)

        self.window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()

        self.OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')
        self.OpCodeAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCodeAPI.dll')

        self.OpCommAPI_Initialize = self.OpCommAPI.OpCommAPI_Initialize
        self.OpCommAPI_Initialize.restype = c_bool
        self.OpCommAPI_Initialize.argtypes = [c_int]

        self.OpCommAPI_UnInitialize = self.OpCommAPI.OpCommAPI_UnInitialize
        self.OpCommAPI_UnInitialize.restype = c_bool
        self.OpCommAPI_UnInitialize.argtypes = []

        self.OpCommAPI_SetRqData = self.OpCommAPI.OpCommAPI_SetRQData
        self.OpCommAPI_SetRqData.restype = c_void_p
        self.OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

        self.OpCommAPI_SendRq = self.OpCommAPI.OpCommAPI_SendRq
        self.OpCommAPI_SendRq.restype = c_int
        self.OpCommAPI_SendRq.argtypes = (c_int, c_int, c_int)

        self.OpCommAPI_ClearRQData = self.OpCommAPI.OpCommAPI_ClearRQData
        self.OpCommAPI_ClearRQData.restype = c_void_p
        self.OpCommAPI_ClearRQData.argtypes = []

        self.OpCodeAPI_GetExpCode = self.OpCodeAPI.OpCodeAPI_GetExpCode
        self.OpCodeAPI_GetExpCode.restype = c_char_p
        self.OpCodeAPI_GetExpCode.argtypes = [c_char_p]

        self.OpCommAPI_GetRqrpData = self.OpCommAPI.OpCommAPI_GetRqrpData
        self.OpCommAPI_GetRqrpData.restype = c_char_p
        self.OpCommAPI_GetRqrpData.argtypes = (c_int, c_int, c_int, c_int)

        self.OpCommAPI_GetRqrpCount = self.OpCommAPI.OpCommAPI_GetRqrpCount
        self.OpCommAPI_GetRqrpCount.restype = c_int
        self.OpCommAPI_GetRqrpCount.argtypes = (c_int, c_int,)

        err = self.OpCommAPI_Initialize(self.window_handle)
        if err == 0:
            print('Init 실패')
        else:
            print('Init 실패')

    def onDestroy(self):
        print('Destroy')

    def WindowProcdure(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_USER:
            print('11111')
        elif msg == win32con.WM_LBUTTONUP:
            print('Button Click')
            sAccn = b'27122016751'
            sPswd = b'1357'
            sCode = b'KR4201Q31900'
            sSCode = b'000020'

            self.OpCommAPI_SetRqData(0, sAccn)
            self.OpCommAPI_SetRqData(1, sPswd)

            self.result_753 = self.OpCommAPI_SendRq(self.window_handle, 753, 0)
            print('753 : ' + str(self.result_753))

        elif msg == 7419:
            dcnt = self.OpCommAPI_GetRqrpCount(self.result_753, 1)
            print ('dcnt : ', dcnt)
            for i in range(dcnt):
                print('i : ', i)
                value = self.OpCommAPI_GetRqrpData(self.result_753, 1, i, 1)
                print ('value 1 : ', value)
                value = self.OpCommAPI_GetRqrpData(self.result_753, 1, i, 2)
                print ('value 2 : ', value)
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)


if __name__ == '__main__':
    w = MyWindow()
    w.OpenWindow()
    win32gui.PumpMessages()