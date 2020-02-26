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

# OpCommAPI_SendRq return Value
SENDRQ_NOT_INITIALIZE      = -99      # Initialize 하지 않음.
SENDRQ_INVALID_RQRPID      = -21      # 존재하지 않는 RQRPID
SENDRQ_RQDATA_LACK         = -22      # RQ데이터 부족
SENDRQ_NOT_SUPPORT         = -23      # 지원하는 않는 RQ. Multi Type Input은 지원하지 않음.
SENDRQ_MEMORY_LACK         = -24      # 메모리 부족
SENDRQ_INVALID_ACCNO       = -25      # 조회 불가능한 계좌번호
SENDRQ_SEND_LIMIT          = -26      # 초당 전송 횟수 제한
SENDRQ_SYNC_RPWAITING      = -27      # 동기식 TR로 전송 제한
SENDRQ_INVALID_CONKEY      = -28      # 존재하지 않는 연속키값이거나 연속조회가 불가능한 TR
SENDRQ_ERROR_SOCKET        =  -1      # 소켓송신 에러
SENDRQ_ERROR_NOTCONNECT    =  -2      # 통신 미연결 상태
SENDRQ_ERROR_ALLOCMEM      =  -3      # 메모리 에러
SENDRQ_ERROR_FORMAT        =  -4      # 통신규약 에러
SENDRQ_ERROR_DOWNLOAD      =  -5      # 다운로드 상태
SENDRQ_CERT_NOTDEFINE      =  -6      # 인증서 미정의
SENDRQ_LOGIN_NOTUNSERINFO  =  -7      # 유저정보 없음
SENDRQ_LOGIN_FAIL          =  -8      # 승인처리 실패
SENDRQ_SENDLEN_OVER        =  -9      # 데이터 전문길이 초과
SENDRQ_ERROR_NOTCOMPLETE   = -16      # 데이터 조회중 오류
SENDRQ_CERT_NOTCOMPLETE    = -17      # 인증서 오류