#!/usr/bin/env python
# coding: utf-8

# # 연속으로 3번 게임하기

import sys
from socket import *
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
from threading import Timer 

class cards:
    def __init__(self,level):
        self.level=level
        self.size=level**2
    
    def name(self):
        self.picname=[]
        file = open("picture.txt","r")
        line = file.read()
        name = line.split("\n")
        for part in name:
            self.picname.append(part)
        file.close()

    # 난이도에 따라 카드 선택 및 순서 섞기
    def shuffle(self):
        self.numpic=int(self.level**2/2)
        self.totalpic=self.picname[:self.numpic]*2
        random.shuffle(self.totalpic) # 원본 데이터 순서 change
    
    def createDeck(self):    
        self.deck=[]
        for c in self.totalpic:
            self.deck.append(card(c,False))

class card:
    def __init__(self,name,show):
        self.show=show # 카드 뒤집힘 여부
        self.name=name
        
    def __str__(self):
        if self.show == True:
            return self.name
        else:
            return 'card.gif'

class main:
    def __init__(self,window):        
        self.window = window
        self.window.title("카드 짝 맞추기 게임")
        self.window.resizable(False,False)  

        self.database()
        
    def gamestart(self):
        self.f.pack_forget()
        self.f1=Frame(self.window,height=80,bg="white")
        self.f1.pack()
        self.f1_2=Frame(self.window)
        self.f1_2.pack()
        self.f3=Frame(self.window)
        self.f3.pack()
        self.f4=Frame(self.window,height=50)
        self.f4.pack()  
        
        self.l1=Label(self.f1, text="누가누가 더 빨리 맞추나~ 짝 맞추기 게임\nPLAYER: "+self.d1+" ",font=("맑은 고딕",15),fg="white",bg="black")
        self.l1.pack(expand=True)
        
        self.varRadio=1
        self.startBtn=Button(self.f3,text="게임 시작", font=("맑은 고딕",12,"bold"),fg="blue",command=self.start,bg="white")
        self.startBtn.pack(side="right")
    
        self.l2=Label(self.f1,text=None,font=("Malgun Gothic",13,"bold"),fg="deep pink",bg="white")
        self.l2.pack(expand=True)
        
    def start(self):
        self.startBtn.pack_forget()
        
        self.lev={1:"하",2:"중",3:"상"}
        self.l2.config(text="Level"+str(self.varRadio)+" 난이도 "+self.lev[self.varRadio]+ " ["+str(self.varRadio*2+2)+"x"+str(self.varRadio*2+2)+"]",bg="white")

        # level에 따른 규칙 지정
        if self.varRadio==1:
            self.limittime=60
            self.minuspoint=10
            self.showtime=1
        elif self.varRadio==2:
            self.limittime=180
            self.minuspoint=8
            self.showtime=2
        else:
            self.limittime==300
            self.minuspoint=5
            self.showtime=4
            
        self.l3=Label(self.f1_2,text="시간: "+str(self.limittime),font=("Malgun Gothic",13))
        self.l3.grid(row=0,column=0,columnspan=2)
        self.l4=Label(self.f1_2,text="점수: "+str(self.point),font=("Malgun Gothic",13))
        self.l4.grid(row=0,column=2,columnspan=2)
        self.l5=Label(self.f1_2,text=None,font=("Malgun Gothic",13))
        self.l5.grid(row=1,column=0,columnspan=4)
           
        self.cardlen=self.varRadio*2+2
        self.selectcard=cards(self.cardlen)
        self.selectcard.name()
        self.selectcard.shuffle()
        self.selectcard.createDeck()          

        # showtime초 이후에 printBoard 함수 실행
        t = Timer(self.showtime, self.printBoard) 
        t.start()
        
        self.printanswer()
        self.count=True
        self.countdown(self.limittime)

    # 정답 제공
    def printanswer(self):
        self.labels=[]
        cnt = 0
        self.p=[]
        for i in range(self.cardlen):
            for j in range(self.cardlen):
                self.p.append(PhotoImage(file=self.selectcard.totalpic[cnt]))
                self.labels.append(Label(self.f3,image=self.p[cnt]))
                self.labels[cnt].grid(row=i,column=j)
                cnt+=1
                
    # 게임 가능한 상태    
    def printBoard(self):
        self.buttons = []
        cnt = 0
        self.p=[]
        for i in range(self.cardlen):
            for j in range(self.cardlen):
                self.p.append(PhotoImage(file=self.selectcard.deck[cnt]))
                c = lambda index=cnt: self.click(index)
                self.buttons.append(Button(self.f3,command=c,image=self.p[cnt]))
                self.buttons[cnt].grid(row=i,column=j)
                cnt+=1
    
    def click(self,index):
        # 뒤집힌 카드를 선택한 경우
        if self.selectcard.deck[index].show==False:
            self.selectcard.deck[index].show=True
            self.p1=PhotoImage(file=self.selectcard.deck[index])
            self.buttons[index].config(image=self.p1)
            self.buttons[index].image=self.p1
            self.numclick+=1
            
            if len(self.clickbutton)==2:
                self.p2=PhotoImage(file=self.selectcard.deck[self.clickbutton[0]])
                self.buttons[self.clickbutton[0]].config(image=self.p2)
                self.buttons[self.clickbutton[0]].image=self.p2
                self.p3=PhotoImage(file=self.selectcard.deck[self.clickbutton[1]])
                self.buttons[self.clickbutton[1]].config(image=self.p3)
                self.buttons[self.clickbutton[1]].image=self.p3
                self.clickbutton=[]
        
            if self.numclick==2:
                self.numclick=0   
                self.clickbutton.append(index)
                self.compare() 
            else:
                self.clickbutton.append(index)
                self.l5.config(text="")
        else:
            messagebox.showwarning("warn","같은 버튼을 두번 선택하였습니다.")

    # 선택된 두개의 카드 비교
    def compare(self):
        self.ttrial+=1
        if self.selectcard.deck[self.clickbutton[0]].name==self.selectcard.deck[self.clickbutton[1]].name:           
            self.clickbutton=[]
            self.l5.config(text="맞았습니다!   +10점",fg="blue")
            self.point+=10
            self.l4.config(text="점수: "+str(self.point))            
            self.countpairs()
        else:
            self.l5.config(text="틀렸습니다.   -"+str(self.minuspoint)+"점",fg="red")
            self.selectcard.deck[self.clickbutton[0]].show= False
            self.selectcard.deck[self.clickbutton[1]].show= False
            self.score()
            
    def countpairs(self):
        self.pair += 1
        if self.pair == self.cardlen**2/2:
            self.l3.grid_forget()
            self.l4.grid_forget()
            self.l5.config(text="Level"+str(self.varRadio)+" 성공 (총 시도:"+str(self.ttrial)+"번  시간:"+
                                str(self.limittime-self.remaining)+"초)",font=("Malgun Gothic",14),fg="red")
            self.count=False
            if self.varRadio<3:
                self.resetButton = Button(self.f4, command=self.result, text="END!!", width=15,bg="white")
                self.resetButton.pack(side="right")
                self.nextButton = Button(self.f4, command=self.nextLevel, text="NEXT =>", width=15,bg="white")
                self.nextButton.pack(side="right")
            else:
                self.resetButton = Button(self.f4, command=self.result, text="END!!", width=15,bg="white")
                self.resetButton.pack(side="right")

    def nextLevel(self):
        self.nextButton.destroy()
        self.resetButton.destroy()
        self.varRadio+=1
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        self.clickbutton=[]
        self.ttrial=0 
        self.numclick=0
        self.pair=0
        self.point=100

        # 현재까지의 기록 저장
        self.totalclick.append(self.ttrial)
        self.totaltime.append(self.limittime-self.remaining)
        self.totalpoint.append(self.point)
        
        self.l5.config(text="")
        self.start()
    
    def restart(self):
        self.f1.pack_forget()
        self.f1_2.pack_forget()
        self.f3.pack_forget()
        self.f4.pack_forget()
        
        self.database()
        
    ########################################################  결과 출력  #################################################
    def result(self):
        self.l2.pack_forget()
        self.f1_2.pack_forget()

        # 현재까지의 기록 저장
        self.totalclick.append(self.ttrial)
        self.totaltime.append(self.limittime-self.remaining)
        self.totalpoint.append(self.point)
        
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        self.resetButton.pack_forget()
        self.nextButton.pack_forget()
        
        self.insert2()
        self.showRank()
        
        self.theEnd = Button(self.f4,text="전체 게임종료",command=self.window.destroy, width=20,bg="white")
        self.theEnd.pack(side="right",ipadx=13,ipady=3)
        self.reset=Button(self.f4,text="다시 시작",command=self.restart,width=20,bg="white")
        self.reset.pack(side="left",ipadx=13,ipady=3)
            
    # 게임 실패 시
    def gamefail(self):                
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        self.l2.pack_forget()

        # 현재까지의 기록 저장
        self.totalclick.append(self.ttrial)
        self.totaltime.append(self.limittime-self.remaining)
        if self.point<0:
            self.totalpoint.append(0)
        else:
            self.totalpoint.append(self.point)
            
        self.insert2()
        self.l3.grid_remove()
        self.l4.grid_remove()
        self.l5.config(text="게임을 실패하였습니다.",font=("Malgun Gothic",15),fg="red3")
        self.showRank()
        
        self.theEnd = Button(self.f4, command=self.window.destroy, text="전체 게임종료", width=20,bg="white")
        self.theEnd.pack(side="right",ipadx=13,ipady=3)
        self.reset=Button(self.f4,text="다시 시작",command=self.restart,width=20,bg="white")
        self.reset.pack(side="left",ipadx=13,ipady=3)
        
    ########################################################  규칙  #########################################################
    # 점수 계산
    def score(self):
        self.point-=self.minuspoint # 감점
        if self.point<0:
            self.l4.config(text="점수: "+str(0))
            self.count=False
            messagebox.showinfo("Fail","점수 미달이므로 실패입니다.")
            self.gamefail()
        elif self.point<=30:
            self.l4.config(text="점수: "+str(self.point),fg="red")
        elif self.point>=150:
            self.l4.config(text="점수: "+str(self.point),fg="green")
        else:
            self.l4.config(text="점수: "+str(self.point))
    
    # 시간 계산
    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining
        if self.remaining <= 0:
            messagebox.showinfo("Fail","시간이 초과하여 실패입니다.")
            self.gamefail()
        elif self.count==False:
            self.l3.configure(text="time: %d" % self.remaining)
        else:
            if self.remaining<=15:
                self.l3.config(fg="red")
            self.l3.configure(text="time: %d" % self.remaining)
            self.remaining = self.remaining - 1
            self.window.after(1000, self.countdown) # 1000ms 이후에 countdown 함수 실행
    
    ########################################################  최종 결과창  #########################################################
    def showRank(self):
        # 정렬
        self.tempList = sorted(self.df,key=lambda x: -x[7])
        self.rlabel = Label(self.f3, text="Result", font=("Malgun Gothic",12,"bold")).grid(row=0, columnspan=8)
        # create Treeview with 8 columns
        cols = ('Rank', 'ID', 'Age', 'Gender','Level', 'Point', 'Click', 'Time', 'Total')
        self.listBox = ttk.Treeview(self.f3, columns=cols, show='headings',selectmode='browse')
        # set column headings, column, width
        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.column(col,width=75)

        # 데이터 입력
        for i, (name,age,gender,level,point,click,time,total) in enumerate(self.tempList, start=1):
            self.listBox.insert("", "end", values=(i, name,age,gender,level,point,click,time,total),iid=str(i))
            if self.d1==name and self.d2==str(age) and self.d3==gender and self.d4==str(level) and self.d5==str(point) and self.d6==str(click) and self.d7==str(time):
                self.r=i
        self.listBox.selection_set(str(self.r)) # player의 순위 highlight
        self.listBox.grid(row=1, column=0, columnspan=8)
        
        self.sb = ttk.Scrollbar(self.window, orient="vertical", command=self.listBox.yview)
        self.listBox.configure(yscrollcommand=self.sb.set)
    
        self.mine=Label(self.f3,text="순위: "+str(self.r)+"위\n"+self.d1+"의 성적: Level"+self.d4+" "+self.d5+"점 "+
                        self.d6+"번 시도 "+self.d7+"초", font=("Malgun Gothinc",16,"bold")) # 순위, 성적 제시
        self.mine.grid(row=2,column=0,columnspan=8)
        
    ##########################################################  관리  ###############################################################
    # 개인정보 입력
    def database(self):
        self.clickbutton=[]
        self.ttrial=0 
        self.numclick=0
        self.pair=0
        self.totalclick=[]
        self.totaltime=[]
        self.totalpoint=[]
        self.point=100
        self.remaining=0
        
        self.f=Frame(self.window,bg="azure")
        self.f.pack()
        
        self.dlabel=Label(self.f,text="정보를 입력해주세요",font=("Malgun Gothic",16),bg="azure")
        self.dlabel.grid(row=0,column=0,columnspan=4,padx=30,pady=10)
        
        # ID
        self.idl=Label(self.f, text="ID ( 영어로 )",bg="azure");self.idl.grid(row=1,column=0,padx=10,pady=10,columnspan=2)
        self.edit1=Entry(self.f,width=10);self.edit1.grid(row=1,column=2,padx=5,pady=10,columnspan=2)
        # Age
        self.agel=Label(self.f, text="Age",bg="azure");self.agel.grid(row=2,column=0,padx=10,pady=10,columnspan=2)
        self.edit2=Entry(self.f,width=10);self.edit2.grid(row=2,column=2,padx=5,pady=10,columnspan=2)
        # Gender
        self.radio = IntVar()  
        self.gender = Label(self.f, text="Gender(M/F)",bg="azure")  
        self.gender.grid(row=3,column=0,padx=5,pady=10,columnspan=2)
        self.R1 = Radiobutton(self.f, text="M", variable=self.radio, value=1,bg="azure")
        self.R1.grid(row=3,column=2,padx=5,pady=10)
        self.R2 = Radiobutton(self.f, text="F", variable=self.radio, value=2,bg="azure")
        self.R2.grid(row=3,column=3,padx=5,pady=10)
        
        # 입력
        self.btnInsert=Button(self.f,text="입력",font=("Malgun Gothic",11,"bold"),command=self.insertData,bg="lightcyan2")
        self.btnInsert.grid(row=4,column=0,columnspan=4, ipadx=15,ipady=3)
        
    def insertData(self):
        self.d1=self.edit1.get();self.d2=self.edit2.get()
        if self.radio.get()==1:
            self.d3="M"
        elif self.radio.get()==2:
            self.d3="F"
        else:
            self.d3="Null"

        # 미입력 정보
        if self.d2=="":
            self.d2="0"
        if self.d1=="":
            messagebox.showerror("경고","ID를 작성하지 않았습니다.\n아이디가 Guest로 지정됩니다.")
            self.d1="Guest"
        
        self.gamestart()

    def insert2(self):
        self.d4=str(self.varRadio)
        self.d5=str(sum(self.totalpoint))
        self.d6=str(sum(self.totalclick))
        self.d7=str(sum(self.totaltime))
        self.d8=str(self.varRadio*sum(self.totalpoint)*sum(self.totalclick)*sum(self.totaltime))
        self.totalinfo=self.d1+","+self.d2+","+self.d3+","+self.d4+","+self.d5+","+self.d6+","+self.d7+","+self.d8
        # server에게 정보 전달
        self.client()

    # 클라이언트 함수
    def client(self):
        # 기본 포트로 설정
        port = ECHO_PORT
        host="메인 server IP"  ####################### 실행시 server의 ip로 바꾸기 ########################

        # IP 주소 변수에 서버 주소와 포트 설정
        addr = host, port
    
        # 소켓 생성
        s = socket(AF_INET, SOCK_STREAM)

        try:
            s.connect(addr)
        except Exception as e:
            print('connection failed')
            sys.exit(2)
    
        # 연결되어 준비 완료 화면에 출력
        print ('connected!')

        # 입력받은 텍스트를 서버로 발송
        sent = s.send(self.totalinfo.encode())
        if sent == 0:
             print("socket connection broken")

        self.df=[]
        while True:
            data = s.recv(BUFSIZE)
            if len(data)==0:
                break
            info=repr(data.decode())
            info=str(info).split("'")[1]
            info=info.split("/")

            for i in range(len(info)):
                dt=info[i].split(",")
                for i in range(5):
                    dt[i+3]=int(dt[i+3])
                self.df.append(dt)
                

# ECHO_PORT 기본 포트
ECHO_PORT = 9190
# 버퍼 사이즈
BUFSIZE = 5120

window=Tk()
main(window)
window.mainloop()

