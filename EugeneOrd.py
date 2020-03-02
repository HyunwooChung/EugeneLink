import win32ui
from PyQt5.QtWidgets import *
from EugeneHd import *
from EugeneLib import *

# 주문 송신 모듈
class EugeneOrd(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    # 주식 매도/매수 주문 전송처리
    def SendStkOrd(self, sOrdTp):
        self.ui.TxtBrOrdNo.setText("")

        sVal = self.ui.EditAcno.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 0, sVal)       # 계좌번호

        sVal = self.ui.EditPswd.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 1, sVal)       # 비밀번호

        sVal = self.ui.EditCode.text()
        sVal = sVal.encode()
        # 표준종목코드로 변환하여 전송
        sVal = CLib.OpCodeAPI_GetExpCode(sVal)
        CLib.OpCommAPI_SetRqData( 2, sVal)       # 종목코드

        sVal = self.ui.EditQty.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 3, sVal)       # 주문수량

        sVal = self.ui.EditPrc.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 4, sVal)       # 주문가격

        sVal = sOrdTp.encode()
        CLib.OpCommAPI_SetRqData( 5, sVal)       # 매도매수구분 (10:매도, 20:매수)

        sVal = self.ui.CmbBns.currentText()
        sVal = sVal[:3].encode()
        CLib.OpCommAPI_SetRqData( 6, sVal)       # 매매구분코드 (010:지정가, 020:시장가:, 030:조건부, 040:최유리, 050:최우선)

        CLib.OpCommAPI_SetRqData( 7, b"010")     # 신용거래구분 (010 고정)
        CLib.OpCommAPI_SetRqData( 9, b"N")       # 담보대출주문여부 (N 고정)

        sVal = self.ui.CmbCnd.currentText()
        sVal = sVal[:1].encode()
        CLib.OpCommAPI_SetRqData(10, sVal)       # 주문조건코드 (0:없음, 1:IOC, 2:FOK)

        CLib.OpCommAPI_SetRqData(11, b"010")     # 프로그램호가구분 (010 고정)
        CLib.OpCommAPI_SetRqData(12, b"0")       # 프로그램호가신고구분 (0 고정)
        CLib.OpCommAPI_SetRqData(13, b"N")       # 선물대용여부 (N 고정)
        CLib.OpCommAPI_SetRqData(14, b"000")     # 반대매매상환구분 (000 고정)
        CLib.OpCommAPI_SetRqData(18, b"N")       # 보류대상주문확인여부 (N 고정)
        CLib.OpCommAPI_SetRqData(22, b"N")       # 공매도가능여부 (N 고정)
        CLib.OpCommAPI_SetRqData(23, b"00")      # 공매도구분 (00 고정)

        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
        iRtn = CLib.OpCommAPI_SendRq(self.Hwnd, RQRP_TRAN_STK_ORD, 0)

        if iRtn < 0:
            sErrMsg = dic_sendrq_error.get(iRtn)
            sErrMsg = "신규주문 전송 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)

        return iRtn


    # 주식 정정/취소 주문 전송처리
    def SendStkMdfy(self, sOrdTp):
        self.ui.TxtBrOrdNo_2.setText("")

        sVal = self.ui.EditAcno.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 0, sVal)       # 계좌번호

        sVal = self.ui.EditPswd.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 1, sVal)       # 비밀번호

        sVal = self.ui.EditOOrdNo.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 2, sVal)       # 원주문번호

        sVal = sOrdTp.encode()
        CLib.OpCommAPI_SetRqData( 3, sVal)       # 매도매수구분 (20:정정, 30:취소)

        CLib.OpCommAPI_SetRqData( 4, b"20")      # 일부전부구분 (20:전부)

        sVal = self.ui.EditCode_2.text()
        sVal = sVal.encode()
        # 표준종목코드로 변환하여 전송
        sVal = CLib.OpCodeAPI_GetExpCode(sVal)
        CLib.OpCommAPI_SetRqData( 5, sVal)       # 종목코드

        sVal = self.ui.EditQty_2.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 6, sVal)       # 주문수량

        sVal = self.ui.EditPrc_2.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 7, sVal)       # 주문가격

        sVal = self.ui.CmbBns.currentText()
        sVal = sVal[:3].encode()
        CLib.OpCommAPI_SetRqData( 8, sVal)       # 매매구분코드 (010:지정가, 020:시장가:, 030:조건부, 040:최유리, 050:최우선)

        sVal = self.ui.CmbCnd.currentText()
        sVal = sVal[:1].encode()
        CLib.OpCommAPI_SetRqData( 9, sVal)       # 주문조건코드 (0:없음, 1:IOC, 2:FOK)

        CLib.OpCommAPI_SetRqData(10, b"0")       # 프로그램호가신고구분 (0 고정)

        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
        iRtn = CLib.OpCommAPI_SendRq(self.Hwnd, RQRP_TRAN_STK_MDFY, 0)

        if iRtn < 0:
            sErrMsg = dic_sendrq_error.get(iRtn)
            sErrMsg = "정정취소 전송 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)

        return iRtn


    # 주식 매도/매수 주문 응답처리
    def RecvStkOrd(self, wParam, lParam, iRqRpID):
        print("recvestkord")
        sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 0, 0, 0)
        print(sVal)
        self.ui.TxtBrOrdNo.setText(sVal.decode("cp949"))


    # 주식 정정/취소 주문 응답처리
    def RecvStkMdfy(self, wParam, lParam, iRqRpID):
        sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 0, 0, 0)
        self.ui.TxtBrOrdNo_2.setText(sVal.decode("cp949"))

