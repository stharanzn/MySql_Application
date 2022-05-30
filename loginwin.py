#login window

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math
import random
import mysql.connector as mys
from time import sleep
edittab = False
import startfile

#variables
themeback="black"
fontback=themeback
fontcolor="red"
entryback="white"
toshow='*'
databasename='mysql'
temptab = None
templisttab = None
listnames = []
labels = []
btn =  []
changesdone = 0
but = ['None','None']
datawindow = None


class loginwindow():
    def __init__(self):
        self.setup()

    def setup(self):
        loginwin=Tk()
        loginwin.title("Connecting to mysql server")
        loginwin.config(background=themeback)
        loginwin.state("zoomed")
        Label(loginwin,text="Login to mysql \n\n",bg=fontback,fg=fontcolor,font="Agency_fb 20 bold").grid(column=0,row=0,columnspan=3)

        Label(loginwin,text="Enter your user (Default 'root'): ",bg=fontback,fg=fontcolor,font="Agency_fb 12 bold").grid(column=0,row=1)
        username=Entry(loginwin, width=20,bg=entryback)
        username.insert(0,'root')
        username.grid(column=2,row=1,sticky=E)

        Label(loginwin,text="",bg=fontback,fg=fontcolor).grid(column=1,row=2)
        Label(loginwin,text="",bg=fontback,fg=fontcolor).grid(column=1,row=4)        

        Label(loginwin,text="Enter your mysql password\n(leave empty for no password):",bg=fontback,fg=fontcolor,font="Agency_fb 12 bold").grid(column=0,row=3,sticky = S)
        password=Entry(loginwin,width=20,bg=entryback,show=toshow)
        password.grid(column=2,row=3,sticky=S)

        loginwin.bind('<Return>', lambda e : self.connect(username, password,loginwin))

        Button(loginwin,text="Login",width=15,command= lambda : self.connect(username, password,loginwin)).grid(column=1,row=5,sticky=S)
        
    def connect(self,username,password,loginwin):
        global conn
        connestablished = False
        uname=username.get()
        upass=password.get()
        if uname=='':
            uname='root'

        try:
            mys.connect(host='localhost',user=uname,passwd=upass,database=databasename)
            connestablished = True

        except:
            messagebox.showerror("Status","Connection failed  \n")
        
        if connestablished == True:
            conn = mys.connect(host='localhost',user=uname,passwd=upass,database=databasename)
            messagebox.showinfo("Status","Connection Successful")
            loginwin.destroy()
            mycursor=conn.cursor()
            datawin=startfile.databasewin(mycursor,conn)

if __name__ == '__main__':
    log = loginwindow()
