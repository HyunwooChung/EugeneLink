# 유진투자증권 챔피언 링크 - 파이썬 샘플소스
유진투자증권 챔피언 링크 API를 이용하여 주문, 조회, 시세 처리를 할 수 있는 기본 샘플소스입니다.
## 개발환경
* Anaconda 3 (32bit)
* Pycharm 2018.3.7 (32bit) - 이후 버전은 32bit 설치 불가
* PyQt5
* Qt Designer 5.9.7
* 유진투자증권 챔피언 링크 API (32bit)

## 파일설명
* EugeneMain.py
  * 윈도우 이벤트 수신처리
  * 윈도우 폼 셋팅, 윈도우 컨트롤 셋팅
* EugeneHd.py
  * 윈도우 메시지, 오류 메시지, TRAN ID, 구분값 정의  
* EugeneLib.py
  * 유진투자증권 챔피언 링크 API 함수정의
* EugeneOrd.py
  * 주식 매도/매수 주문, 정정/취소 주문 전송처리
* EugeneQry.py
  * 주식 주문/체결내역, 주식 잔고내역 조회요청 및 수신처리
* EugeneReal.py
  * 주식 호가시세, 체결시세 요청 및 실시간 수신처리
* EugeneWindow.ui
  * 화면 UI (Qt Designer 사용)

## 유의사항
* 챔피언 링크 설치 폴더에 개발한 프로그램의 exe 파일이 있어야 됨.  
  챔피언 링크 실행 후 설정에서 개발 프로그램의 exe 파일을 등록하면 로그인시 개발 프로그램을 실행시킴.
* 유진투자증권에서 제공하는 API (OpCodeAPI.dll, OpCommAPI.dll) 2개만 가지고는 실행시 오류 발생.  
  2개의 dll이 챔피언 링크의 다른 dll 파일을 참조하기 때문  
  유진투자증권 챔피언 링크 설치 폴더(C:\EugeneFN\NewChampionLink)에 있는 모든 dll을 개발 폴더에 복사하거나,  
  챔피언 링크 설치폴더에 파이썬 소스파일을 만들어서 실행 해야됨.
* 테스트 로그인 비밀번호, 계좌번호의 비밀번호는 1357

## 자주하는 질문
* 이슈 링크 : <https://github.com/HyunwooChung/EugeneLink/issues/1>
  
## 참조
* 해당 소스는 깃허브에 업로드 되어 있습니다.
* 깃허브 링크 : <https://github.com/HyunwooChung/EugeneLink/>
