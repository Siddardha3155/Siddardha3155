from http import server
from tkinter import *
import socket
from tkinter import messagebox
from tokenize import String
import serial
import time
ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)
def sensor_data(client_socket):
    for i in range(20000):
        line = ser.readline()
        if line:
            print(line)
            string = line.decode(errors='replace')
            if(i>1):
                num = int(string[10:len(string)-5])
                if(num<10):
                    client_socket.send(string.encode("ASCII"))
                    
BUFF_SIZE=1024*1024
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def verify(challenge):
    if(challenge[1:4]+challenge[0]==challenge[4:len(challenge)]):
        return True
    else:
        return False
def connect_server(gui):
    try:
        print("server connection requested")
        client_socket.connect(("192.168.56.1",9999))
        x=client_socket.recv(BUFF_SIZE)#!
        print(x.decode("ASCII")) #connection check
        register=client_socket.recv(BUFF_SIZE).decode("ASCII")#2
        def on_closing():
                client_socket.send("close".encode("ASCII"))#6
                gui.destroy()
        gui.protocol("WM_DELETE_WINDOW",on_closing)
        if(register=="found"):
            challenge=client_socket.recv(BUFF_SIZE).decode("ASCII")#3
            if(verify(challenge)):
                client_socket.send("verified".encode("ASCII"))#4
                print(client_socket.recv(BUFF_SIZE).decode("ASCII"))#5
                sensor_data(client_socket)
            else:
                client_socket.send("notverified".encode("ASCII"))#4
                on_closing()
                print("not auth")
        else:
            print("register")
            on_closing()

    except  Exception as e:
        print("un authorized")

gui=Tk()
gui.geometry("500x500")
password= Entry(gui,show="*",width=20)
def close_win():
    if(password.get()=="mg"):
        gui.destroy()
        gui1=Tk()
        gui1.geometry("500x500")
        b=Button(gui1,text="connect to the server",command=lambda:connect_server(gui1)).place(x=100,y=100)
        gui1.mainloop()
    else:
        Label(gui,text="wrong password").place(x=150,y=150)
l1=Label(gui,text="Enter the Password", font=('Helvetica',20)).pack(pady=20)
password.pack()
b1=Button(gui, text="submit", font=('Helvetica bold',
10),command=close_win).pack(pady=20)
gui.mainloop()
