from ctypes import *

class EugeneLib():
    def __init__(self):
        pass

    # 유진챔피언링크에서 제공하는 Library 로드 및 함수 정의
    def LoadLib(self):
        OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')
        OpCodeAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCodeAPI.dll')

        self.OpCommAPI_Initialize = OpCommAPI.OpCommAPI_Initialize
        self.OpCommAPI_Initialize.restype = c_bool
        self.OpCommAPI_Initialize.argtypes = [c_int]

        self.OpCommAPI_UnInitialize = OpCommAPI.OpCommAPI_UnInitialize
        self.OpCommAPI_UnInitialize.restype = c_bool
        self.OpCommAPI_UnInitialize.argtypes = []

        # 조회 데이터
        self.OpCommAPI_SetRqData = OpCommAPI.OpCommAPI_SetRQData
        self.OpCommAPI_SetRqData.restype = c_void_p
        self.OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

        self.OpCommAPI_SendRq = OpCommAPI.OpCommAPI_SendRq
        self.OpCommAPI_SendRq.restype = c_int
        self.OpCommAPI_SendRq.argtypes = [c_int, c_int, c_int]

        self.OpCommAPI_ClearRQData = OpCommAPI.OpCommAPI_ClearRQData
        self.OpCommAPI_ClearRQData.restype = c_void_p
        self.OpCommAPI_ClearRQData.argtypes = []

        self.OpCodeAPI_GetExpCode = OpCodeAPI.OpCodeAPI_GetExpCode
        self.OpCodeAPI_GetExpCode.restype = c_char_p
        self.OpCodeAPI_GetExpCode.argtypes = [c_char_p]

        self.OpCommAPI_GetRqrpData = OpCommAPI.OpCommAPI_GetRqrpData
        self.OpCommAPI_GetRqrpData.restype = c_char_p
        self.OpCommAPI_GetRqrpData.argtypes = [c_int, c_int, c_int, c_int]

        self.OpCommAPI_GetRqrpCount = OpCommAPI.OpCommAPI_GetRqrpCount
        self.OpCommAPI_GetRqrpCount.restype = c_int
        self.OpCommAPI_GetRqrpCount.argtypes = [c_int, c_int]

        # 실시간 데이터
        self.OpCommAPI_RequestReal = OpCommAPI.OpCommAPI_RequestReal
        self.OpCommAPI_RequestReal.restype = c_int
        self.OpCommAPI_RequestReal.argtypes = [c_int, c_bool, c_byte, c_char_p]

        self.OpCommAPI_UnRegisterRealAll = OpCommAPI.OpCommAPI_UnRegisterRealAll
        self.OpCommAPI_UnRegisterRealAll.restype = c_void_p
        self.OpCommAPI_UnRegisterRealAll.argtypes = [c_int]

        self.OpCommAPI_GetRealData = OpCommAPI.OpCommAPI_GetRealData
        self.OpCommAPI_GetRealData.restype = c_char_p
        self.OpCommAPI_GetRealData.argtypes = [c_byte, c_int]

        # 종목코드 관련 데이터
        self.OpCodeAPI_GetExpCode = OpCodeAPI.OpCodeAPI_GetExpCode
        self.OpCodeAPI_GetExpCode.restype = c_char_p
        self.OpCodeAPI_GetExpCode.argtypes = [c_char_p]

        self.OpCodeAPI_GetNameByCode = OpCodeAPI.OpCodeAPI_GetNameByCode
        self.OpCodeAPI_GetNameByCode.restype = c_char_p
        self.OpCodeAPI_GetNameByCode.argtypes = [c_char_p]