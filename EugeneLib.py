from ctypes import *

# 유진 Library Load 모듈
class EugeneLib(object):
    OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')
    OpCodeAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCodeAPI.dll')

    # 초기화
    OpCommAPI_Initialize = OpCommAPI.OpCommAPI_Initialize
    OpCommAPI_Initialize.restype = c_bool
    OpCommAPI_Initialize.argtypes = [c_int]

    OpCommAPI_UnInitialize = OpCommAPI.OpCommAPI_UnInitialize
    OpCommAPI_UnInitialize.restype = c_bool
    OpCommAPI_UnInitialize.argtypes = []

    # 조회 데이터
    OpCommAPI_SetRqData = OpCommAPI.OpCommAPI_SetRQData
    OpCommAPI_SetRqData.restype = c_void_p
    OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

    OpCommAPI_SendRq = OpCommAPI.OpCommAPI_SendRq
    OpCommAPI_SendRq.restype = c_int
    OpCommAPI_SendRq.argtypes = [c_int, c_int, c_int]

    OpCommAPI_ClearRQData = OpCommAPI.OpCommAPI_ClearRQData
    OpCommAPI_ClearRQData.restype = c_void_p
    OpCommAPI_ClearRQData.argtypes = []

    OpCommAPI_GetRqrpData = OpCommAPI.OpCommAPI_GetRqrpData
    OpCommAPI_GetRqrpData.restype = c_char_p
    OpCommAPI_GetRqrpData.argtypes = [c_int, c_int, c_int, c_int]

    OpCommAPI_GetRqrpCount = OpCommAPI.OpCommAPI_GetRqrpCount
    OpCommAPI_GetRqrpCount.restype = c_int
    OpCommAPI_GetRqrpCount.argtypes = [c_int, c_int]

    # 실시간 데이터
    OpCommAPI_RequestReal = OpCommAPI.OpCommAPI_RequestReal
    OpCommAPI_RequestReal.restype = c_int
    OpCommAPI_RequestReal.argtypes = [c_int, c_bool, c_byte, c_char_p]

    OpCommAPI_UnRegisterRealAll = OpCommAPI.OpCommAPI_UnRegisterRealAll
    OpCommAPI_UnRegisterRealAll.restype = c_void_p
    OpCommAPI_UnRegisterRealAll.argtypes = [c_int]

    OpCommAPI_GetRealData = OpCommAPI.OpCommAPI_GetRealData
    OpCommAPI_GetRealData.restype = c_char_p
    OpCommAPI_GetRealData.argtypes = [c_byte, c_int]

    # 종목코드 관련 데이터
    OpCodeAPI_GetExpCode = OpCodeAPI.OpCodeAPI_GetExpCode
    OpCodeAPI_GetExpCode.restype = c_char_p
    OpCodeAPI_GetExpCode.argtypes = [c_char_p]

    OpCodeAPI_GetNameByCode = OpCodeAPI.OpCodeAPI_GetNameByCode
    OpCodeAPI_GetNameByCode.restype = c_char_p
    OpCodeAPI_GetNameByCode.argtypes = [c_char_p]

CLib = EugeneLib()
