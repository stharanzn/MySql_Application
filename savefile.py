#saving data
import startfile
import tkinter
from tkinter import *
from tkinter import messagebox
import mysql.connector


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

class savingdata():
    def __init__(self, pww = 'paned window', cursor = 'cursor', tablename = 'tablename'):
        self.pww = pww
        self.cursor = cursor
        self.tablename = tablename
        self.listnames = startfile.listnames
        self.listtabinstance = startfile.listtab(self.cursor,self.tablename)
        
    def getrowtitle(self,btnnumber,column):
        columnname = ['sthaitsempty','thirdcase','3','4']
        self.cursor.execute(f'desc {self.tablename}')
        rownames = self.cursor.fetchall()
        if btnnumber<0:
            btnnumber = 0
        columnlen = len(self.listnames[0])
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

    def savechanges(self,label,button,textname,buttonnumber,column,listnames):
        self.listnames = listnames
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
        startfile.changesdone = 1
        startfile.listtab(self.cursor,self.tablename)

    def editlist(self,row,column,buttonnumber,boxname):
        global edittab,labels,btn,listnames
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
        
        but = Button(self.pww, text = 'Modify Value', width = 15, command = lambda : self.savefilevar.savechanges(labels[0],but,boxname,buttonnumber,row,listnames))
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
        startfile.listtab.__init__(self,self.cursor,self.tablename)

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
        startfile.listtab.__init__(self,self.cursor,self.tablename)
        

    def addrow(self,cno,rno,tabname,but,lab = None):
        global fontback, fontcolor
        if lab != None:
            lab.destroy()
        but.destroy()
        labels = []
        for i in range(len(tabname)):
            label = Entry(self.pww, width = 18)
            label.grid(column = cno, row = rno)
            label.insert(0,'row_value')
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

if __name__ == '__main__':
    print('this is the wrong start file')    
