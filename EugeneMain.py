import sys
import win32ui, win32gui, win32con, win32ts
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from EugeneHd  import *
from EugeneLib import *
from EugeneOrd import *
from EugeneRealPrc import *

ui = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\EugeneWindow.ui")[0]

class MyWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 유진 Library Load
        EugeneLib()

        # 실시간 시세 클래스 선언
        self.CRealPrc = EugeneRealPrc(self)

        # 윈도우 이벤트 수신처리
        self.WindowEvent(self.winId())

        # 윈도우 컨트롤 셋팅
        self.SetControl()

        # 윈도우핸들러
        # 유진 Library 호출시 필요
        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
        sMsg = "윈도우핸들러 : " + str(self.Hwnd)
        self.TxtBrLog.append(sMsg)

        iErr = EugeneLib.OpCommAPI_Initialize(self.Hwnd)

        if iErr == 0:
            self.TxtBrLog.append('Initialize : 서버접속 실패')
        else:
            self.TxtBrLog.append('Initialize : 서버접속 성공')

        self.EditCode.setText("005930")
        self.EditAcno.setText("27122016751")
        self.EditPswd.setText("1357")

    # 윈도우 컨트롤 셋팅
    def SetControl(self):
        self.BtnPstn.clicked.connect(self.BtnPstnClick)
        self.BtnPrc.clicked.connect(self.BtnPrcClick)
        self.BtnBuy.clicked.connect(self.BtnBuyClick)
        self.BtnSell.clicked.connect(self.BtnSellClick)
        self.BtnMdfy.clicked.connect(self.BtnMdfyClick)
        self.BtnCncl.clicked.connect(self.BtnCnclClick)
        self.EditCode.textChanged.connect(self.EditCodeChanged)

    # 유진 API 윈도우 이벤트 수신처리
    # PyQt 사용시 일반적인 윈도우 이벤트 수신처리 방법을 모르겠음
    # 해당방법으로 정상 작동은 함
    def WindowEvent(self, app_hwnd):
        win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        #win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

        def WindowProc(hWnd, msg, wParam, lParam):
            if msg == WM_EU_REAL_RECV:
                # 실시간 주식 우선호가 수신처리
                if wParam == REAL_TRAN_PRC:
                    self.CRealPrc.RecvRealPrc(wParam, lParam)
                # 실시간 주식 체결시세 수신처리
                elif wParam == REAL_TRAN_TRD:
                    self.CRealPrc.RecvRealTrd(wParam, lParam)

            elif msg == WM_EU_RQRP_RECV:
                pass


            elif msg == win32con.WM_DESTROY:
                iErr = EugeneLib.OpCommAPI_UnInitialize()
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


    # 실시간시세 버튼 클릭
    def BtnPrcClick(self):
        self.CRealPrc.ReqRealPrc()

    # 잔고조회 버튼 클릭
    def BtnPstnClick(self):
        pass

    # 매수주문 버튼 클릭
    def BtnBuyClick(self):
        pass

    # 매도주문 버튼 클릭
    def BtnSellClick(self):
        pass

    # 정정주문 버튼 클릭
    def BtnMdfyClick(self):
        pass

    # 취소주문 버튼 클릭
    def BtnCnclClick(self):
        pass

    def EditCodeChanged(self):
        sCode = self.EditCode.text()
        # 종목코드를 6자리 입력한 경우 종목명 조회
        if len(sCode) == 6:
            sCode = sCode.encode()
            sCodeNM = EugeneLib.OpCodeAPI_GetNameByCode(sCode)
            sCodeNM = sCodeNM.decode("cp949")
            self.TxtBrNm.setText(sCodeNM)
        else:
            self.TxtBrNm.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()


