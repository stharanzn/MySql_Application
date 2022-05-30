#tests

import tkinter
from tkinter import *
from tkinter import messagebox

screen = Tk()

def changecolor(btn):
    btn.configure(bg = 'red')

tkvar = StringVar()
choices = {'first','second','third','fourth'}
tkvar.set('first')

fk = StringVar()
fk.set('second')

secmenu = OptionMenu(screen, fk,*choices)
secmenu.pack()

popupmenu = OptionMenu(screen, tkvar, *choices)
Label(screen, text = 'choose it boi').pack()
popupmenu.pack()

def change_dropdown(*args):
    print(tkvar.get())
    text = tkvar.get()
    fktext = fk.get()
    print(text,fktext,'here it is')
    
texts = 'hello'

def p(tkvar,fk,*args):
    global texts
    texts = tkvar.get()
    fktext = fk.get()
    print(texts, fktext)
tkvar.trace('w',lambda a,b,c : p(tkvar,fk))
screen.bind('<w>', p)

btn = Button(screen, text = 'test\n', width = 20, command = lambda : changecolor(btn))
btn.pack()

btn = Button(screen, text = 'test\n', width = 20, command = lambda : p(tkvar,fk))
btn.pack()


fk.trace('q',lambda a,b,c : z(fk))
screen.bind('<q>',z)

screen.mainloop()

class createtable():
    def __init__(self,tabaddbut,cursor):
        tabaddbut.destroy()
        self.win = Tk()
        self.themeback = themeback
        self.fontcolor = fontcolor
        self.win.grab_set()
        self.win.title('Creating table ')
        self.win.config(background = themeback)
        #self.panw = PanedWindow(orient = 'horizontal')
        self.cursor = cursor
        self.takevalues()

    def takevalues(self):
        text = StringVar()
        text.set('tablename')
        Lable(self.win, text = '\nEnter table name ', bg = self.themeback, fg = self.fontcolor, font = 'Agency_fb 12 bold').grid(row = 1, column = 0, columnspan = 2)
        tabname = Entry(self.win, text = text, width = 20)
        tabname.grid(column = 2, row = 1)

op = messagebox.askquestion('delete','you sure',icon = 'warning')
if op == 'yes':
    print('yes')
else:
    print('no')
