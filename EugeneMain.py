import sys
import win32ui, win32gui, win32con, win32ts
from ctypes import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from EugeneHd  import *
from EugeneLib import *
from EugeneOrd import *
from EugeneQry import *
from EugeneReal import *

ui = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\EugeneWindow.ui")[0]

class MyWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 윈도우 이벤트 수신처리
        self.WindowEvent(self.winId())

        # 윈도우핸들러
        # 유진 Library 호출시 필요
        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
        sMsg = "윈도우핸들러 : " + str(self.Hwnd)
        self.TxtBrLog.append(sMsg)
        print(sMsg)

        # 윈도우폼 셋팅
        self.SetWindowForm()

        # 윈도우 컨트롤 셋팅
        self.SetControl()

        # 실시간 시세 인스턴스 생성
        self.CReal = EugeneReal(self)

        # 주문전송 인스턴스 생성
        self.COrd = EugeneOrd(self)

        # RQRP 조회 인스턴스 생성
        self.CQry = EugeneQry(self)

        iRtn = CLib.OpCommAPI_Initialize(self.Hwnd)

        if iRtn == 0:
            self.TxtBrLog.append("서버접속 : 실패")
        else:
            self.TxtBrLog.append("서버접속 : 성공")

        # 예제용 입력값
        self.EditCode.setText("005930")
        self.EditAcno.setText("27111091101")
        self.EditPswd.setText("1357")

    def SetWindowForm(self):
        # 우선호가 TableWidget 컬럼크기 셋팅
        iTblCnt = self.TablePrc.rowCount()
        for i in range(iTblCnt):
            self.TablePrc.setRowHeight(i, 20)

        # 체결시세 TableWidget 컬럼크기 셋팅
        iTblCnt = self.TableTick.rowCount()
        for i in range(iTblCnt):
            self.TableTick.setRowHeight(i, 20)

        # 주문/체결조회 TableWidget 컬럼크기 셋팅
        iTblCnt = self.TableTrd.rowCount()
        for i in range(iTblCnt):
            self.TableTrd.setRowHeight(i, 20)

        iTblCnt = self.TableTrd.columnCount()
        for i in range(iTblCnt):
            self.TableTrd.setColumnWidth(i, tpl_TablePstn[i][0])

        '''
        self.TableTrd.setColumnWidth( 0,  60)
        self.TableTrd.setColumnWidth( 1,  60)
        self.TableTrd.setColumnWidth( 2,  70)
        self.TableTrd.setColumnWidth( 3, 120)
        self.TableTrd.setColumnWidth( 4,  60)
        self.TableTrd.setColumnWidth( 5,  70)
        self.TableTrd.setColumnWidth( 6,  70)
        self.TableTrd.setColumnWidth( 7,  90)
        self.TableTrd.setColumnWidth( 8,  70)
        self.TableTrd.setColumnWidth( 9,  70)
        self.TableTrd.setColumnWidth(10,  90)
        '''

        # 잔고조회 TableWidget 컬럼크기 셋팅
        iTblRow = self.TablePstn.rowCount()
        for i in range(iTblRow):
            self.TablePstn.setRowHeight(i, 20)

        self.TablePstn.setColumnWidth( 0,  70)
        self.TablePstn.setColumnWidth( 1, 120)
        self.TablePstn.setColumnWidth( 2,  70)
        self.TablePstn.setColumnWidth( 3,  70)
        self.TablePstn.setColumnWidth( 4,  70)
        self.TablePstn.setColumnWidth( 5,  90)
        self.TablePstn.setColumnWidth( 6, 110)
        self.TablePstn.setColumnWidth( 7, 110)
        self.TablePstn.setColumnWidth( 8, 110)


    # 윈도우 컨트롤 셋팅
    def SetControl(self):
        self.BtnTrd.clicked.connect(self.BtnTrdClick)
        self.BtnPstn.clicked.connect(self.BtnPstnClick)
        self.BtnPrc.clicked.connect(self.BtnPrcClick)
        self.BtnBuy.clicked.connect(self.BtnBuyClick)
        self.BtnSell.clicked.connect(self.BtnSellClick)
        self.BtnMdfy.clicked.connect(self.BtnMdfyClick)
        self.BtnCncl.clicked.connect(self.BtnCnclClick)
        self.EditCode.textChanged.connect(self.EditCodeChanged)
        self.CmbBns.currentIndexChanged.connect(self.CmbBnsChanged)


    # 유진 API 윈도우 이벤트 수신처리
    # PyQt 사용시 일반적인 윈도우 이벤트 수신처리 방법을 모르겠음
    # 해당방법으로 정상 작동은 함
    def WindowEvent(self, app_hwnd):
        win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        #win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

        def WindowProc(hWnd, msg, wParam, lParam):
            if msg == WM_EU_REAL_RECV:
                self.RecvReal(wParam, lParam)
            elif msg == WM_EU_RQRP_RECV:
                self.RecvRqRp(wParam, lParam)
            elif msg == WM_EU_RQRP_ERR_RECV:
                self.RecvRqRpErr(wParam, lParam)
            elif msg == WM_EU_NOTI_RECV:
                pass
            elif msg == win32con.WM_DESTROY:
                iRtn = CLib.OpCommAPI_UnInitialize()
                if iRtn == 0:
                    self.TxtBrLog.append("서버종료 : 실패")
                else:
                    self.TxtBrLog.append("서버종료 : 성공")

                win32gui.DestroyWindow(app_hwnd)
                win32gui.PostQuitMessage(0)

            try:
                return win32gui.CallWindowProc(self.old_win32_proc, hWnd, msg, wParam, lParam)
            except Exception as e:
                print("except")

        self.old_win32_proc = win32gui.SetWindowLong(app_hwnd, win32con.GWL_WNDPROC, WindowProc)


    def RecvReal(self, wParam, lParam):
        # 실시간 주식 우선호가 수신처리
        if wParam == REAL_TRAN_STK_PRC:
            self.CReal.RecvRealStkPrc(wParam, lParam)
        # 실시간 주식 체결시세 수신처리
        elif wParam == REAL_TRAN_STK_TICK:
            self.CReal.RecvRealStkTick(wParam, lParam)


    def RecvRqRp(self, wParam, lParam):
        # 주식 매도/매수 주문 응답처리
        if wParam == self.iRqRpID and self.RQRP_TRAN_ID == RQRP_TRAN_STK_ORD:
            self.COrd.RecvStkOrd(wParam, lParam, self.iRqRpID)
        # 주식 정정/취소 주문 응답처리
        elif wParam == self.iRqRpID and self.RQRP_TRAN_ID == RQRP_TRAN_STK_MDFY:
            self.COrd.RecvStkMdfy(wParam, lParam, self.iRqRpID)
        # 주식 주문/체결 조회 응답처리
        elif wParam == self.iRqRpID and self.RQRP_TRAN_ID == RQRP_TRAN_STK_TRD:
            self.CQry.RecvStkTrd(wParam, lParam, self.iRqRpID)
        # 주식잔고 조회 응답처리
        elif wParam == self.iRqRpID and self.RQRP_TRAN_ID == RQRP_TRAN_STK_PSTN:
            self.CQry.RecvStkPstn(wParam, lParam, self.iRqRpID)

        CLib.OpCommAPI_ClearRQData()


    def RecvRqRpErr(self, wParam, lParam):
        print(wParam)
        print(lParam)


    # 실시간시세 버튼 클릭
    def BtnPrcClick(self):
        self.CReal.ReqRealStkPrc()

    # 주식 주문/체결 조회 버튼 클릭
    def BtnTrdClick(self):
        self.iRqRpID = self.CQry.QueryStkTrd()
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_TRD

    # 주식잔고 조회 버튼 클릭
    def BtnPstnClick(self):
        self.iRqRpID = self.CQry.QueryStkPstn()
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_PSTN

    # 주식 매수주문 버튼 클릭
    def BtnBuyClick(self):
        self.iRqRpID = self.COrd.SendStkOrd("20")
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_ORD

    # 주식 매도주문 버튼 클릭
    def BtnSellClick(self):
        self.iRqRpID = self.COrd.SendStkOrd("10")
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_ORD

    # 주식 정정주문 버튼 클릭
    def BtnMdfyClick(self):
        self.iRqRpID = self.COrd.SendStkMdfy("20")
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_MDFY

    # 주식 취소주문 버튼 클릭
    def BtnCnclClick(self):
        self.iRqRpID = self.COrd.SendStkMdfy("30")
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_MDFY

    # 주문유형 콤보박스 변경시
    def CmbBnsChanged(self):
        pass

    # 종목코드 입력시
    def EditCodeChanged(self):
        sCode = self.EditCode.text()
        # 종목코드를 6자리 입력한 경우 종목명 조회
        if len(sCode) == 6:
            self.EditCode_2.setText(sCode)

            sCode = sCode.encode()
            sCodeNM = CLib.OpCodeAPI_GetNameByCode(sCode)
            sCodeNM = sCodeNM.decode("cp949")
            self.TxtBrNm.setText(sCodeNM)
            self.TxtBrNm_2.setText(sCodeNM)
        else:
            self.TxtBrNm.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()
