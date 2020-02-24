# 개발환경 : Anaconda3 32bit, Pycharm 32bit
# 설치모듈 : pyqt5, pywin32

import sys
import time
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32ui, win32gui, win32con, win32ts

WM_WTSSESSION_CHANGE = 0x2B1

WM_EU_RQRP_RECV = 7419

form_class = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ButtonClick)
        self.pushButton_2.clicked.connect(self.ButtonClick_2)
        self.session_events(self.winId())
        self.load_api()

    def session_events(self, app_hwnd):
        win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

        def MyWndProc(hWnd, msg, wParam, lParam):
            if msg == WM_WTSSESSION_CHANGE:
                print("msg change")
            elif msg == WM_EU_RQRP_RECV:
                self.OnReceive()
            elif msg == win32con.WM_DESTROY:
                win32gui.DestroyWindow(app_hwnd)
                win32gui.PostQuitMessage(0)

            try:
                return win32gui.CallWindowProc(self.old_win32_proc, hWnd, msg, wParam, lParam)
            except Exception as e:
                print("except")

        self.old_win32_proc = win32gui.SetWindowLong(app_hwnd, win32con.GWL_WNDPROC, MyWndProc)

    def load_api(self):
        self.textBrowser.append('111')
        self.window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        msg = "Handle : " + str(self.window_handle)
        self.textBrowser.append(msg)

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
            self.textBrowser.append('Initialize : 실패')
        else:
            self.textBrowser.append('Initialize : 성공')

    def ButtonClick(self):

        sAccn = b'27122016751'
        sPswd = b'1357'
        sCode = b'KR4201Q31900'
        sSCode = b'000020'

        self.OpCommAPI_SetRqData(0, sAccn)
        self.OpCommAPI_SetRqData(1, sPswd)

        self.result_753 = self.OpCommAPI_SendRq(self.window_handle, 753, 0)
        print('Acno : ' + str(sAccn))

        msg = 'SendRq 753 : ' + str(self.result_753)
        self.textBrowser.append(msg)

        '''
        self.OpCommAPI_ClearRQData()

        self.OpCommAPI_SetRqData(0, sCode)
        result = self.OpCommAPI_SendRq(self.window_handle, 351, 0)

        msg = 'SendRq 351 : ' + str(result)
        self.textBrowser.append(msg)

        code = self.OpCodeAPI_GetExpCode(sSCode)
        msg = 'Code : ' + str(code)
        self.textBrowser.append(msg)
        '''

        #err = OpCommAPI_UnInitialize()
        #print(err)

    def ButtonClick_2(self):
        self.textBrowser.append("PostMessage")
        window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        #win32gui.PostMessage(window_handle, WM_EU_RQRP_RECV, 0, 0)

    def OnReceive(self):
        dcnt = self.OpCommAPI_GetRqrpCount(self.result_753, 1)
        msg = "조회건수 : " + str(dcnt)
        self.textBrowser.append(msg)
        for i in range(dcnt):
            value = self.OpCommAPI_GetRqrpData(self.result_753, 1, i, 0)
            value = value.decode("cp949")
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(value)))

            value = self.OpCommAPI_GetRqrpData(self.result_753, 1, i, 2)
            value = value.decode("cp949")
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(value)))

            value = self.OpCommAPI_GetRqrpData(self.result_753, 1, i, 3)
            value = value.decode("cp949")
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(value)))

            value = self.OpCommAPI_GetRqrpData(self.result_753, 1, i, 6)
            value = value.decode("cp949")
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()