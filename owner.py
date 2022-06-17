import socket
from tkinter import *
from tkinter import *
import tkinter.messagebox
BUFF_SIZE=1024*1024
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.56.1",9998))
print("requesting connection to server")
x=client_socket.recv(BUFF_SIZE)
print(x.decode("ASCII"))
xq=client_socket.recv(BUFF_SIZE)
while x.decode("ASCII")=="accept":
    xq=client_socket.recv(BUFF_SIZE)
    print(xq.decode("ASCII"))
    tkinter.messagebox.showinfo("danger")


