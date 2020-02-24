#OpCommAPI_Initialize 함수 호출시 Starter 화면에 보내는 메세지
WM_EU_STARTER_CLOSE  = 7417 # WM_USER+6393

#리얼 데이터 수신시 메세지
#afx_msg long WM_EU_REAL_RECV(nRealID, sRealCode);
#nRealID    : 수신한 리얼 데이터 ID
#sRealCode  : 수신한 리얼 데이터의 종목 코드
WM_EU_REAL_RECV      = 7418 # WM_USER+6394

#조회 데이터 수신시 메세지
#afx_msg long WM_EU_RQRP_RECV(nRqRpSeqID, bContinue);
#nRqRpSeqID : 수신한 조회 데이터 유일 Key 값 (OpCommAPI_SendRq return value)
#bContinue  : 다음 데이터 존재 여부
WM_EU_RQRP_RECV      = 7419 #WM_USER+6395


#조회 데이터 서버 오류 발생시 메세지
#afx_msg long WM_EU_REAL_RECV(nRqRpSeqID, sErrMsg);
#nRqRpSeqID : 수신한 조회 데이터 유일 Key 값 (OpCommAPI_SendRq return value)
#sErrMsg    : 서버 오류 메세지
WM_EU_RQRP_ERR_RECV	 = 7420 #WM_USER+6396

#소켓이나 기타 공지 사항 수신시
#afx_msg long WM_EU_REAL_RECV(NOTIID, sNotiMsg);
#NOTIID     : 공지사항 종류
#sNotiMsg   : 공지사항 메세지(NOTI_SERVER_NOTIFY 일때만 유효한 값)
WM_EU_NOTI_RECV	     = 7421 #WM_USER+6397