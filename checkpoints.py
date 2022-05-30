#project (checkpoint)

# So what should be the theme of the project?
# The theme would be making a gui based programme.
# Can have mysql database.
# saves data after encoding(basically make an encoder program as well)

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math
import random
import mysql.connector as mys
from time import sleep
edittab = False
import newtab

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
otherusedatabase = None


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
            datawin=databasewin(mycursor)

        

class listtab():
    def __init__(self, mycursor, tablename):
        self.cursor = mycursor
        self.tablename= tablename
        self.pww = PanedWindow(orient = 'horizontal')
        self.pww.grid(column = 0, row = 110, columnspan = 10,sticky=W)
        self.pww.config(background = themeback)
        self.showlist(self.cursor)

    def getrowtitle(self,btnnumber,column):
        global listnames
        columnname = ['sthaitsempty','thirdcase','3','4']
        self.cursor.execute(f'desc {self.tablename}')
        rownames = self.cursor.fetchall()
        if btnnumber<0:
            btnnumber = 0
        columnlen = len(listnames[0])
        if btnnumber < columnlen:
            rownumber = btnnumber
        else:
            rownumber = btnnumber%columnlen

        columnname[3] = rownames[rownumber][0]

        #check for primary keys
        
        for i in range(len(rownames)):
            if rownames[rownumber][3] == "PRI":
                columnname[1] = 'easy'
                break
            
            elif rownames[i][3] == 'PRI':
                columnname[0] = rownames[i][0]
                columnname[1] = 'seceasy'
                columnname[2] = self.getcolumnnames(i,column)
                break
            

        if columnname[0] == 'sthaitsempty':
            columnname[0] = rownames[rownumber][0]

        if columnname[1] == 'thirdcase':
            if len(rownames) <=2:
                if btnnumber % 2 != 0:
                    i = 0
                else:
                    i = 1
                columnname[3] = self.getcolumnnames(i,column)
                columnname[2] = rownames[i][0]
                columnname[1] = '2columns'
            else:
                
                if btnnumber % 3 ==2:
                    print('1st')
                    columnname[2] = (rownames[0][0],self.getcolumnnames(0,column))
                    columnname[1] = (rownames[1][0],self.getcolumnnames(1,column))
                elif btnnumber % 3 ==1:
                    print('2nd')
                    columnname[1] = (rownames[0][0],self.getcolumnnames(0,column))
                    columnname[2] = (rownames[2][0],self.getcolumnnames(2,column))
                elif btnnumber % 3 == 0 and btnnumber == 0 or btnnumber < 2:
                    print('3rd')
                    columnname[1] = (rownames[1][0],self.getcolumnnames(1,column))
                    columnname[2] = (rownames[2][0],self.getcolumnnames(2,column))
                elif btnnumber % 3 == 0:# and btnnumber>3 and btnnumber < 5:
                    print('4th')
                    columnname[1] = (rownames[0][0], self.getcolumnnames(0,column))
                    columnname[2] = (rownames[2][0], self.getcolumnnames(2,column))
                
        print(columnname)
        return columnname
        

    def getcolumnnames(self,btnnumber,column):
        self.cursor.execute(f'select * from {self.tablename}')
        names = self.cursor.fetchall()

        name = names[column][btnnumber]
        
        return name

    def savechanges(self,label,button,textname,buttonnumber,column):
        global changesdone
        newvalue = label.get()
    
        try:
            button.destroy()
        except:
            pass
        label.destroy()

