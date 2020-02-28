from EugeneMain import *

class EugeneOrd(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    # 주식 매도/매수 주문 전송처리
    def SendStkOrd(self, sOrdTp):

        sAcno = self.ui.EditAcno.text()
        sAcno = sAcno.encode()
        EugeneLib.OpCommAPI_SetRqData( 0, sAcno)      # 계좌번호

        sPswd = self.ui.EditAcno.text()
        sPswd = sPswd.encode()
        EugeneLib.OpCommAPI_SetRqData( 1, sPswd)      # 비밀번호

        sCode = self.ui.EditCode.text()
        sCode = sCode.encode()
        # 표준종목코드로 변환하여 전송
        sStdCode = EugeneLib.OpCodeAPI_GetExpCode(sCode)
        EugeneLib.OpCommAPI_SetRqData( 2, sStdCode)   # 종목코드

        EugeneLib.OpCommAPI_SetRqData( 3, sPswd)      # 주문수량
        EugeneLib.OpCommAPI_SetRqData( 4, sAccn)      # 주문가격
        EugeneLib.OpCommAPI_SetRqData( 5, sOrdTp)     # 매도매수구분
        EugeneLib.OpCommAPI_SetRqData( 6, sPswd)      # 매매구분코드
        EugeneLib.OpCommAPI_SetRqData( 7, "010")      # 신용거래구분 (010 고정)
        EugeneLib.OpCommAPI_SetRqData( 9, "N")        # 담보대출주문여부 (N 고정)
        EugeneLib.OpCommAPI_SetRqData(10, sPswd)      # 주문조건코드
        EugeneLib.OpCommAPI_SetRqData(11, "010")      # 프로그램호가구분 (010 고정)
        EugeneLib.OpCommAPI_SetRqData(12, "0")        # 프로그램호가신고구분 (0 고정)
        EugeneLib.OpCommAPI_SetRqData(13, "N")        # 선물대용여부 (N 고정)
        EugeneLib.OpCommAPI_SetRqData(14, "000")      # 반대매매상환구분 (000 고정)
        EugeneLib.OpCommAPI_SetRqData(18, "N")        # 보류대상주문확인여부 (N 고정)
        EugeneLib.OpCommAPI_SetRqData(22, "N")        # 공매도가능여부 (N 고정)
        EugeneLib.OpCommAPI_SetRqData(23, "00")       # 공매도구분 (00 고정)

        iRtn = EugeneLib.OpCommAPI_SendRq(self.window_handle, RQRP_TRAN_ORD, 0)
        return iRtn


    # 주식 정정/취소 주문 전송처리
    def SendStkMdfy(self, sOrdTp):
        pass


