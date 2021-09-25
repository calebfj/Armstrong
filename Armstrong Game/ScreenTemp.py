from tkinter import *
import tkinter as tk
from tkinter import Text, filedialog, LEFT, TOP, BOTTOM, messagebox, ACTIVE, DISABLED
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from GameState import GameState
from PlayerValues import PlayerValues

global gameStateNum
global consequence
consequence = ""
gameStateNum = 0
PlayerValues = PlayerValues()


def main():
    root = tk.Tk()

    # gameState1 = GameState(
    #     "You're on the battlefield, soldier. What do you do next?",
    #
    #     "Look for medical items in order to patch up the injured squad.",
    #     "Look for food for yourself - you're famished.",
    #     "You ignore the cabinets and keep walking.",
    #     "This situation is too bleak - make a run for it."
    # )

    gameStateList = [
        GameState(  #gamestate 0
            "You're on the battlefield, soldier. What do you do next?",

            "Look for medical items in order to patch up the injured squad.",
            "Look for food for yourself - you're famished.",
            "You ignore the cabinets and keep walking.",    # result: you step on a wire -1 hp
            "This situation is too bleak - make a run for it."  # death
        ),
        GameState(  #gamestate 1
            "You go back to your squad.",

            "One of Armstrongs teammates finds an escape map in a random corner.",
            "You find the normal map yourself in a random cabinet",
            "You look into an old dusty room where you find nothing and end up stepping on a rusty nail.",
            "You found a random red button on the wall next to a map... Push it?"  # death
        ),
        GameState(  #gamestate 2
            "You're now passing the enemy's basecamp. What will you do?",

            "You find a solider's barracks and steal disguises for your team",  # button 1
            "Find dynamite on the side of an armory.",  # button 2
            "You dont know whats in there so you avoid it entirely.",   # button 3
            "You see a guard out front of the basecamp, maybe try to convince him to help you out?"  # death
        ),
        GameState(  #gamestate 3
            "You're now at the enemy checkpoint to leave the battlefield. What do you want to do?",     # button 1

            "Your squad puts on disguises and enters the checkpoint office to see if there is anything useful there.",  #button 2
            "Lets not risk anything and keep moving!",
            "You try to throw a rock at the guards to distract them, but it ricochets back at you and you take damage. ",   #button 3
            "You see a break in the crowd at the checkpoint. Run for it!"  # death
        ),
        GameState(  #gamestate 4
            "Following the maps or through mere luck you run into what seems to be an escape hatch.",

            "If you have the key and the escape map you can succesfully escape.",
            "Use the dynamite to blow the hatch. You might escape but it's only a matter of time before they find you.",
            "You don't have anything, so you get captured by the enemy once you reach the hatch and do not escape.",
            ""
        ),
        GameState(  # finale
            """End Screen: Displays the following game stats-
                How many collectibles did you get?
                How much health did you end up with?
                Did you save your squad?
                How fast was your game time?""",

            "Restart game",
            "",
            "",
            ""
        )

    ]

    print(gameStateList[0].getMessage())

    # myList = [GameState("hi")]

    # global centerMessage
    def updateGameValues():
        if PlayerValues.isDead():
            message = "You died."
            firstChoice = ""
            secondChoice = ""
            thirdChoice = ""
            deathChoice = ""

        else:
            gameState = gameStateList[gameStateNum]

            message = gameState.getMessage()
            firstChoice = gameState.getChoice1()
            secondChoice = gameState.getChoice2()
            thirdChoice = gameState.getChoice3()
            deathChoice = gameState.getChoiceDeath()


        result.config(text=consequence)

        centerTextBox.config(text=message)
        choice1Button.config(text=firstChoice)
        choice2Button.config(text=secondChoice)
        choice3Button.config(text=thirdChoice)
        choice4Button.config(text=deathChoice)

        health.config(text="Health: " + str(PlayerValues.getHealth()))

        if gameStateNum == 4 and not PlayerValues.hasDynamite():
            choice2Button.config(state=DISABLED)

        if gameStateNum == 1 and not PlayerValues.hasBandages() and not PlayerValues.hasFood():
                # team was too weak to move. you're alone.
            return






    def choice1():
        # print("why")
        # message = "You chose Choice 1!"
        # centerTextBox.config(text=message)
        # messagebox.showinfo( "Choice 1", "You choose Choice 1!")
        # choice1.config(text="Test")
        global gameStateNum

        if gameStateNum == 0:
            global consequence
            consequence = "You find bandages."
            PlayerValues.unlockBandages()

        gameStateNum += 1

        updateGameValues()





    def choice2():
        # message = "You chose Choice 2!"
        # centerTextBox.config(text=message)
        global gameStateNum

        if gameStateNum == 0:
            global consequence
            consequence = "You find some food for your squad. You eat your portion. +1 HP"
            PlayerValues.unlockFood()
            PlayerValues.changeHealth(1)


        # if gameStateNum == 2:
        #     PlayerValues.unlockDynamite()

        gameStateNum += 1
        updateGameValues()

        # what did you find


    def choice3():
        # message = "You chose Choice 3!"
        # centerTextBox.config(text=message)
        global gameStateNum

        if gameStateNum == 0:
            global consequence
            consequence = "You trip on a wire and are injured by a trap. -1 HP"
            PlayerValues.changeHealth(-1)



        gameStateNum += 1
        updateGameValues()

    def choice4():
        # message = "You chose Choice 4!"
        # centerTextBox.config(text=message)
        global gameStateNum

        if gameStateNum == 0:
            global consequence
            consequence = "You get hit by a motar round and die."

        gameStateNum += 1

        PlayerValues.die()

        updateGameValues()

    canvas = tk.Canvas(root, height=700, width=700, bg="white")
    canvas.pack()

    frame = tk.Frame(root, bg="#263D42")
    frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

    textFrame = tk.Frame(root, bg="#406870")
    textFrame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

    textFrame = tk.Frame(root, bg="#263D42")
    textFrame.place(relwidth=0.85, relheight=0.56, relx=0.0735, rely=0.07)

    # set the message

    # centerTextBox.insert('end', centerMessage)

    # centerTextBox.config(state='disabled')

    # gameState is 0

    if gameStateNum == 0:
        centerMessage = gameStateList[0].getMessage()

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

        result = Label(
            root,
            height=10,
            width=10,
            padx=5,
            pady=5,
            text="Result"
        )

        # centerTextBox.
        result.place(relwidth=0.8, relheight=0.05, relx=0.5, rely=0.2, anchor=CENTER)

        health = Label(
            root,
            height=10,
            width=10,
            padx=5,
            pady=5,
            text="Health: " + str(PlayerValues.getHealth())
        )

        # centerTextBox.
        health.place(relwidth=0.1, relheight=0.05, relx=0.1, rely=0.1)

        buttonWidth = 80

        choice1msg = gameStateList[0].getChoice1()
        choice1Button = tk.Button(root, text=choice1msg, state=ACTIVE, width=buttonWidth, padx=5, pady=5, fg="white", bg="#406870",
                            command=choice1)
        choice1Button.place(relx=0.5, rely=0.69, anchor=CENTER)


        choice2msg = gameStateList[0].getChoice2()
        choice2Button = tk.Button(root, text=choice2msg, state=ACTIVE, width=buttonWidth, padx=5, pady=5, fg="white", bg="#406870",
                            command=choice2)
        choice2Button.place(relx=0.5, rely=0.76, anchor=CENTER)

        choice3msg = gameStateList[0].getChoice3()
        choice3Button = tk.Button(root, text=choice3msg, state=ACTIVE, width=buttonWidth, padx=5, pady=5, fg="white", bg="#406870",
                            command=choice3)
        choice3Button.place(relx=0.5, rely=0.83, anchor=CENTER)

        choice4msg = gameStateList[0].getChoiceDeath()
        choice4Button = tk.Button(root, text=choice4msg, state=ACTIVE, width=buttonWidth, padx=5, pady=5, fg="white", bg="#406870",
                            command=choice4)
        choice4Button.place(relx=0.5, rely=0.90, anchor=CENTER)

    if gameStateNum != 0:
        centerTextBox.config(text="lol")
        print("why")

    root.mainloop()


main()
