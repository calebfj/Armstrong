import tkinter as tk
from tkinter import Text, filedialog, LEFT, TOP, BOTTOM, messagebox, ACTIVE, DISABLED
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style

root = tk.Tk()

def choice1():
    messagebox.showinfo( "Choice 1", "You choose Choice 1!")

def choice2():
    messagebox.showinfo( "Choice 2", "You choose Choice 2!")

def choice3():
    messagebox.showinfo( "Choice 3", "You choose Choice 3!")

def choice4():
    messagebox.showinfo( "Choice 4", "You choose Choice 4!")

canvas = tk.Canvas(root, height=700, width=700, bg="white")
canvas.pack()

frame = tk.Frame(root, bg="#263D42")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

textFrame = tk.Frame(root, bg="#406870")
textFrame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

textFrame = tk.Frame(root, bg="#263D42")
textFrame.place(relwidth=0.85, relheight=0.56, relx=0.0735, rely=0.07)

centerTextBox = Text(
    root,
    height = 100,
    width = 100,
    padx = 30,
    pady = 10
)

centerMessage = '''
    This text box will act as the main text screen for dialog communication between the player and game events.
    
    Choice 1: Enter the building
    
    Choice 2: Pick up the box
    
    Choice 3: Run back to your squad
    
    Choice 4: Make a text based video game
'''

centerTextBox.place(relwidth=0.8, relheight=0.5, relx=0.0959, rely=0.095)
centerTextBox.insert('end', centerMessage)
centerTextBox.config(state='disabled')

choice4 = tk.Button(root, text="Choice 4", state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870", command=choice4)
choice4.place(relx=0.25, rely=0.88)

choice3 = tk.Button(root, text="Choice 3", state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870", command=choice3)
choice3.place(relx=0.25, rely=0.81)

choice2 = tk.Button(root, text="Choice 2", state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870", command=choice2)
choice2.place(relx=0.25, rely=0.74)

choice1 = tk.Button(root, text="Choice 1", state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870", command=choice1)
choice1.place(relx=0.25, rely=0.67)

root.mainloop()
