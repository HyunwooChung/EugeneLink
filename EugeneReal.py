import win32ui
from PyQt5.QtWidgets import *
from EugeneHd import *
from EugeneLib import *

#실시간 시세 모듈
class EugeneReal(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    # 실시간 주식시세 요청
    def ReqRealStkPrc(self):
        sCode = self.ui.EditCode.text()
        sCode = sCode.encode()

        # 표준종목코드로 변환하여 조회
        sStdCode = CLib.OpCodeAPI_GetExpCode(sCode)

        self.Hwnd = win32ui.FindWindow(None, "MainWindow").GetSafeHwnd()

        # 주식 우선호가 요청
        iRtn = CLib.OpCommAPI_RequestReal(self.Hwnd, True, REAL_TRAN_STK_PRC, sStdCode)

        if iRtn < 0:
            sErrMsg = dic_setreal_error.get(iRtn)
            sErrMsg = "우선호가 요청 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "우선호가 요청 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)

        # 주식 체결시세 요청
        iRtn = CLib.OpCommAPI_RequestReal(self.Hwnd, True, REAL_TRAN_STK_TRD, sStdCode)

        if iRtn < 0:
            sErrMsg = dic_setreal_error.get(iRtn)
            sErrMsg = "체결시세 요청 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "체결시세 요청 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)


    # 실시간 주식 우선호가 수신처리
    def RecvRealStkPrc(self, wParam, lParam):
        lstBuy  = []
        lstSell = []

        sVal = CLib.OpCommAPI_GetRealData(wParam, 30)  # 매도5호가변화량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 28)  # 매도5호가잔량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 26)  # 매도5호가
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 24)  # 매도4호가변화량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 22)  # 매도4호가잔량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 20)  # 매도4호가
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 18)  # 매도3호가변화량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 16)  # 매도3호가잔량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 14)  # 매도3호가
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 12)  # 매도2호가변화량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 10)  # 매도2호가잔량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  8)  # 매도2호가
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  6)  # 매도1호가변화량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  4)  # 매도1호가잔량
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  2)  # 매도1호가
        lstSell.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  3)  # 매수1호가
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  5)  # 매수1호가잔량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  7)  # 매수1호가변화량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  9)  # 매수2호가
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 11)  # 매수2호가잔량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 13)  # 매수2호가변화량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 15)  # 매수3호가
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 17)  # 매수3호가잔량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 19)  # 매수3호가변화량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 21)  # 매수4호가
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 23)  # 매수4호가잔량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 25)  # 매수4호가변화량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 27)  # 매수5호가
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 29)  # 매수5호가잔량
        lstBuy.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 31)  # 매수5호가변화량
        lstBuy.append(sVal.decode("cp949"))

        # 매도1~5호가 셋팅
        for i in range(0, 5):
            sVal = lstSell[i * 3]
            self.ui.TablePrc.setItem(i, 0, QTableWidgetItem(sVal))
            sVal = lstSell[(i * 3) + 1]
            self.ui.TablePrc.setItem(i, 1, QTableWidgetItem(sVal))
            sVal = lstSell[(i * 3) + 2]
            self.ui.TablePrc.setItem(i, 2, QTableWidgetItem(sVal))

        # 매수 1~5호가 셋팅
        for i in range(0, 5):
            sVal = lstBuy[i * 3]
            self.ui.TablePrc.setItem(i + 5, 2, QTableWidgetItem(sVal))
            sVal = lstBuy[(i * 3) + 1]
            self.ui.TablePrc.setItem(i + 5, 3, QTableWidgetItem(sVal))
            sVal = lstBuy[(i * 3) + 2]
            self.ui.TablePrc.setItem(i + 5, 4, QTableWidgetItem(sVal))

    # 실시간 주식 체결시세 수신처리
    def RecvRealStkTrd(self, wParam, lParam):
        lstTrd = []
        sVal = CLib.OpCommAPI_GetRealData(wParam,  1)  # 체결시각
        lstTrd.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  4)  # 체결가
        lstTrd.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam,  2)  # 전일대비
        lstTrd.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 14)  # 체결량
        lstTrd.append(sVal.decode("cp949"))

        sVal = CLib.OpCommAPI_GetRealData(wParam, 15)  # 누적거래량
        lstTrd.append(sVal.decode("cp949"))

        MAX_ROW = 20
        iRow = self.ui.TableTrd.rowCount()

        # 체결시세 row가 MAX_ROW를 넘으면 삭제
        if (iRow >= MAX_ROW):
            self.ui.TableTrd.removeRow(MAX_ROW)

        self.ui.TableTrd.insertRow(0)

        for i in range(len(lstTrd)):
            self.ui.TableTrd.setItem(0, i, QTableWidgetItem(lstTrd[i]))



