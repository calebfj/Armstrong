from tkinter import *

root = Tk()

e = Entry(root, width=50, borderwidth=8)
e.pack()
e.get()
e.insert(0, "Enter Your Name")

def myClick():
    msg = "Hello " + e.get()
    myLabel = Label(root, text=msg)
    myLabel.pack()


myButton = Button(root, text="HI", command=myClick, bg="blue", fg="white")

myButton.pack()


root.mainloop()
