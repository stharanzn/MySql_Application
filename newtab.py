import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector as myc
import startfile

themeback = 'black'
fontcolor = 'white'

###################################################   CREATING NEW TABLE start  ########################################################
        

class createtable():
    def __init__(self,selff,database,cursor):
        self.otherself = selff
        self.database = database
        self.win = Tk()
        self.themeback = themeback
        self.fontcolor = fontcolor
        self.win.grab_set()
        self.win.title('Creating table ')
        self.win.config(background = themeback)
        self.win.state('zoomed')
        self.cursor = cursor
        self.tabname = Entry(self.win, width = 20)
        self.tabname.grid(column = 1, row = 1)
        self.tabname.insert(0,'Tablename')
        self.leb = Label(self.win,bg = self.themeback).grid(column = 1, row = 2)
        self.cno = 0
        self.rno = 4
        self.columnnamesentry = []
        self.n = StringVar()
        self.m = StringVar()
        self.columntypes = {'string(varchar)', 'int'}
        self.columnkeys = {'None', 'Primary key'}
        self.lab = Label(self.win,bg = self.themeback).grid(column = 0, row = 104)        
        self.desbut = Button(self.win, text = 'cancel', width = 15,command = lambda : self.win.destroy()).grid(column = 0, row = 105)
        self.rowlen = 1
        self.deflist = []
        self.cslot = 0
        vars = []
        self.rest(vars)
        self.addcolumn(vars)

    def addcolumn(self,varlist,first = 'no'):

        rno = 4

        column = Entry(self.win, width = 20)
        column.grid(column = self.cno, row = 3)
        self.columnnamesentry.append([])
        self.columnnamesentry[self.cslot].append(column)
        column.insert(0,f'column_name_{len(self.columnnamesentry)}')
        self.cno += 2
        if first != 'yes':
            for i in range(self.rowlen):
                row = Entry(self.win, width = 18)
                row.grid(column = self.cno-2, row = rno)
                self.columnnamesentry[self.cslot].append(row)
                row.insert(0,f'row_value_{self.cslot+1}_{len(self.columnnamesentry[self.cslot])-1}')
                rno += 1
        self.cslot += 1        

