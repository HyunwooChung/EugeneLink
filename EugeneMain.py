import sys
import win32ui, win32gui, win32con, win32ts
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from EugeneHd  import *
from EugeneLib import *
from EugeneOrd import *
from EugeneCtl import *

ui = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\EugeneWindow.ui")[0]

class MyWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.CCtl = EugeneCtl()

        self.Clib = EugeneLib()
        self.Clib.LoadLib()

        self.WindowEvent(self.winId())
        self.SetControl()

        iErr = self.Clib.OpCommAPI_Initialize(self.winId())

        if iErr == 0:
            self.TxtBrLog.append('Initialize : 서버접속 성공')
        else:
            self.TxtBrLog.append('Initialize : 서버접속 실패')

    # 컨트롤 셋팅
    def SetControl(self):
        self.BtnJango.clicked.connect(self.CCtl.BtnJangoClick)
        self.BtnSise.clicked.connect(self.CCtl.BtnSiseClick)
        self.BtnBuy.clicked.connect(self.CCtl.BtnBuyClick)
        self.BtnSell.clicked.connect(self.CCtl.BtnSellClick)
        self.BtnMdfy.clicked.connect(self.CCtl.BtnMdfyClick)
        self.BtnCncl.clicked.connect(self.CCtl.BtnCnclClick)

    # 유진 API에서 송신하는 윈도우 이벤트 수신처리
    # pyqt5 사용시 일반적으로 윈도우 이벤트 수신처리 방법을 모르겠음
    # 해당방법으로 정상 작동은 함
    def WindowEvent(self, app_hwnd):
        win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        #win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

        def WindowProc(hWnd, msg, wParam, lParam):
            if msg == WM_EU_REAL_RECV:
                self.OnRealRecv(wParam, lParam)
            elif msg == WM_EU_RQRP_RECV:
                self.OnRqrpRecv(wParam, lParam)
            elif msg == win32con.WM_DESTROY:
                iErr = self.Clib.OpCommAPI_UnInitialize()
                if iErr == 0:
                    self.TxtBrLog.append('UnInitialize : 종료실패')
                else:
                    self.TxtBrLog.append('UnInitialize : 종료성공')

                win32gui.DestroyWindow(app_hwnd)
                win32gui.PostQuitMessage(0)

            try:
                return win32gui.CallWindowProc(self.old_win32_proc, hWnd, msg, wParam, lParam)
            except Exception as e:
                print("except")

        self.old_win32_proc = win32gui.SetWindowLong(app_hwnd, win32con.GWL_WNDPROC, WindowProc)


    def OnRqrpRecv(self, wParam, lParam):
        dcnt = self.OpCommAPI_GetRqrpCount(self.result_753, 1)
        msg = "조회건수 : " + str(dcnt)
        self.TxtBrLog.append(msg)
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

            self.TxtBrLog.append(sSise)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()
