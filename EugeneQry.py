import win32ui
from PyQt5.QtWidgets import *
from EugeneHd import *
from EugeneLib import *

# RQRP 조회 모듈
class EugeneQry(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    # 주식잔고 조회 요청
    def QueryStkPstn(self):
        CLib.OpCommAPI_SetRqData( 0, b"1")       # 조회구분 (1 고정)

        sVal = self.ui.EditAcno.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 1, sVal)       # 계좌번호

        sVal = self.ui.EditPswd.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 2, sVal)       # 비밀번호

        CLib.OpCommAPI_SetRqData( 3, b"040")     # 주문매체구분 (040 고정)
        CLib.OpCommAPI_SetRqData( 4, b"N")       # 수수료포함여부 (N 수수료 포함 안함)
        CLib.OpCommAPI_SetRqData( 5, b"N")       # 현재가반영여부 (N 고정)

        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
        iRtn = CLib.OpCommAPI_SendRq(self.Hwnd, RQRP_TRAN_STK_PSTN, 0)

        if iRtn < 0:
            sErrMsg = dic_sendrq_error.get(iRtn)
            sErrMsg = "주식잔고 조회 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "주식잔고 조회 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)

        return iRtn

    # 주식잔고 조회 응답 처리
    def RecvStkPstn(self, wParam, lParam, iRqRpID):
        iCnt = CLib.OpCommAPI_GetRqrpCount(iRqRpID, 1)
        sMsg = "주식잔고조회 건수 : " + str(iCnt)
        self.ui.TxtBrLog.append(sMsg)

        for i in range(iCnt):
            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 0)      # 종목코드
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 0, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 1)      # 종목명
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 1, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 6)      # 잔고수량
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 2, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 9)      # 금일매수수량
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 3, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 10)     # 금일매도수량
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 4, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 11)     # 매입단가
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 5, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 12)     # 매입금액
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 6, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 22)     # 평가금액
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 7, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 23)     # 평가손익
            value = value.decode("cp949")
            self.ui.TablePstn.setItem(i, 8, QTableWidgetItem(value))

        CLib.OpCommAPI_ClearRQData()