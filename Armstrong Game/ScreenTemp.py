from tkinter import *
import tkinter as tk
from tkinter import Text, filedialog, LEFT, TOP, BOTTOM, messagebox, ACTIVE, DISABLED
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from GameState import GameState
from PlayerValues import PlayerValues

global gameStateNum
global consequence
global collectiblesList
consequence = ""
gameStateNum = 0
# hey there :)

global PlayerValues
PlayerValues = PlayerValues()


def main():
    root = tk.Tk()
    root.geometry("1920x1080")
    root.tk.call('tk', 'scaling', 2.0)
    # gameState1 = GameState(
    #     "You're on the battlefield, soldier. What do you do next?",
    #
    #     "Look for medical items in order to patch up the injured squad.",
    #     "Look for food for yourself - you're famished.",
    #     "You ignore the cabinets and keep walking.",
    #     "This situation is too bleak - make a run for it."
    # )

    gameStateList = [
        GameState(  # gamestate 0
            "You're on the battlefield, soldier. What do you do next?",

            "Look for medical items in order to patch up the injured squad.",
            "Look for food for yourself - you're famished.",
            "You ignore the cabinets and keep walking.",  # result: you step on a wire -1 hp
            "This situation is too bleak - make a run for it."  # death
        ),
        GameState(  # gamestate 1
            "You go back to your squad. You see a strange room, a chest, and a mysterious red button on the wall.",

            "You have your team search around.",
            "Open the chest",
            "Explore the room.",  # choice 3
            "Push the mysterious button."  # death
        ),
        GameState(  # gamestate 2
            "You're now passing the enemy's basecamp. What will you do?",

            "Using a map, you find a soldier's barracks and steal disguises for your team",  # button 1
            "Check out the armory.",  # button 2
            "You don't know what's in there so you avoid it entirely.",  # button 3
            "Try to convince a guard to help you out."  # death
        ),
        GameState(  # gamestate 3
            "You're now at the enemy checkpoint to leave the battlefield. What do you want to do?",  # button 1

            "Your squad puts on disguises and enters the checkpoint office to see if there is anything useful there.",
            # button 2
            "Let's not risk anything and keep moving!",
            "You try to throw a rock at the guards to distract them. ",  # button 3
            "You see a break in the crowd at the checkpoint. Run for it!"  # death
        ),
        GameState(  # gamestate 4
            "You encounter a maze.",

            "Using the map and the key, try to escape!",
            "Use the dynamite to blow through the maze.",
            "Try to make it through the maze blind.",
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

    # myList = [GameState("hi")]

    # global centerMessage
    def updateGameValues():
        if PlayerValues.isDead():
            message = "You died."
            firstChoice = "Restart"
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

        global collectiblesList

        collectiblesList = "Collectibles: \n"

        if PlayerValues.hasBandages():
            collectiblesList += "🩹"

        if PlayerValues.hasFood():
            collectiblesList += "🍞"

        if PlayerValues.hasNormalMap():
            collectiblesList += "🗺"

        if PlayerValues.hasDynamite():
            collectiblesList += "🧨"

        if PlayerValues.hasEscapeMap():
            collectiblesList += "🏃🗺‍"

        if PlayerValues.hasDisguises():
            collectiblesList += "👔"

        if PlayerValues.hasKey():
            collectiblesList += "🗝"

        collectibles.config(text=collectiblesList)

        if gameStateNum == 5 or PlayerValues.isDead():
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=DISABLED)
            choice3Button.config(state=DISABLED)
            choice4Button.config(state=DISABLED)


        elif gameStateNum == 4:
            if not PlayerValues.hasKey():
                choice1Button.config(state=DISABLED)
            if not PlayerValues.hasDynamite():
                choice2Button.config(state=DISABLED)

        elif gameStateNum == 3 and not PlayerValues.hasDisguises():
            choice1Button.config(state=DISABLED)

        elif gameStateNum == 2 and (not PlayerValues.hasNormalMap() and not PlayerValues.hasEscapeMap()):
            choice1Button.config(state=DISABLED)
            choice2Button.config(state=DISABLED)

        elif gameStateNum == 1 and not PlayerValues.hasBandages():
            choice1Button.config(state=DISABLED)

        elif gameStateNum == 0:
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=ACTIVE)
            choice3Button.config(state=ACTIVE)
            choice4Button.config(state=ACTIVE)

        else:
            choice1Button.config(state=ACTIVE)

    def choice1():
        # print("why")
        # message = "You chose Choice 1!"
        # centerTextBox.config(text=message)
        # messagebox.showinfo( "Choice 1", "You choose Choice 1!")
        # choice1.config(text="Test")
        global gameStateNum
        global consequence
        global PlayerValues

        if PlayerValues.isDead():
            # global collectiblesList
            # collectiblesList = "Collectibles: "

            PlayerValues.reset()

            consequence = ""
            gameStateNum = -1

        if gameStateNum == 0:
            consequence = "You find bandages."
            PlayerValues.unlockBandages()

        if gameStateNum == 1:
            consequence = "One of Armstrongs teammates finds an escape map!"
            PlayerValues.unlockEscapeMap()

        if gameStateNum == 2:
            consequence = "You find some clothes you might be able to use as disguises."
            PlayerValues.unlockDisguises()

        if gameStateNum == 3:
            consequence = """You find a key labeled "Emergency Escape Hatch"."""
            PlayerValues.unlockKey()

        if gameStateNum == 4:
            consequence = "You successfully escape!"

        if gameStateNum == 5:
            global collectiblesList
            collectiblesList = "Collectibles: "

            PlayerValues.reset()

            consequence = ""
            gameStateNum = -1

        gameStateNum += 1

        updateGameValues()

    def choice2():
        # message = "You chose Choice 2!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence

        if gameStateNum == 0:
            consequence = "You find some food for your squad. You eat your portion. +1 HP"
            PlayerValues.unlockFood()
            PlayerValues.changeHealth(1)

        if gameStateNum == 1:
            consequence = "You find a normal map."
            PlayerValues.unlockNormalMap()

        if gameStateNum == 2:  # requires escape map OR normal map
            consequence = "You find dynamite!"
            PlayerValues.unlockDynamite()

        if gameStateNum == 3:
            consequence = "Nothing happens - you keep moving."

        if gameStateNum == 4:
            consequence = "You escape with minor injuries but it's only a matter of time before they find you. -1 HP"
            PlayerValues.changeHealth(-1)

        # if gameStateNum == 2:
        #     PlayerValues.unlockDynamite()

        gameStateNum += 1
        updateGameValues()

        # what did you find

    def choice3():
        # message = "You chose Choice 3!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence

        if gameStateNum == 0:
            consequence = "You trip on a wire and are injured by a trap. -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 1:
            consequence = "You find nothing and step on a rusty nail. -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 2:
            consequence = "You step on a rusty nail. -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 3:
            consequence = "It ricochets back at you. -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 4:
            consequence = "You cannot unlock the escape hatch, so get captured by the enemy."
            PlayerValues.die()

        gameStateNum += 1
        updateGameValues()

    def choice4():
        # message = "You chose Choice 4!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence

        if gameStateNum == 0:
            consequence = "You get hit by a motar round. Your bits fly everywhere."

        if gameStateNum == 1:
            consequence = "A self destruct sequences starts and the building blows up. Oof."

        if gameStateNum == 2:
            consequence = "Your convincing skills were subpar. You got captured."

        if gameStateNum == 3:
            consequence = "A grandma beats you to death for cutting in front of her in line."

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
            text=""
        )

        # centerTextBox.
        result.place(relwidth=0.7, relheight=0.05, relx=0.5, rely=0.2, anchor=CENTER)

        health = Label(
            root,
            height=10,
            width=20,
            padx=5,
            pady=5,
            text="Health: " + str(PlayerValues.getHealth())
        )

        # centerTextBox.
        health.place(relwidth=0.1, relheight=0.05, relx=0.1, rely=0.1)

        global collectiblesList
        collectiblesList = "Collectibles: \n"

        collectibles = Label(
            root,
            text=collectiblesList,
            justify=LEFT,
            anchor='n'
        )

        # centerTextBox.
        collectibles.place(relwidth=0.1, relheight=0.076, relx=0.1, rely=0.51)

        buttonWidth = 80

        choice1msg = gameStateList[0].getChoice1()
        choice1Button = tk.Button(root,
                                  text=choice1msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice1)
        choice1Button.place(relx=0.5, rely=0.69, anchor=CENTER)

        choice2msg = gameStateList[0].getChoice2()
        choice2Button = tk.Button(root,
                                  text=choice2msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice2)
        choice2Button.place(relx=0.5, rely=0.76, anchor=CENTER)

        choice3msg = gameStateList[0].getChoice3()
        choice3Button = tk.Button(root,
                                  text=choice3msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice3)
        choice3Button.place(relx=0.5, rely=0.83, anchor=CENTER)

        choice4msg = gameStateList[0].getChoiceDeath()
        choice4Button = tk.Button(root,
                                  text=choice4msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice4)
        choice4Button.place(relx=0.5, rely=0.90, anchor=CENTER)

    root.mainloop()


main()
