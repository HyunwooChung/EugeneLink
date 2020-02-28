# 개발환경 : Anaconda3 32bit, Pycharm 32bit
# 설치모듈 : pyqt5, pywin32
import sys
import time
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32ui, win32gui, win32con, win32ts
import LinkHeader as hd

WM_WTSSESSION_CHANGE = 0x2B1

form_class = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ButtonClick)
        self.pushButton_2.clicked.connect(self.ButtonClick_2)
        self.pushButton_3.clicked.connect(self.ButtonClick_3)
        self.lineEdit.setText("005930")
        self.lineEdit_2.setText("27122016751")
        self.lineEdit_3.setText("1357")
        self.session_events(self.winId())
        self.load_lib()


    def session_events(self, app_hwnd):
        win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        #win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

        def MyWndProc(hWnd, msg, wParam, lParam):
            if msg == WM_WTSSESSION_CHANGE:
                print("msg change")
            elif msg == hd.WM_EU_REAL_RECV:

            elif msg == hd.WM_EU_RQRP_RECV:
                self.OnRqrpRecv(wParam, lParam)
            elif msg == win32con.WM_DESTROY:
                err = self.OpCommAPI_UnInitialize()
                if err == 0:
                    self.textBrowser.append('Initialize : 실패')
                else:
                    self.textBrowser.append('Initialize : 성공')

                win32gui.DestroyWindow(app_hwnd)
                win32gui.PostQuitMessage(0)

            try:
                return win32gui.CallWindowProc(self.old_win32_proc, hWnd, msg, wParam, lParam)
            except Exception as e:
                print("except")

        self.old_win32_proc = win32gui.SetWindowLong(app_hwnd, win32con.GWL_WNDPROC, MyWndProc)

    # 유진챔피언링크에서 제공하는 Library 로드 및 함수 정의
    def load_lib(self):
        self.window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        msg = "Handle : " + str(self.window_handle)
        self.textBrowser.append(msg)

        self.OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')
        self.OpCodeAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCodeAPI.dll')

        self.OpCommAPI_Initialize = self.OpCommAPI.OpCommAPI_Initialize
        self.OpCommAPI_Initialize.restype = c_bool
        self.OpCommAPI_Initialize.argtypes = [c_int]

        print(type(msg))
        print(type(self.OpCommAPI_Initialize))

        self.OpCommAPI_UnInitialize = self.OpCommAPI.OpCommAPI_UnInitialize
        self.OpCommAPI_UnInitialize.restype = c_bool
        self.OpCommAPI_UnInitialize.argtypes = []

        # 조회 데이터
        self.OpCommAPI_SetRqData = self.OpCommAPI.OpCommAPI_SetRQData
        self.OpCommAPI_SetRqData.restype = c_void_p
        self.OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

        self.OpCommAPI_SendRq = self.OpCommAPI.OpCommAPI_SendRq
        self.OpCommAPI_SendRq.restype = c_int
        self.OpCommAPI_SendRq.argtypes = [c_int, c_int, c_int]

        self.OpCommAPI_ClearRQData = self.OpCommAPI.OpCommAPI_ClearRQData
        self.OpCommAPI_ClearRQData.restype = c_void_p
        self.OpCommAPI_ClearRQData.argtypes = []

        self.OpCodeAPI_GetExpCode = self.OpCodeAPI.OpCodeAPI_GetExpCode
        self.OpCodeAPI_GetExpCode.restype = c_char_p
        self.OpCodeAPI_GetExpCode.argtypes = [c_char_p]

        self.OpCommAPI_GetRqrpData = self.OpCommAPI.OpCommAPI_GetRqrpData
        self.OpCommAPI_GetRqrpData.restype = c_char_p
        self.OpCommAPI_GetRqrpData.argtypes = [c_int, c_int, c_int, c_int]

        self.OpCommAPI_GetRqrpCount = self.OpCommAPI.OpCommAPI_GetRqrpCount
        self.OpCommAPI_GetRqrpCount.restype = c_int
        self.OpCommAPI_GetRqrpCount.argtypes = [c_int, c_int]

        # 실시간 데이터
        self.OpCommAPI_RequestReal = self.OpCommAPI.OpCommAPI_RequestReal
        self.OpCommAPI_RequestReal.restype = c_int
        self.OpCommAPI_RequestReal.argtypes = [c_int, c_bool, c_byte, c_char_p]

        self.OpCommAPI_UnRegisterRealAll = self.OpCommAPI.OpCommAPI_UnRegisterRealAll
        self.OpCommAPI_UnRegisterRealAll.restype = c_void_p
        self.OpCommAPI_UnRegisterRealAll.argtypes = [c_int]

        self.OpCommAPI_GetRealData = self.OpCommAPI.OpCommAPI_GetRealData
        self.OpCommAPI_GetRealData.restype = c_char_p
        self.OpCommAPI_GetRealData.argtypes = [c_byte, c_int]

        # 종목코드 관련 데이터
        self.OpCodeAPI_GetExpCode = self.OpCodeAPI.OpCodeAPI_GetExpCode
        self.OpCodeAPI_GetExpCode.restype = c_char_p
        self.OpCodeAPI_GetExpCode.argtypes = [c_char_p]

        self.OpCodeAPI_GetNameByCode = self.OpCodeAPI.OpCodeAPI_GetNameByCode
        self.OpCodeAPI_GetNameByCode.restype = c_char_p
        self.OpCodeAPI_GetNameByCode.argtypes = [c_char_p]

        err = self.OpCommAPI_Initialize(self.window_handle)
        if err == 0:
            self.textBrowser.append('Initialize : 실패')
        else:
            self.textBrowser.append('Initialize : 성공')

    def ButtonClick(self):
        sCode = self.lineEdit.text()
        sCode = sCode.encode()

        name = self.OpCodeAPI_GetNameByCode(sCode)
        name = name.decode("cp949")

        self.textBrowser_2.setText(name)

        sStCode = self.OpCodeAPI_GetExpCode(sCode)
        sStCode = sStCode.decode("cp949")

        self.textBrowser_4.setText(sStCode)

        # err = OpCommAPI_UnInitialize()
        # print(err)

    # 선물 잔고조회 RQRP_ID : 753
    def ButtonClick_2(self):
        sAccn = self.lineEdit_2.text()
        sPswd = self.lineEdit_3.text()
        sAccn = sAccn.encode()
        sPswd = sPswd.encode()

        self.OpCommAPI_SetRqData(0, sAccn)
        self.OpCommAPI_SetRqData(1, sPswd)

        self.result_753 = self.OpCommAPI_SendRq(self.window_handle, 753, 0)

        msg = 'SendRq 753 : ' + str(self.result_753)
        self.textBrowser.append(msg)

    def ButtonClick_3(self):
        sCode = self.lineEdit.text()
        sCode = sCode.encode()

        # 표준종목코드로 변환하여 조회
        sStCode = self.OpCodeAPI_GetExpCode(sCode)

        err = self.OpCommAPI_RequestReal(self.window_handle, True, 21, sStCode)

        if err == 0:
            self.textBrowser.append('RequestReal : 성공')
        else:
            self.textBrowser.append('RequestReal : 실패')


    def OnRqrpRecv(self, wParam, lParam):
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

        self.OpCommAPI_ClearRQData()

    def OnRealRecv(self, wParam, lParam):

        if wParam == 21:
            value = self.OpCommAPI_GetRealData(wParam, 0)  # 종목코드
            value = value.decode("cp949")
            sSise = value

            value = self.OpCommAPI_GetRealData(wParam, 1)  # 체결시간
            value = value.decode("cp949")
            sSise = sSise + ' | ' + value

            value = self.OpCommAPI_GetRealData(wParam, 4)  # 체결가
            value = value.decode("cp949")
            sSise = sSise + ' | ' + value

            value = self.OpCommAPI_GetRealData(wParam, 12)  # 매도호가
            value = value.decode("cp949")
            sSise = sSise + ' | ' + value

            value = self.OpCommAPI_GetRealData(wParam, 13)  # 매수호가
            value = value.decode("cp949")
            sSise = sSise + ' | ' + value

            self.textBrowser_3.append(sSise)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()