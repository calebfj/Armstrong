from tkinter import *

root = Tk()
root.title("Game GUI")

myLabel = Label(root, text = "")
myLabel.grid(row=0, column=0)

def choice1():
    msg = "You picked choice 1!"
    myLabel = Label(root, text=msg)
    myLabel.grid(row=0, column=0)

def choice2():
    msg = "You picked choice 2!"
    myLabel = Label(root, text=msg)
    myLabel.grid(row=0, column=0)

def choice3():
    msg = "You picked choice 3!"
    myLabel = Label(root, text=msg)
    myLabel.grid(row=0, column=0)

button_choice1 = Button(root, text="Choice 1", padx=40, pady=20, command=choice1)
button_choice1.grid(row=1, column=0)

button_choice2 = Button(root, text="Choice 2", padx=40, pady=20, command=choice2)
button_choice2.grid(row=1, column=1)

button_choice3 = Button(root, text="Choice 3", padx=40, pady=20, command=choice3)
button_choice3.grid(row=1, column=2)

root.mainloop()