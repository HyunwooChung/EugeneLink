import sys
import time
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32ui, win32gui, win32con, win32api
from pywin.mfc import docview, dialog, window

WM_EU_RQRP_RECV = 7419

form_class = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ButtonClick)
        self.pushButton_2.clicked.connect(self.ButtonClick_2)

        message_map = {
                WM_EU_RQRP_RECV: self.OnReceive,
                win32con.WM_SIZE: self.OnReceive,
        }


    def OnReceive(self):
        self.textBrowser.append("Receive PostMessage")

    def ButtonClick(self):
        self.textBrowser.append('111')
        window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        msg = "Handle : "+ str(window_handle)
        self.textBrowser.append(msg)

        OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')
        OpCodeAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCodeAPI.dll')

        OpCommAPI_Initialize = OpCommAPI.OpCommAPI_Initialize
        OpCommAPI_Initialize.restype = c_bool
        OpCommAPI_Initialize.argtypes = [c_int]

        OpCommAPI_UnInitialize = OpCommAPI.OpCommAPI_UnInitialize
        OpCommAPI_UnInitialize.restype = c_bool
        OpCommAPI_UnInitialize.argtypes = []

        OpCommAPI_SetRqData = OpCommAPI.OpCommAPI_SetRQData
        OpCommAPI_SetRqData.restype = c_void_p
        OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

        OpCommAPI_SendRq = OpCommAPI.OpCommAPI_SendRq
        OpCommAPI_SendRq.restype = c_int
        OpCommAPI_SendRq.argtypes = (c_int, c_int, c_int)

        OpCommAPI_ClearRQData = OpCommAPI.OpCommAPI_ClearRQData
        OpCommAPI_ClearRQData.restype = c_void_p
        OpCommAPI_ClearRQData.argtypes = []

        OpCodeAPI_GetExpCode = OpCodeAPI.OpCodeAPI_GetExpCode
        OpCodeAPI_GetExpCode.restype = c_char_p
        OpCodeAPI_GetExpCode.argtypes = [c_char_p]

        err = OpCommAPI_Initialize(window_handle)
        if err == 0 :
            self.textBrowser.append('Initialize : 실패')
        else:
            self.textBrowser.append('Initialize : 성공')

        sAccn = b'27122016751'
        sPswd = b'1357'
        sCode = b'KR4201Q31900'
        sSCode = b'000020'

        OpCommAPI_SetRqData(0, sAccn)
        OpCommAPI_SetRqData(1, sPswd)

        result = OpCommAPI_SendRq(window_handle, 753, 0)
        print('Acno : ' + str(sAccn))

        msg = 'SendRq 753 : ' + str(result)
        self.textBrowser.append(msg)

        OpCommAPI_ClearRQData()

        OpCommAPI_SetRqData(0, sCode)
        result = OpCommAPI_SendRq(window_handle, 351, 0)

        msg = 'SendRq 351 : ' + str(result)
        self.textBrowser.append(msg)

        code = OpCodeAPI_GetExpCode(sSCode)
        msg = 'Code : ' + str(code)
        self.textBrowser.append(msg)

        err = OpCommAPI_UnInitialize()
        print(err)

    def ButtonClick_2(self):
        self.textBrowser.append("PostMessage")
        window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        win32gui.PostMessage(window_handle, WM_EU_RQRP_RECV, 0, 0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()