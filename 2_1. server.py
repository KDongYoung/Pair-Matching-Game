#! /usr/bin/env python

# server for tcp echo.
import sys
from socket import *
from threading import Thread
import sqlite3

# ECHO_PORT 기본 포트
ECHO_PORT = 9190

# 버퍼 사이즈
BUFSIZE = 2048

class Server:
    def __init__(self):
        self.port = ECHO_PORT       # 기본 포트로 설정
        self.s = socket(AF_INET, SOCK_STREAM)   # 소켓 생성 (UDP = SOCK_DGRAM, TCP = SOCK_STREAM)
        self.s.bind(('', self.port))    # 포트 설정
        print ('server ready')  # 준비 완료 화면에 표시

        while True:
            self.s.listen(3)    # 포트 ON
            self.connection, self.address = self.s.accept()
            ip, port = str(self.address[0]), str(self.address[1])
            print("Connected with " + ip + ":" + port)
            t = Thread(target=self.clientThread)
            t.start()
        self.s.close()

    def clientThread(self):
        client_input = self.connection.recv(BUFSIZE)
        self.score=str(client_input).split("'")[1]
        self.score=self.score.split(",")
        self.insert()
        self.save()
        self.connection.close()

    def insert(self):
        con, cur = None, None
        sql = ""
        con = sqlite3.connect("C:/sqlite/pairgameDB")
        cur = con.cursor()

        sql = "INSERT INTO pairgame VALUES('" + self.score[0] + "','" + self.score[1] + "','" + self.score[2] + "','" + self.score[3] + "','" + self.score[4] + "','" + self.score[5] + "','" + self.score[6] + "','" + self.score[7] + "')"
        cur.execute(sql)
        con.commit()
        con.close()

    def save(self):
        con, cur = None, None
        # 데이터 불러오기
        con = sqlite3.connect("C:/sqlite/pairgameDB")  ########### 데이터베이스를 생성한 경로로 바꾸기 ############
        cur = con.cursor()
        cur.execute("SELECT * FROM pairgame")

        data=[]
        while True:
            row = cur.fetchone()
            if row == None:
                break
            d1 = row[0]
            d2 = row[1]
            d3 = row[2]
            d4 = row[3]
            d5 = row[4]
            d6 = row[5]
            d7 = row[6]
            d8 = row[7]
            data.append(str(d1)+","+str(d2)+","+str(d3)+","+str(d4)+","+str(d5)+","+str(d6)+","+str(d7)+","+str(d8))
        data="/".join(data)
        self.connection.send(data.encode())
        print("finish sending")

Server()
