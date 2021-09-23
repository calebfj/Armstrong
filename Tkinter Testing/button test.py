from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="gotem")
    myLabel.pack()

# myButton = Button(root, text="HI", state=DISABLED)
# myButton = Button(root, text="HI", padx=50, pady=50, command=myClick())
# myButton = Button(root, text="HI", command=myClick, bg="blue", fg="white") #you can use hex codes
myButton = Button(root, text="HI", command=myClick, bg="blue", fg="white")

myButton.pack()


root.mainloop()
