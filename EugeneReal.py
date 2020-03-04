from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from EugeneHd import *
from EugeneLib import *

#실시간 시세 모듈
class EugeneReal(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow
        self.bReal = False

    # 실시간 주식시세 요청
    def ReqRealStkPrc(self):
        sCode = self.ui.EditCode.text()
        sCode = sCode.encode()

        # 표준종목코드로 변환하여 조회
        sStdCode = CLib.OpCodeAPI_GetExpCode(sCode)

        # 실시간 시세 수신중이면, 수신 해제처리
        if self.bReal == True:
            # 실시간 주식 우선호가 해제
            CLib.OpCommAPI_RequestReal(self.ui.winId(), False, REAL_TRAN_STK_PRC, sStdCode)

            # 실시간 주식 체결시세 해제
            CLib.OpCommAPI_RequestReal(self.ui.winId(), False, REAL_TRAN_STK_TICK, sStdCode)

            self.bReal = False
            self.ui.BtnPrc.setText("실시간 시세")

            sErrMsg = "실시간 시세 해제"
            self.ui.TxtBrLog.append(sErrMsg)
            return

        # 실시간 주식 우선호가 요청
        iRtn = CLib.OpCommAPI_RequestReal(self.ui.winId(), True, REAL_TRAN_STK_PRC, sStdCode)

        if iRtn < 0:
            sErrMsg = DIC_SETREAL_ERR.get(iRtn)
            sErrMsg = "우선호가 요청 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "우선호가 요청 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)

        # 실시간 주식 체결시세 요청
        iRtn = CLib.OpCommAPI_RequestReal(self.ui.winId(), True, REAL_TRAN_STK_TICK, sStdCode)

        if iRtn < 0:
            sErrMsg = DIC_SETREAL_ERR.get(iRtn)
            sErrMsg = "체결시세 요청 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            self.bReal = True
            self.ui.BtnPrc.setText("시세 중단")

            sErrMsg = "체결시세 요청 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)


    # 실시간 주식 우선호가 수신처리
    def RecvRealStkPrc(self, wParam, lParam):
        lstBuy  = []
        lstSell = []

        sVal = CLib.OpCommAPI_GetRealData(wParam, 30)  # 매도5호가변화량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 28)  # 매도5호가잔량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 26)  # 매도5호가
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 24)  # 매도4호가변화량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 22)  # 매도4호가잔량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 20)  # 매도4호가
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 18)  # 매도3호가변화량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 16)  # 매도3호가잔량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 14)  # 매도3호가
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 12)  # 매도2호가변화량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 10)  # 매도2호가잔량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  8)  # 매도2호가
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  6)  # 매도1호가변화량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  4)  # 매도1호가잔량
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  2)  # 매도1호가
        lstSell.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  3)  # 매수1호가
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  5)  # 매수1호가잔량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  7)  # 매수1호가변화량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  9)  # 매수2호가
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 11)  # 매수2호가잔량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 13)  # 매수2호가변화량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 15)  # 매수3호가
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 17)  # 매수3호가잔량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 19)  # 매수3호가변화량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 21)  # 매수4호가
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 23)  # 매수4호가잔량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 25)  # 매수4호가변화량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 27)  # 매수5호가
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 29)  # 매수5호가잔량
        lstBuy.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 31)  # 매수5호가변화량
        lstBuy.append(sVal.decode("cp949").strip())

        # 매도1~5호가 셋팅
        for i in range(0, 5):
            sVal = lstSell[i * 3]
            self.ui.TablePrc.setItem(i, 0, QTableWidgetItem(sVal))
            sVal = lstSell[(i * 3) + 1]
            self.ui.TablePrc.setItem(i, 1, QTableWidgetItem(sVal))
            sVal = lstSell[(i * 3) + 2]
            self.ui.TablePrc.setItem(i, 2, QTableWidgetItem(sVal))

            # 컬럼 정렬 셋팅
            self.ui.TablePrc.item(i, 0).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.ui.TablePrc.item(i, 1).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.ui.TablePrc.item(i, 2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)

            # 컬럼 색상 셋팅
            self.ui.TablePrc.item(i, 0).setBackground(QtGui.QColor(207, 229, 255))
            self.ui.TablePrc.item(i, 1).setBackground(QtGui.QColor(207, 229, 255))
            self.ui.TablePrc.item(i, 2).setBackground(QtGui.QColor(207, 229, 255))

        # 매수 1~5호가 셋팅
        for i in range(0, 5):
            sVal = lstBuy[i * 3]
            self.ui.TablePrc.setItem(i + 5, 2, QTableWidgetItem(sVal))
            sVal = lstBuy[(i * 3) + 1]
            self.ui.TablePrc.setItem(i + 5, 3, QTableWidgetItem(sVal))
            sVal = lstBuy[(i * 3) + 2]
            self.ui.TablePrc.setItem(i + 5, 4, QTableWidgetItem(sVal))

            # 컬럼 정렬 셋팅
            self.ui.TablePrc.item(i + 5, 2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.ui.TablePrc.item(i + 5, 3).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.ui.TablePrc.item(i + 5, 4).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)

            # 컬럼 색상 셋팅
            self.ui.TablePrc.item(i + 5, 2).setBackground(QtGui.QColor(255, 221, 207))
            self.ui.TablePrc.item(i + 5, 3).setBackground(QtGui.QColor(255, 221, 207))
            self.ui.TablePrc.item(i + 5, 4).setBackground(QtGui.QColor(255, 221, 207))


    # 실시간 주식 체결시세 수신처리
    def RecvRealStkTick(self, wParam, lParam):
        lstTick = []
        sVal = CLib.OpCommAPI_GetRealData(wParam,  1)  # 체결시각
        sVal = sVal.decode("cp949").strip()
        sVal = sVal[0:2] + ":" + sVal[2:4] + ":" + sVal[4:6]
        lstTick.append(sVal)

        sVal = CLib.OpCommAPI_GetRealData(wParam,  4)  # 체결가
        lstTick.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam,  2)  # 전일대비
        sVal = sVal.decode("cp949").strip()
        sVal = "%+0d" % int(sVal)
        lstTick.append(sVal)

        sVal = CLib.OpCommAPI_GetRealData(wParam, 14)  # 체결량
        lstTick.append(sVal.decode("cp949").strip())

        sVal = CLib.OpCommAPI_GetRealData(wParam, 29)  # 체결강도
        sVal = sVal.decode("cp949").strip()
        sVal = "%0.2f" % (float(sVal) / 100)
        lstTick.append(sVal + "%")

        MAX_ROW = 20
        iRow = self.ui.TableTrd.rowCount()

        # 체결시세 row가 MAX_ROW를 넘으면 삭제
        if (iRow >= MAX_ROW):
            self.ui.TableTick.removeRow(MAX_ROW)

        self.ui.TableTick.insertRow(0)
        self.ui.TableTick.setRowHeight(0, 20)

        for i in range(len(lstTick)):
            self.ui.TableTick.setItem(0, i, QTableWidgetItem(lstTick[i]))

        # 컬럼 정렬 셋팅
        self.ui.TableTick.item(0, 0).setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.ui.TableTick.item(0, 1).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.ui.TableTick.item(0, 2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.ui.TableTick.item(0, 3).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.ui.TableTick.item(0, 4).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
