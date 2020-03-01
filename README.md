# 유진투자증권 챔피언 링크 - 파이썬 샘플소스

## 개발환경
* Anaconda 3 (32bit)
* Pycharm 2018.3.7 (32bit) - 이후 버전은 32bit 설치 불가
* PyQt5

## 파일설명
* EugeneMain.py
* EugeneHd.py
* EugeneLib.py
* EugeneOrd.py
* EugeneQry.py
* EugeneReal.py
* EugeneWindow.ui

## 주의사항
* 유진투자증권에서 제공하는 API(OpCodeAPI.dll, OpCommAPI.dll) 2개만 가지고는 실행시 오류 발생  
  2개의 API가 다른 챔피언 링크의 dll 파일을 참조하기 때문
* 유진투자증권 챔피언 링크 설치 폴더(C:\EugeneFN\NewChampionLink)에 있는 모든 dll을 프로젝트 폴더에 카피하거나,  
  챔피언 링크 설치폴더에 파이썬 소스파일을 만들어서 컴파일 해야됨
