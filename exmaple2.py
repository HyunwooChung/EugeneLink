import sys
import time
from ctypes import *
from ctypes.wintypes import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32ui, win32gui
from ctypes.wintypes import HWND
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(393, 284)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 0, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 30, 351, 201))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 393, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.ButtonClick)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))


    def ButtonClick(self):
        self.textBrowser.append('Process Start 333')
        window_handle = win32ui.FindWindow(None, u"MainWindow").GetSafeHwnd()
        msg = "Handle : "+ str(window_handle)
        self.textBrowser.append(msg)

        OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')

        OpCommAPI_Initialize = OpCommAPI['OpCommAPI_Initialize']
        OpCommAPI_Initialize.restype = c_bool
        OpCommAPI_Initialize.argtypes = [c_int]

        OpCommAPI_SetRqData = OpCommAPI['OpCommAPI_SetRQData']
        OpCommAPI_SetRqData.restype = c_void_p
        OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

        OpCommAPI_SendRq = OpCommAPI['OpCommAPI_SendRq']
        OpCommAPI_SendRq.restype = c_int
        OpCommAPI_SendRq.argtypes = (c_int, c_int, c_int)

        err = OpCommAPI_Initialize(window_handle)
        if err == 0 :
            self.textBrowser.append('Initialize : 실패')
        else:
            self.textBrowser.append('Initialize : 성공')

        sAccn = b'27122016751'
        sPswd = b'1357'

        OpCommAPI_SetRqData(0, sAccn)
        OpCommAPI_SetRqData(1, sPswd)

        msg = '계좌번호 : ' + str(sAccn)
        self.textBrowser.append(msg)

        result = OpCommAPI_SendRq(window_handle, 753, 0)

        msg = '753 호출 : ' + str(result)
        self.textBrowser.append(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    myApp = Ui_MainWindow()
    myApp.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()