##        columnname = self.getcolumnnames(buttonnumber,tablename)
        rowtitle = self.getrowtitle(buttonnumber,column)
        if rowtitle[1] == 'easy':
            self.cursor.execute(f'update {self.tablename} set {rowtitle[0]} = "{newvalue}" where {rowtitle[0]} = "{textname}"')

        elif rowtitle[1] == 'seceasy':
            self.cursor.execute(f'update {self.tablename} set {rowtitle[3]} = "{newvalue}" where {rowtitle[0]} = "{rowtitle[2]}"')

        else:
            if rowtitle[1] == "2columns":
                self.cursor.execute(f'update {self.tablename} set {rowtitle[0]} = "{newvalue}" where {rowtitle[2]} = "{rowtitle[3]}" and {rowtitle[0]} = "{textname}"')
            else:
                if textname == 'None' and rowtitle[2][1] != 'None' and rowtitle[1][1] != 'None':
                    print('here')
                    self.cursor.execute(f'update {self.tablename} set {rowtitle[3]} = "{newvalue}" where {rowtitle[0]} = "{textname}" and {rowtitle[2][0]} = "{rowtitle[2][1]}" and {rowtitle[1][0]} = "{rowtitle[1][1]}"')
                    
                elif rowtitle[2][1] == 'None' and textname !='None' and rowtitle[1][1] != 'None':
                    print('sechere')
                    self.cursor.execute(f'update {self.tablename} set {rowtitle[3]} = "{newvalue}" where {rowtitle[0]} = "{textname}" and {rowtitle[2][0]} = {rowtitle[2][1]} and {rowtitle[1][0]} = "{rowtitle[1][1]}"')

                elif rowtitle[2][1] != 'None' and textname !='None' and rowtitle[1][1] =='None':
                    print('thirdhere')
                    self.cursor.execute(f'update {self.tablename} set {rowtitle[3]} = "{newvalue}" where {rowtitle[0]} = "{textname}" and {rowtitle[2][0]} = "{rowtitle[2][1]}" and {rowtitle[1][0]} = {rowtitle[1][1]}')
                    

                elif rowtitle[2][1] =='None' and textname =='None' and rowtitle[1][1] == 'None':
                    print('fourthhere')
                    self.cursor.execute(f'update {self.tablename} set {rowtitle[3]} = "{newvalue}" where {rowtitle[0]} = {textname} and {rowtitle[2][0]} = {rowtitle[2][1]} and {rowtitle[1][0]} = {rowtitle[1][1]}')
                else:
                    print('else here')
                    self.cursor.execute(f'update {self.tablename} set {rowtitle[3]} = "{newvalue}" where {rowtitle[0]} = "{textname}" and {rowtitle[2][0]} = "{rowtitle[2][1]}" and {rowtitle[1][0]} = "{rowtitle[1][1]}"')
                
            
        self.pww.destroy()
        changesdone = 1
        self.__init__(self.cursor,self.tablename)

    def commitchanges(self,button):
        global changesdone
        changesdone = 0
        button.destroy()
        self.cursor.execute('commit')

    def editlist(self,row,column,buttonnumber,boxname):
        global listbuttons,edittab,labels,btn
        if edittab == True:
            labels[0].destroy()
            try:
                btn[0].destroy()
            except:
                pass
                   
        if edittab == False:
            edittab = True
        #listbuttons[buttonnumber].destroy()
        if boxname == None:
            boxname = 'None'
        lab = Entry(self.pww, width = 17, bg = entryback)
        lab.insert(0,boxname)
        lab.grid(column = column, row = row+3)
        
        but = Button(self.pww, text = 'Modify Value', width = 15, command = lambda : self.savechanges(labels[0],but,boxname,buttonnumber,row))
        but.grid(column = 0, row = 210)

        if len(labels) >= 1:
            labels[0] = lab
            
        else:
            labels.append(lab)
            
        if len(btn) >= 1:
            btn[0].destroy()
            btn[0] =  but

        else:
            btn.append(but)

    def addcolumnname(self,newcolumn,addbtn):
        addbtn.destroy()
        columnname = newcolumn.get()
        self.cursor.execute(f'alter table {self.tablename} add {columnname} varchar(30)')
        self.cursor.execute('commit')
        self.__init__(self.cursor,self.tablename)

    def addcolumn(self,cno,btn):
        btn.destroy()
        newcolumn = Entry(self.pww, bg = entryback)
        newcolumn.insert(0,'Columnname...')
        newcolumn.grid(column = cno, row = 1)

        addbtn = Button(self.pww, text = 'Add', width = 15, command = lambda : self.addcolumnname(newcolumn,addbtn))
        addbtn.grid(column = cno, row = 3,sticky = 'S')

    def rowadd(self,labels,tabname,btn):
        for i in range(len(labels)):
            if i == 0:
                self.cursor.execute(f'insert into {self.tablename} ({tabname[0][0]}) values("{labels[0].get()}")')
            elif i == 1:
                self.cursor.execute(f'update {self.tablename} set {tabname[1][0]} = "{labels[1].get()}" where {tabname[0][0]} = "{labels[0].get()}"')
            else:
                self.cursor.execute(f'update {self.tablename} set {tabname[i][0]} = "{labels[i].get()}" where {tabname[0][0]} = "{labels[0].get()}" and {tabname[1][0]} = "{labels[1].get()}"')

        btn.destroy()
        self.__init__(self.cursor,self.tablename)
        

    def addrow(self,cno,rno,tabname,but,lab = None):
        global fontback, fontcolor
        if lab != None:
            lab.destroy()
        but.destroy()
        labels = []
        for i in range(len(tabname)):
            label = Entry(self.pww, width = 18)
            label.grid(column = cno, row = rno)
            label.insert(0,'row value')
            labels.append(label)
            cno +=1

            if i == len(tabname)-1 :
                Label(self.pww, bg = fontback, fg = fontcolor).grid(column = 0, row = rno+2)
                addbtn = Button(self.pww, text = 'Add', width = 15, command = lambda : self.rowadd(labels,tabname,addbtn))
                addbtn.grid(column = int(cno/2), row = rno+3)
        
    def droptab(self):
        global temptab,templisttab,otherusedatabase
        ask = messagebox.askquestion('Delete',f'Are you sure you want to delete table {self.tablename}',icon = 'warning')
        if ask == 'yes':
            self.cursor.execute(f'drop table {self.tablename}')
            tableopen = False
            templisttab.pww.destroy()
            temptab.pw.destroy()
            
            temptab = tablewin(otherusedatabase,self.cursor)
        else:
            pass
        

    def showlist(self, cursor):
        global listnames,changesdone,fontback,fontcolor
        cursor.execute(f'select * from {self.tablename}')
        tablelist = cursor.fetchall()
        cursor.execute(f'desc {self.tablename}')
        tabname = cursor.fetchall()
        cno = 0
        rno = 2
        for i in range(len(tabname)):
            if i == len(tabname)-1:
                Label(self.pww, text = '\n', bg = themeback).grid(column = 0,row = 0)
                addbtn = Button(self.pww, text = 'Add column', width = 15, command = lambda cno = cno+1 : self.addcolumn(cno,addbtn))
                addbtn.grid(column =cno+1,row = 1)
                Label(self.pww,bg = themeback).grid(column = cno, row = 2)
                
            Label(self.pww,text = tabname[i][0],width = 18,borderwidth = 6, relief = 'ridge',fg = 'yellow', bg = 'red', font = 'Agency_fb 10').grid(column = cno,row = 1)
            cno +=1
        listnames = []
        bno = 0
        btn = None
        for i in range(len(tablelist)):
            for j in range(len(tabname)):
                if cno >= len(tabname):
                    cno = 0
                    rno +=1
                if tablelist[i][j] == None:
                    text = 'None'
                else:
                    text = tablelist[i][j]
                btn = Button(self.pww, text = text,width = 15,command = lambda i=i,j=j,c=bno:self.editlist(i,j,c,tablelist[i][j]))
                btn.grid(column = cno, row = rno)
                bno+=1
                cno +=1
                if i == len(tablelist)-1 and j == len(tabname)-1:
                    emlab = Label(self.pww,bg = fontback, fg = fontcolor)
                    emlab.grid(column = 0, row = rno+1)
                    newrowbut = Button(self.pww, text = 'Add row', width = 15, command = lambda : self.addrow(0,rno+1,tabname,newrowbut,emlab))
                    newrowbut.grid(column = 0, row = rno+2)
                    dropbut = Button(self.pww, text = 'delete table', width = 15, command = lambda : self.droptab())
                    dropbut.grid(column = 1, row = rno +2)
                    dropbut.config(fg = 'red')
            listnames.append(tablelist[i])
        if len(tablelist) == 0:
            lab = Label(self.pww, text = "\nEmpty table, click on the below button to add a row\n", font ='Agency_fb 12 bold', bg = fontback, fg = fontcolor)
            lab.grid(column = 0, row = rno,columnspan = 3)
            newrowbut = Button(self.pww, text = 'Add row', width = 15, command = lambda : self.addrow(0,rno+1,tabname,newrowbut,lab))
            newrowbut.grid(column = 0, row = rno+1)

        if changesdone == 1:
            commitbtn = Button(self.pww, text = f'commit changes in "{self.tablename}"', command = lambda : self.commitchanges(commitbtn))
            commitbtn.grid(column = 0, row = 212,columnspan = 3)
        else:
            pass
            