# here goes the combobox or option menu

        columnkeys = {'first','second','third'}

        n = StringVar(self.win)
        n.set('string(varchar)')
        Label(self.win, text = '\nAdvance options',bg = self.themeback, fg = self.fontcolor, font = 'Agency_fb 12').grid(column = self.cno-1, row = 2)
        columntypebox = OptionMenu(self.win,n, *self.columntypes)
        columntypebox.config(width = 11)
        columntypebox.grid(column = self.cno-1, row = 3)
        
        m = StringVar(self.win)
        m.set('None')
        varlist.append((n,m))
        columnkeybox = OptionMenu(self.win,m, *self.columnkeys)
        columnkeybox.config(width = 10)
        columnkeybox.grid(column = self.cno-1, row = 5)

        Label(self.win,bg = self.themeback, fg = self.fontcolor).grid(column = self.cno-1, row = 6)
        default = Entry(self.win, width = 20)
        default.insert(0,'Default value - NULL/0')
        self.deflist.append(default)
        default.grid(column = self.cno-1, row = 7)

        

        
        

    def addrow(self,btn = 'isthere',first = 'no'):
        if btn != 'isthere':
            btn.destroy()

        else:
            pass

        rno = self.rowlen + 4
        
        if first != 'yes':
            self.rowlen += 1
            cno = 0            
        
            for i in range(len(self.columnnamesentry)):
                row = Entry(self.win, width = 18)
                row.grid(column = cno, row = rno)
                self.columnnamesentry[i].append(row)
                row.insert(0,f'row_value_{i+1}_{len(self.columnnamesentry[i])-1}')
                cno += 2
        
            
        Label(self.win, bg = self.themeback, fg = self.fontcolor).grid(column = 0, row = rno+1)
        btn = Button(self.win, text = 'add new row', width = 15, command = lambda : self.addrow(btn))
        btn.grid(column = 0, row = rno+2)
            

    def create(self,varlist):
        typelist = []
        proceed = 0
        mainproceed = 0
        erroroccured = 0
        errorshown = 0
        hasprimary = 'no'
        unwanted = ["'","?","/",">","<","!","@","#","$","%","^","&","*","(",")","-","+","[","]","{","}",'"',"\\",".",","]
        errors = ['Terminating table creation due to following error/s\n']
        self.cursor.execute('show tables')
        tabnames = self.cursor.fetchall()

        tabnamee = self.tabname.get().translate({ord(x) : '' for x in unwanted})
        tabnamee = tabnamee.strip().replace(" ","_")
        for i in range(len(tabnames)):
            if tabnamee == tabnames[i][0]:
                msg = '==>Table name already exists'
                errors.append(msg)
                proceed = 0
                print(tabnames)
            
        if tabnamee == '' or tabnamee == 'Tablename':
            self.tabname.config(fg = 'Blue')            
            msg = '==> Please specify a table name for your table\n'
            errors.append(msg)
            mainproceed = 0

        try:
            tabnamee = int(tabnamee)
            self.tabname.config(fg = 'Blue')
            msg = '==> Cannot name an integer as a tablaname\n'
            errors.append(msg)
            proceed = 0

        except:
            proceed = 1
            

        for i in range(len(varlist)):
            typelist.append([None,None,None])
            
            if varlist[i][0].get() == 'string(varchar)':
                typelist[i][0]= 'varchar(30)'
            else:
                typelist[i][0] = 'int'


            if varlist[i][1].get() == 'None':
                typelist[i][1] = ''
                
            else:
                if hasprimary == 'no':
                    typelist[i][1] = 'Primary key'
                    hasprimary = 'yes'
                else:
                    msg = '==> There cannot be 2 primary keys in a single table, switching to None\n'
                    errors.append(msg)
                    varlist[i][1].set('None')
                    typelist[i][1] = ''
                
            if (self.deflist[i].get() == 'Default value - NULL/0' or self.deflist[i].get().strip() == '') and typelist[i][0] != 'int':
                typelist[i][2] = 'NULL'
                
            elif typelist[i][0] == 'int':
                if (self.deflist[i].get() == 'Default value - NULL/0' or self.deflist[i].get().strip() == ''):
                    typelist[i][2] = '0'

                    
                else:
                    try:
                        defval = self.deflist[i].get().strip().translate({ord(x) : '' for x in unwanted})
                        defval = defval.replace(" ","_")
                        defval = int(defval)
                        typelist[i][2] = defval
                        
                    except:
                        msg = f'==> cannot put a string value {defval} as default value in an integer column type\n'
                        errors.append(msg)
                        proceed = 0

            if i == len(varlist)-1 and len(errors)>1:
                mainproceed = 0
                errormsgs = ''.join(errors)
                messagebox.showinfo('Terminating table creation',errormsgs)
                errors = ['Terminating table creation due to following error/s\n']

            elif i == len(varlist)-1 and len(errors) == 1:
                mainproceed = 1
                proceed = 1
                        
        if proceed == 1 and mainproceed == 1:

            tabname = self.tabname.get().translate({ord(x) : '' for x in unwanted})
            tabname = tabname.strip().replace(" ","_")
            
            for column in range(len(self.columnnamesentry)):

                columnentry = self.columnnamesentry[column][0].get().translate({ord(x) : '' for x in unwanted})
                columnentry = columnentry.strip().replace(" ","_")
                
                
                if column == 0:

                                                
                    if typelist[0][0] == 'int':
                        self.cursor.execute(f'create table {tabname} ({columnentry} {typelist[0][0]} {typelist[0][1]} default {typelist[0][2]} )')
                    else:
                        self.cursor.execute(f'create table {tabname} ({columnentry} {typelist[0][0]} {typelist[0][1]} default "{typelist[0][2]}")')
                            
                else:
                    
                    if typelist[column][0] == 'int':
                        self.cursor.execute(f'alter table {tabname} add {columnentry} {typelist[column][0]} {typelist[column][1]} default {typelist[column][2]}')
                    else:
                        self.cursor.execute(f'alter table {tabname} add {columnentry} {typelist[column][0]} {typelist[column][1]} default "{typelist[column][2]}"')

                if column == len(self.columnnamesentry)-1:
                    self.cursor.execute(f'alter table {tabname} add sthaid int unique key auto_increment')
                else:
                    pass

            for column in range(0,len(self.columnnamesentry)):

                columnentry = self.columnnamesentry[column][0].get().translate({ord(x) : '' for x in unwanted})
                columnentry = columnentry.strip().replace(" ","_")
                
                for row in range(1,len(self.columnnamesentry[0])):

                    columnvalue = self.columnnamesentry[column][row].get().translate({ord(x) : '' for x in unwanted})
                    columnvalue = columnvalue.strip().replace(" ","_")

                    if column != 0:
                        try:
                            if typelist[column][0] != 'int':
                                self.cursor.execute(f'update {tabname} set {columnentry} = "{columnvalue}" where sthaid = {row} ')
                            else:
                                self.cursor.execute(f'update {tabname} set {columnentry} = {columnvalue} where sthaid = {row} ')
                        except:
                            if columnvalue != '':
                                self.columnnamesentry[column][row].config(fg = 'blue')
                            else:
                                self.columnnamesentry[column][row].config(bg = 'blue')

                            if dupboxshown == 0:
                                msg = "==> There can't be duplicate entry in a primary and unique key"
                                errors.append(msg)
                                dupboxshown = 1
                                erroroccured = 1
                            else:
                                pass
                    else:
                        if typelist[0][0] != 'int':
                            self.cursor.execute(f'insert into {tabname}({columnentry}) values("{columnvalue}")')
                        else:
                            try:
                                check = int(self.columnnamesentry[0][row].get())
                                self.cursor.execute(f'insert into {tabname}({columnentry}) values({check})')
                            except:
                                self.columnnamesentry[0][row].config(fg = 'blue')
                                if errorshown == 0:
                                    msg = f'==> Cannot enter a string data type into a column with integer datatype \nor Duplicate entry in {columnentry}'
                                    errors.append(msg)
                                    errorshown = 1
                                    erroroccured = 1
                    
                if column == len(self.columnnamesentry)-1 :

                    if erroroccured == 1 :
                        errormsgs = ''.join(errors)
                        messagebox.showinfo('Invalid values',errormsgs)
                        self.cursor.execute(f'drop table {tabname} ')
                    else:
                        self.cursor.execute(f'alter table {tabname} drop column sthaid ')
                        self.cursor.execute('commit')
                        self.win.destroy()
                        if self.otherself == 'hello':
                            pass
                        else:
                            startfile.tablewin.__init__(self.otherself,self.database,self.cursor)
                        return 1
        
    
    def rest(self,varlist):
        
        Label(self.win, bg = self.themeback, fg = self.fontcolor).grid(column = 100, row = 3)
        Button(self.win, text = 'add new column', width = 15,command = lambda : self.addcolumn(varlist)).grid(column = 101, row = 3)
        
        Label(self.win, bg = self.themeback, fg = self.fontcolor).grid(column = 0, row = 102)
        createtabut = Button(self.win, text = 'create table', width = 15,command = lambda : self.create(varlist))
        createtabut.grid(column = 1, row = 103)

        Label(self.win, bg = self.themeback, fg = self.fontcolor).grid(column = 0, row = self.rowlen+3)
        btn = Button(self.win, text = 'add new row', width = 15, command = lambda : self.addrow(btn))
        btn.grid(column = 0, row = self.rowlen+4)


        

###################################################   CREATING NEW TABLE END   ########################################################

if __name__ == "__main__":
    conn = myc.connect(host = 'localhost', user = 'root', passwd = 'Tiger@12', database = 'stharanzn')
    cursor = conn.cursor()

    createtable('hello','stharanzn',cursor)

