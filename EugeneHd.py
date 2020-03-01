# OpCommAPI_Initialize 함수 호출시 Starter 화면에 보내는 메세지
WM_EU_STARTER_CLOSE  = 7417 # WM_USER+6393

# 리얼 데이터 수신시 메세지
# afx_msg long WM_EU_REAL_RECV(nRealID, sRealCode);
# nRealID    : 수신한 리얼 데이터 ID
# RealCode  : 수신한 리얼 데이터의 종목 코드
WM_EU_REAL_RECV      = 7418 # WM_USER+6394

# 조회 데이터 수신시 메세지
# afx_msg long WM_EU_RQRP_RECV(nRqRpSeqID, bContinue);
# nRqRpSeqID : 수신한 조회 데이터 유일 Key 값 (OpCommAPI_SendRq return value)
# bContinue  : 다음 데이터 존재 여부
WM_EU_RQRP_RECV      = 7419 #WM_USER+6395

# 조회 데이터 서버 오류 발생시 메세지
# afx_msg long WM_EU_REAL_RECV(nRqRpSeqID, sErrMsg);
# nRqRpSeqID : 수신한 조회 데이터 유일 Key 값 (OpCommAPI_SendRq return value)
# sErrMsg    : 서버 오류 메세지
WM_EU_RQRP_ERR_RECV	 = 7420 #WM_USER+6396

# 소켓이나 기타 공지 사항 수신시
# afx_msg long WM_EU_REAL_RECV(NOTIID, sNotiMsg);
# NOTIID     : 공지사항 종류
# sNotiMsg   : 공지사항 메세지(NOTI_SERVER_NOTIFY 일때만 유효한 값)
WM_EU_NOTI_RECV	     = 7421 #WM_USER+6397

# WM_EU_NOTI_RECV Notify Value
dic_noti_error = \
    {  50 :  "다중접속에 의한 접속 해제"
    ,  51 :  "통신 단절"
    , 100 :  "서버에서 내려온 긴급 메세지"
    }

# OpCommAPI_SendRq return Value
dic_sendrq_error = \
    { -99 :  "Initialize 하지 않음"
    , -21 :  "존재하지 않는 RQRPID"
    , -22 :  "RQ데이터 부족"
    , -23 :  "지원하는 않는 RQ Multi Type Input은 지원하지 않음"
    , -24 :  "메모리 부족"
    , -25 :  "조회 불가능한 계좌번호"
    , -26 :  "초당 전송 횟수 제한"
    , -27 :  "동기식 TR로 전송 제한"
    , -28 :  "존재하지 않는 연속키값이거나 연속조회가 불가능한 TR"
    ,  -1 :  "소켓송신 에러"
    ,  -2 :  "통신 미연결 상태"
    ,  -3 :  "메모리 에러"
    ,  -4 :  "통신규약 에러"
    ,  -5 :  "다운로드 상태"
    ,  -6 :  "인증서 미정의"
    ,  -7 :  "유저정보 없음"
    ,  -8 :  "승인처리 실패"
    ,  -9 :  "데이터 전문길이 초과"
    , -16 :  "데이터 조회중 오류"
    , -17 :  "인증서 오류" }

# OpCommAPI_RequestReal return Value
dic_setreal_error = \
    { -99 :  "Initialize 하지 않음"
    ,  -1 :  "주문체결통보 설정시 본인 ID가 아님"
    }

# REAL TRAN
REAL_TRAN_STK_PRC          =   1      # 주식 종목 우선호가
REAL_TRAN_STK_TRD          =  21      # 주식 종목 체결시세
REAL_TRAN_STK_ORD          = 191      # 주식 주문/체결 통보

# RQRP TRAN
RQRP_TRAN_STK_ORD          = 601      # 주식 매도/매수 주문
RQRP_TRAN_STK_MDFY         = 602      # 주식 정정/취소 주문
RQRP_TRAN_STK_PSTN         = 655      # 주식 잔고 조회


HWND = 0