class tablewin():
    def __init__(self,database,mycursor):
        global datawindow
        self.database = database
        self.cursor = mycursor
        self.pw=PanedWindow(orient = 'horizontal')
        self.w = Scrollbar(self.pw)
        self.mylist = Listbox(datawindow,yscrollcommand = self.w.set)
        self.w.grid(column = 100, row = 0)
        self.w.config(command = self.mylist.yview)
        self.pw.grid(column = 0, row = 100, columnspan = 4)
        self.pw.config(background = themeback)
        self.cno = 0
        self.rno = 0
        self.showtable()
    
##    def databaseview(self,cursor):
##        databasewin(cursor)

    def callinglisttab(self,cursor,tablename,tablebuttons,i):
        global templisttab,but
        
        if templisttab == None:
            pass
        else:
            templisttab.pww.destroy()
        try:
            if but[1] != 'None':
                tablebuttons[but[1]].config(bg = 'white')
                tablebuttons[i].config(bg = 'yellow')
                but[1] = i
            else:
                tablebuttons[i].config(bg = 'yellow')
                but[1] = i
        except:
            tablebuttons[i].config(bg = 'yellow')

        templisttab = listtab(cursor, tablename)

    def addtab(self,btn):
        btn.destroy()
        self.pw.destroy()
        test = newtab.createtable(self,self.database,self.cursor)
        
    

    def showtable(self):
        self.cursor.execute('use {}'.format(self.database))
        self.cursor.execute("show tables")
        tables = self.cursor.fetchall()

        Label(self.pw, text = "\n\nDatabase:- " + self.database + '\n',bg = fontback , fg = fontcolor, font = "Agency_fb 12 bold").grid(column = 0, row = 0, columnspan = 7)

        if len(tables) == 0:
            Label(self.pw,text = "\nNo tables to show in this database ",fg = fontcolor, bg = fontback, font = "Agency_fb 12 bold").grid(column = 1,row = 2,columnspan = 3)
            
            tabaddbut = Button(self.pw, text = 'Add table', width = 15, command = lambda : self.addtab(tabaddbut))
            tabaddbut.grid(column = 0, row = 3)
        
        else:
            tablebuttons = []
            self.cno = 0
            self.rno =1
            for i in range(0,len(tables)):
                if self.cno > 8 :
                    self.cno = 0
                    self.rno +=1
                tablebutton = Button(self.pw, text = tables[i][0],width = 15, command = lambda i = i:self.callinglisttab(self.cursor, tables[i][0],tablebuttons,i))
                tablebutton.grid(column = self.cno, row = self.rno)
                tablebuttons.append(tablebutton)
                self.cno += 1
                if i == len(tables)-1:
                    tabaddbut = Button(self.pw, text = 'Add table', width = 15, command = lambda : self.addtab(tabaddbut))
                    tabaddbut.grid(column = self.cno, row = self.rno)
            

