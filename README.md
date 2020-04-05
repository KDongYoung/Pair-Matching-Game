# Pair-Matching-Game
Basic Pair Matching game + can find the rank of the game result (found by server connection))

------------------------------
[ 실행 환경 ] 
1. SQlite를 다운 받은 뒤, C드라이브에 ‘sqlite’라는 이름으로 저장한다.
2. ‘1. 데이터베이스 생성’ 코드를 실행한다. (pairgameDB 데이터베이스 생성, pairgame table 생성)
<div>
  <img src="https://user-images.githubusercontent.com/37610908/78502157-8cda3100-779a-11ea-81ac-abc1b0033630.jpg" width="150%"></img>
</div>

3. ‘2_1. client’ 파일에 약 403번째 줄에 host변수에 메인 server로 사용하고자 하는 컴퓨터(데이터베이스를 생성한 컴퓨터)의 ip값을 입력한다. 
<div>
  <img src="https://user-images.githubusercontent.com/37610908/78502155-8b106d80-779a-11ea-8f71-4c0027f8f3be.jpg" width="80%" height="60%"></img>
</div>

4. ‘2_1. server’파일을 실행한다.
5. ‘2_2. client’ 파일을 실행하여 게임을 한다.
------------------------------
[ 사용한 모듈 ] 

GUI용 : tkinter, threading, random
Server, client용 : sys, socket, threading
<div>
  <img src="https://user-images.githubusercontent.com/37610908/78502158-8d72c780-779a-11ea-901a-bfd5bcb3e97d.jpg" width="30%"></img>
  <img src="https://user-images.githubusercontent.com/37610908/78502159-8e0b5e00-779a-11ea-8a8b-eb63b7bac958.jpg" width="30%"></img>
</div>
