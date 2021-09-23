from tkinter import *
import tkinter as tk
from tkinter import Text, filedialog, LEFT, TOP, BOTTOM, messagebox, ACTIVE, DISABLED
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style


root = tk.Tk()



# global centerMessage
def choice1():
    message = "You chose Choice 1!"
    centerTextBox.config(text=message)
    # messagebox.showinfo( "Choice 1", "You choose Choice 1!")
    choice1.config(text="Test")


def choice2():
    message = "You chose Choice 2!"
    centerTextBox.config(text=message)


def choice3():
    message = "You chose Choice 3!"
    centerTextBox.config(text=message)


def choice4():
    message = "You chose Choice 4!"
    centerTextBox.config(text=message)


canvas = tk.Canvas(root, height=700, width=700, bg="white")
canvas.pack()

frame = tk.Frame(root, bg="#263D42")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

textFrame = tk.Frame(root, bg="#406870")
textFrame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

textFrame = tk.Frame(root, bg="#263D42")
textFrame.place(relwidth=0.85, relheight=0.56, relx=0.0735, rely=0.07)

centerMessage = '''
    This text box will act as the main text screen for dialog communication between the player and game
     events.

    Choice 1: Enter the building

    Choice 2: Pick up the box

    Choice 3: Run back to your squad

    Choice 4: Make a text based video game
'''

centerTextBox = Label(
    root,
    height=100,
    width=100,
    padx=30,
    pady=10,
    text=centerMessage
)

# centerTextBox.
centerTextBox.place(relwidth=0.8, relheight=0.5, relx=0.0959, rely=0.095)
# centerTextBox.insert('end', centerMessage)


# centerTextBox.config(state='disabled')

choice1msg = "Look for medical items in order to patch up the injured squad."
choice1 = tk.Button(root, text=choice1msg, state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870",
                    command=choice1)
choice1.place(relx=0.25, rely=0.67)

choice2msg = "Look for food for yourself - you're famished."
choice2 = tk.Button(root, text=choice2msg, state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870",
                    command=choice2)
choice2.place(relx=0.25, rely=0.74)

choice3msg = "You ignore the cabinets and keep walking."
choice3 = tk.Button(root, text=choice3msg, state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870",
                    command=choice3)
choice3.place(relx=0.25, rely=0.81)

choice4msg = "This situation is too bleak - make a run for it."
choice4 = tk.Button(root, text=choice4msg, state=ACTIVE, width=50, padx=5, pady=5, fg="white", bg="#406870",
                    command=choice4)
choice4.place(relx=0.25, rely=0.88)



root.mainloop()
