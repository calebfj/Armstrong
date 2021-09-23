import tkinter as tk
from tkinter import Text, filedialog
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
import os

root = tk.Tk()
# root.geometry("500x500+250+250")
apps = []

if os.path.isfile('save.txt'):
    with open('save.txt', 'r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        apps = [x for x in tempApps if x.strip()]


def addApp():
    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("executables", "*.exe"), ("all files", "*.*")))
    apps.append(filename)
    print(filename)

    for app in apps:
        label = tk.Label(frame, text=app, bg="white")
        label.pack()


def runApps():
    for app in apps:
        os.startfile(app)


def closeApp():
    exit(0)


canvas = tk.Canvas(root, height=700, width=700, bg="white")
canvas.pack()

frame = tk.Frame(root, bg="#263D42")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

openFile = tk.Button(root, text="Open File", padx=5, pady=2, fg="white", bg="#263D42", command=addApp)
# openFile = tk.Button(self, text="Open File")
openFile.pack(side=RIGHT, padx=10, pady=5)

runApps = tk.Button(root, text="Run Apps", padx=5, pady=2, fg="white", bg="#263D42", command=runApps)
# runApps = tk.Button(self, text="Run Apps")
runApps.pack(side=RIGHT)

closeApp = tk.Button(root, text="CLOSE", padx=5, pady=2, fg="white", bg="#263D42", command=closeApp)
closeApp.pack(side=RIGHT, padx=10, pady=5)

for app in apps:
    label = tk.Label(frame, text=app)
    label.pack()

root.mainloop()

with open('save.txt', 'w') as f:
    for app in apps:
        f.write(app + ',')