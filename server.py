from ctypes.wintypes import MSG
import aes1
from http import client, server
import mysql.connector
import socket
import random  
import string  
def  specific_string(length):  
    sample_string = '01' # define the specific string  
    # define the condition for random string  
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    return result  
BUFF_SIZE=1024*1024
serversocket=socket.socket()
port=9999
serversocket.bind(("192.168.56.1",port))
serversocket.listen(5)
serversocket1=socket.socket()
port1=9998
serversocket1.bind(("192.168.56.1",port1))
serversocket1.listen(5)
c1,addr1=serversocket1.accept()
print("connected to client")
def crp(addr1,c):
    try:
        mydb=mysql.connector.connect(host="localhost",user="root",password="siddu@1003",database="siddu")
        print(mydb)
        mycursor=mydb.cursor()   
        mycursor.execute("SELECT * FROM crp")
        myresult = mycursor.fetchall()
        flag=False
        for x in myresult:
            if(x[0]==addr1[0]):
                c.send("found".encode("ASCII"))#2
                c.send((x[1]+x[2]).encode("ASCII"))
                status1=c.recv(BUFF_SIZE)
                if(status1.decode("ASCII")=="verified"):
                    c.send(specific_string(len(x[1])).encode("ASCII"))
                    sql="UPDATE crp SET status = 'online' WHERE ipv4='"+str(x[0]+"'")
                    mycursor.execute(sql)
                    mydb.commit()
                    c1.send("accept".encode("ASCII"))
                    c1.send("danger".encode("ASCII"))
                    while True:
                        data=c.recv(BUFF_SIZE)
                        c1.send(data)
                else:
                    sql="UPDATE crp SET status = 'offline' WHERE ipv4='"+str(x[0]+"'")
                    mycursor.execute(sql)
                    mydb.commit()
                    break    
                flag=True
                break
        if(flag==False):
            c.send("no".encode("ASCII"))#2
            c.close()        
        else:
            if(c.recv(BUFF_SIZE).decode("ASCII")=="close"):
                print("mg")        
        mydb.close()
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if mydb.is_connected():
            mydb.close()
            mycursor.close()
            print("MySQL connection is closed")
# def authentication():
while True:
    c, addr = serversocket.accept()
    c.send("checking authorization".encode("ASCII"))#1 connection received message sent to client
    print(addr[0])
    crp(addr,c)
# class owner:
#     addr1=()
#     def owner(self):
#         c1,self.addr1=serversocket1.accept()
#         c1.send("mg".encode("ASCII"))
#         print(self.addr1addr1[0])
#     def mg(self):
#         print(self.addr1[0]) 
# from concurrent.futures import ThreadPoolExecutor
# with ThreadPoolExecutor(max_workers=2) as executor1:
#     executor1.submit(authentication)
#     executor1.submit(owner.owner)
