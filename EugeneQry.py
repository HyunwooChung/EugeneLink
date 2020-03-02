import win32ui
from PyQt5.QtWidgets import *
from EugeneHd import *
from EugeneLib import *

# RQRP 조회 모듈
class EugeneQry(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    # 주식 주문/체결 조회 요청
    def QueryStkTrd(self):
        sVal = self.ui.EditAcno.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 0, sVal)       # 계좌번호

        sVal = self.ui.EditPswd.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 1, sVal)       # 비밀번호

        CLib.OpCommAPI_SetRqData( 2, b"")        # 주문번호 (NULL 전체주문)
        CLib.OpCommAPI_SetRqData( 3, b"%")       # 매도매수구분 (% 전체, 10 매도, 20 매수)
        CLib.OpCommAPI_SetRqData( 4, b"%")       # 종목코드 (% 전체)
        CLib.OpCommAPI_SetRqData( 5, b"2")       # 정렬구분 (1 정순, 2 역순)
        CLib.OpCommAPI_SetRqData( 6, b"01")      # 체결구분 (01 전체, 02 미체결)
        CLib.OpCommAPI_SetRqData( 7, b"0")       # 조회구분 (0 고정)

        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()
        iRtn = CLib.OpCommAPI_SendRq(self.Hwnd, RQRP_TRAN_STK_TRD, 0)

        if iRtn < 0:
            sErrMsg = dic_sendrq_error.get(iRtn)
            sErrMsg = "주식주문 조회 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "주식주문 조회 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)

        return iRtn


    # 주식 주문/체결 조회 응답 처리
    def RecvStkTrd(self, wParam, lParam, iRqRpID):
        iCnt = CLib.OpCommAPI_GetRqrpCount(iRqRpID, 1)
        sMsg = "주식주문 조회 건수 : " + str(iCnt)
        self.ui.TxtBrLog.append(sMsg)

        for i in range(iCnt):
            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 4)      # 주문번호
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 0, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 5)      # 원주문번호
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 1, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 6)      # 종목코드
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 2, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 7)      # 종목명
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 3, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 8)      # 정정취소구분
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 4, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 9)      # 매매구분
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 5, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 11)     # 주문수량
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 6, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 12)     # 주문가격
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 7, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 13)     # 미체결잔량
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 8, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 14)     # 체결수량
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 9, QTableWidgetItem(value))

            value = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 32)     # 체결평균단가
            value = value.decode("cp949")
            self.ui.TableTrd.setItem(i, 10, QTableWidgetItem(value))


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
        CLib.OpCommAPI_SetRqData( 4, b"N")       # 수수료포함여부 (Y 수수료 포함, N 수수료 포함 안함)
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
        print(iRqRpID)
        iCnt = CLib.OpCommAPI_GetRqrpCount(iRqRpID, 1)
        sMsg = "주식잔고 조회 건수 : " + str(iCnt)
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
