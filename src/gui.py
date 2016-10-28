from Tkinter import *

def show_values():
    print (w1.get(), w2.get())

master = Tk()
w1 = Scale(master, from_=0, to=100, tickinterval=0.1, length=300)
w1.pack(side=LEFT)
w2 = Scale(master, from_=0, to=100, tickinterval=0.1, length=300)
w2.pack(side=LEFT)
Button(master, text='Show', command=show_values).pack()

while True:
    show_values()
    master.update()