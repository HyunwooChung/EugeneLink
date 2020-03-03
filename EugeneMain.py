import sys
import win32ui, win32gui, win32con, win32ts
from ctypes import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
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

        # 디폴트 입력값
        self.EditCode.setText("005930")
        self.EditAcno.setText("27111091101")
        self.EditPswd.setText("1357")


    # 윈도우 form 셋팅
    def SetWindowForm(self):
        # 우선호가 QTableWidget 컬럼 Height 셋팅
        iTblCnt = self.TablePrc.rowCount()
        for i in range(iTblCnt):
            self.TablePrc.setRowHeight(i, 20)

        # 체결시세 QTableWidget 컬럼 Height 셋팅
        iTblCnt = self.TableTick.rowCount()
        for i in range(iTblCnt):
            self.TableTick.setRowHeight(i, 20)

        # 주문/체결조회 QTableWidget 컬럼 Height 셋팅
        iTblCnt = self.TableTrd.rowCount()
        for i in range(iTblCnt):
            self.TableTrd.setRowHeight(i, 20)

        # 주문/체결조회 QTableWidget 컬럼 Width 셋팅
        iTblCnt = self.TableTrd.columnCount()
        for i in range(iTblCnt):
            self.TableTrd.setColumnWidth(i, TPL_TRD_FORM[i][0])

        # 잔고조회 QTableWidget 컬럼 Height 셋팅
        iTblRow = self.TablePstn.rowCount()
        for i in range(iTblRow):
            self.TablePstn.setRowHeight(i, 20)

        # 잔고조회 QTableWidget 컬럼 Width 셋팅
        iTblCnt = self.TablePstn.columnCount()
        for i in range(iTblCnt):
            self.TablePstn.setColumnWidth(i, TPL_PSTN_FORM[i][0])

        # 숫자만 입력 가능하도록 셋팅
        self.EditCode.setValidator(QIntValidator())
        self.EditCode_2.setValidator(QIntValidator())
        self.EditPrc.setValidator(QIntValidator())
        self.EditPrc_2.setValidator(QIntValidator())
        self.EditQty.setValidator(QIntValidator())
        self.EditQty_2.setValidator(QIntValidator())
        self.EditOOrdNo.setValidator(QIntValidator())

        # 비밀번호 **** 마스킹 처리
        self.EditPswd.setEchoMode(QLineEdit.Password)


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
            # OpCommAPI_RequestReal 요청에 대한 실시간 데이터 수신 메시지
            if msg == WM_EU_REAL_RECV:
                self.RecvReal(wParam, lParam)
            # OpCommAPI_SendRQ 요청에 대한 응답 메시지
            elif msg == WM_EU_RQRP_RECV:
                self.RecvRqRp(wParam, lParam)
            # OpCommAPI_SendRQ 요청에 대한 오류응답 메시지
            elif msg == WM_EU_RQRP_ERR_RECV:
                self.RecvRqRpErr(wParam, lParam)
            # 서버에서 보내는 긴급 메시지(통신단절, 접속해제 등)
            elif msg == WM_EU_NOTI_RECV:
                self.RecvNoti(wParam, lParam)
            elif msg == win32con.WM_DESTROY:
                iRtn = CLib.OpCommAPI_UnInitialize()
                if iRtn == 0:
                    self.TxtBrLog.append("서버종료 : 실패")
                else:
                    self.TxtBrLog.append("서버종료 : 성공")

                CLib.OpCommAPI_UnRegisterRealAll(self.Hwnd)

                win32gui.DestroyWindow(app_hwnd)
                win32gui.PostQuitMessage(0)

            try:
                return win32gui.CallWindowProc(self.old_win32_proc, hWnd, msg, wParam, lParam)
            except Exception as e:
                print("except")

        self.old_win32_proc = win32gui.SetWindowLong(app_hwnd, win32con.GWL_WNDPROC, WindowProc)


    # OpCommAPI_RequestReal 요청에 대한 실시간 데이터 수신 처리
    def RecvReal(self, wParam, lParam):
        # 실시간 주식 우선호가 수신처리
        if wParam == REAL_TRAN_STK_PRC:
            self.CReal.RecvRealStkPrc(wParam, lParam)
        # 실시간 주식 체결시세 수신처리
        elif wParam == REAL_TRAN_STK_TICK:
            self.CReal.RecvRealStkTick(wParam, lParam)


    # OpCommAPI_SendRQ 요청에 대한 응답 처리
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


    # OpCommAPI_SendRQ 요청에 대한 오류응답 처리
    def RecvRqRpErr(self, wParam, lParam):
        # lParam 주소값을 문자열로 변환
        sVal = string_at(lParam)
        sVal = sVal.decode("cp949")
        self.TxtBrErr.setText(sVal)


    # 서버에서 보내는 긴급 메시지
    def RecvNoti(self, wParam, lParam):
        sErrMsg = DIC_NOTI_MSG.get(wParam)
        sErrMsg = "알림 : " + sErrMsg
        self.TxtBrLog.append(sErrMsg)

        # wParam = 100 : 서버에서 내려온 긴급 메시지
        if wParam == 100:
            # lParam 주소값을 문자열로 변환
            sErrMsg = string_at(lParam)
            sErrMsg = sErrMsg.decode("cp949")
            self.TxtBrLog.append(sErrMsg)


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
        sVal = self.CmbBns.currentText()
        # 지정가, 조건부지정가인 경우 가격 입력가능
        if sVal[:3] == "010" or sVal[:3] == "030":
            self.EditPrc.setEnabled(True)
        # 시장가, 최유리지정가, 최우선지정가인 경우 가격 입력불가
        else:
            self.EditPrc.setText("0")
            self.EditPrc.setEnabled(False)

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
