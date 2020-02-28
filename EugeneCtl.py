from EugeneMain import *

class EugeneCtl(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    def BtnPstnClick(self):
        iErr = EugeneLib.OpCommAPI_UnInitialize()
        print(iErr)
        pass

    def BtnSiseClick(self):
        sAccn = '27122016751'
        sPswd = '1357'
        sAccn = sAccn.encode()
        sPswd = sPswd.encode()
        print('111')


        EugeneLib.OpCommAPI_SetRqData(0, sAccn)
        print('222')
        EugeneLib.OpCommAPI_SetRqData(1, sPswd)
        print('333')

        handler = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        result_753 = EugeneLib.OpCommAPI_SendRq(handler, 753, 0)
        print('444')

        msg = 'SendRq 753 : ' + str(result_753)
        print(msg)

    def BtnBuyClick(self):
        pass

    def BtnSellClick(self):
        pass

    def BtnMdfyClick(self):
        pass

    def BtnCnclClick(self):
        pass