class databasewin():
    def __init__(self,mycursor):
        self.cursor = mycursor
        self.finaldata = self.purify()
        self.datalen=len(self.finaldata)
        self.window()
        self.tableopen = False

    def purify(self):
        #variables
        output=[]
        ci=0
        ri=0
        unwanted=('performance_schema', 'sakila', 'sys', 'world')
        self.cursor=conn.cursor()
        self.cursor.execute("Show databases;")
        databases=self.cursor.fetchall()
        noofdatabases=len(databases)
        cleardatabase = []
        for i in range(noofdatabases):
            if databases[i][0] not in unwanted:
                cleardatabase.append(databases[i][0])
        return cleardatabase

    def buttonpressed(self,selecteddatabase,btn):
        global temptab,templisttab,themeback,but,otherusedatabase
        otherusedatabase = selecteddatabase
        if self.tableopen == False:
            self.tableopen = True
            btn.config(bg = 'yellow')
            but[0] = btn
        else:
            if not templisttab:
                but[0].config(bg = 'white')
                btn.config(bg = 'yellow')
                but[0] = btn
            else:
                templisttab.pww.destroy()
                but[0].config(bg = 'white')
                btn.config(bg = 'yellow')
                but[0] = btn
            temptab.pw.destroy()
        
        temptab = tablewin(selecteddatabase,self.cursor)

    def exit(self,window):
        global conn
        conn.close()
        window.destroy()

    def createdatabase(self,databasename,datawin):
        unwanted = ["'","?","/",">","<","!","@","#","$","%","^","&","*","(",")","-","+","[","]","{","}",'"',"\\",".",","]
        databasename = databasename.get().translate({ord(x) : '' for x in unwanted})
        databasename = databasename.replace(' ',"_")
        self.cursor.execute(f'create database {databasename}')
        datawin.destroy()
        self.__init__(self.cursor)

    def addbase(self,cno,rno,datawin):
        basenameentry = Entry(datawin, width = 18)
        basenameentry.grid(column = cno, row = rno)
        basenameentry.insert(0,'databasename')
        createbut = Button(datawin, text = 'Add',width = 15,command = lambda : self.createdatabase(basenameentry,datawin))
        createbut.grid(column = cno+1, row = rno)
    
    def window(self):
        global datawindow
        datawindow=Tk()
        datawindow.title("Available data ")
        datawindow.config(background=themeback)
        datawindow.state('zoomed')
        if self.datalen == 0:
            Label(datawindow,text="There are no databases to work on. \n To make a new database click on the button below",fg=fontcolor,bg=fontback,font="Agency_fb 20 bold").grid(column=0,row=0,columnspan=self.datalen)
        else:
            Label(datawindow,text="\nSelect a database to work on \n",fg=fontcolor,bg=fontback,font="Agency_fb 20 bold").grid(column=0,row=0,columnspan=self.datalen)
            buttons = []
            cno = 0
            rno = 2
            for i in range(0,self.datalen):
                if cno > 8 :
                    cno = 0
                    rno += 1
                button = Button(datawindow,text = self.finaldata[i],width = 15, command = lambda i = i : self.buttonpressed(self.finaldata[i],buttons[i]))
                button.grid(column = cno, row = rno)
                cno += 1
                buttons.append(button)

                if i == self.datalen-1:
                    baseaddbut = Button(datawindow, text = 'Add database', width = 15, command = lambda : self.addbase(cno,rno,datawindow))
                    baseaddbut.grid(column = cno, row = rno)

        Button(datawindow, text = "Exit",width = 15,command = lambda: self.exit(datawindow)).grid(column = int(2), row = 200)

if __name__ == "__main__":
    log=loginwindow()
