#!/usr/bin/env python
# coding: utf-8

# # 데이터베이스 만들기
import sqlite3
con, cur=None,None
con = sqlite3.connect('C:/sqlite/pairgameDB')
cur=con.cursor()
# Create table 
cur.execute("CREATE TABLE pairgame (id char(15),age int, gender char(4),level int, point int, click int, time int, total int)")
con.commit()
con.close()



