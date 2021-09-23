import tkinter as tk
from tkinter import Text, filedialog, LEFT, TOP, BOTTOM, messagebox, ACTIVE, DISABLED
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style

root = tk.Tk()
# root.geometry("500x500+250+250")
apps = []

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

textFrame = tk.Frame(root, bg="WHITE")
textFrame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

choice4 = tk.Button(root, text="Choice 4", state=ACTIVE, width=10, padx=5, pady=5, fg="white", bg="#263D42", command=choice4)
choice4.pack(side=BOTTOM, padx=10, pady=5)

choice3 = tk.Button(root, text="Choice 3", state=ACTIVE, width=10, padx=5, pady=5, fg="white", bg="#263D42", command=choice3)
choice3.pack(side=BOTTOM, padx=10, pady=5)

choice2 = tk.Button(root, text="Choice 2", state=ACTIVE, width=10, padx=5, pady=5, fg="white", bg="#263D42", command=choice2)
choice2.pack(side=BOTTOM, padx=10, pady=5)

choice1 = tk.Button(root, text="Choice 1", state=ACTIVE, width=10, padx=5, pady=5, fg="white", bg="#263D42", command=choice1)
choice1.pack(side=BOTTOM, padx=10, pady=5)

for app in apps:
    label = tk.Label(frame, text=app)
    label.pack()

root.mainloop()

with open('save.txt', 'w') as f:
    for app in apps:
        f.write(app + ',')