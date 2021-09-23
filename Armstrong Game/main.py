from tkinter import *

root = Tk()
root.title("Game GUI")

def choice1():
    return

def choice2():
    return

def choice3():
    return

button_choice1 = Button(root, text="Choice 1", padx=40, pady=20, command=choice1)
button_choice1.grid(row=3, column=0)

button_choice2 = Button(root, text="Choice 2", padx=40, pady=20, command=choice3)
button_choice2.grid(row=3, column=1)

button_choice3 = Button(root, text="Choice 3", padx=40, pady=20, command=choice3)
button_choice3.grid(row=3, column=2)

root.mainloop()