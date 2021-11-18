import random
from tkinter import *
import tkinter as tk
from tkinter import Text, filedialog, LEFT, TOP, BOTTOM, messagebox, ACTIVE, DISABLED
from tkinter import RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
import keyboard
from RPi import GPIO
from RPLCD import i2c
from gpiozero import LED, Button, LEDBoard
from GameState import GameState
from PlayerValues import PlayerValues
import time

from threading import Thread
from queue import Queue

global paused
global pausedTime
global TimeCheck

TimeCheck = 0
paused = False
pausedTime = 0

global gameStateNum
global consequence
global lcdmessages
global collectiblesList
global numberOfCollected
global amountOfCollect

consequence = ""
gameStateNum = 99

global PlayerValues
global StartTime
PlayerValues = PlayerValues()

BlueLights = LEDBoard(23, 25, 13, 26)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(16, GPIO.IN)

lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'

address = 0x27
port = 1

lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

def congrats(t):
    return t

def main():

    root = tk.Tk()
    root.geometry("1920x1080")
    root.tk.call('tk', 'scaling', 2.0)

    # que = Queue()
    # t = Thread(target=lambda c, arg1: c.put(congrats(arg1)), args=(que, "Congrats!"))
    # t.start()
    # t.join()

    lcd.backlight_enabled

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
            "",

            "Restart game",
            "",
            "",
            ""
        )
    ]

    def relayToTkinterY(channel):
        root.event_generate('<<yellow>>', when='tail')

    def relayToTkinterR(channel):
        if not(gameStateNum == 5 or PlayerValues.isDead()):
            root.event_generate('<<red>>', when='tail')

    def relayToTkinterG(channel):
        if not (gameStateNum == 5 or PlayerValues.isDead()):
            root.event_generate('<<green>>', when='tail')

    def relayToTkinterB(channel):
        if not (gameStateNum == 5 or PlayerValues.isDead()):
            root.event_generate('<<blue>>', when='tail')

    def relayToTkinterS(channel):
        print(pauseButton.grab_status())
        if not (gameStateNum == 5 or PlayerValues.isDead() or pauseButton.gra):
            root.event_generate('<<small>>', when='tail')

    def checkLights(numberOfCollected):
        for x in range(0, numberOfCollected):
            if x == 4:
                break
            else:
                BlueLights.on(x)

    def tick():
        if gameStateNum == 99:
            runningClock.config(text="", bg="#f0f0f0")
            runningClock.after(225, tick)

        elif gameStateNum == 5 or PlayerValues.isDead():
            runningClock.after(225, tick)
        else:
            global pausedTime
            # if paused:
            if not paused:
                global TimeCheck
                TimeCheck = abs(PlayerValues.getStartTime() - time.time() + pausedTime)

            MinuteTime = 0
            SecondTime = TimeCheck

            if TimeCheck >= 60:
                MinuteTime, SecondTime = (TimeCheck // 60, TimeCheck % 60)

            lcd.close(clear=True)
            lcd.write_string(f'{MinuteTime:.0f} minutes')
            lcd.crlf()
            lcd.write_string(f'{SecondTime:.0f} seconds')
            lcd.crlf()

            runningClock.config(text=f"Current Run Time: {MinuteTime:.0f} minutes {SecondTime:.0f} seconds", bg="#f0f0f0")
            runningClock.after(225, tick)

    def pause():
        global paused
        global pausedTime
        global gameStateNum

        if gameStateNum == 99:
            gameStateNum = 0
            PlayerValues.reset()
            updateGameValues()
        elif paused == False:
            choice1Button.config(state=DISABLED)
            choice2Button.config(state=DISABLED)
            choice3Button.config(state=DISABLED)
            choice4Button.config(state=DISABLED)
            paused = True
            pausedTime -= time.time()
        else:
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=ACTIVE)
            choice3Button.config(state=ACTIVE)
            choice4Button.config(state=ACTIVE)
            paused = False
            pausedTime += time.time()

    def keydown(e):
        pause()

    # global centerMessage
    def updateGameValues():
        global collectiblesList, numberOfCollected, pausedTime

        squad = "You did not save your squad!"

        numberOfCollected = 0

        if PlayerValues.hasBandages():
            numberOfCollected += 1
            squad = "You saved your squad!!!"

        if PlayerValues.hasFood():
            numberOfCollected += 1

        if PlayerValues.hasNormalMap():
            numberOfCollected += 1

        if PlayerValues.hasDynamite():
            numberOfCollected += 1

        if PlayerValues.hasEscapeMap():
            numberOfCollected += 1

        if PlayerValues.hasDisguises():
            numberOfCollected += 1

        if PlayerValues.hasKey():
            numberOfCollected += 1

        checkLights(numberOfCollected)

        if PlayerValues.isDead():
            PlayerValues.setEndTime(time.time())
            # m = que.get()
            m = "Congrats!"

            pausedTime = 0
            phealth = len(PlayerValues.getHealth())
            gameState = gameStateList[5]

            GameTime = PlayerValues.getEndTime()
            MinuteTime = 0
            SecondTime = GameTime

            if GameTime >= 60:
                MinuteTime, SecondTime = (GameTime // 60, GameTime % 60)

            message = m + f'\nYou had {phealth:.0f} hearts remaining\nYou got {numberOfCollected:.0f} collectibles\n' + squad + f"\nTotal Run Time: {MinuteTime:.0f} minutes {SecondTime:.0f} seconds"
            firstChoice = gameState.getChoice1()
            secondChoice = gameState.getChoice2()
            thirdChoice = gameState.getChoice3()
            deathChoice = gameState.getChoiceDeath()

        else:
            if gameStateNum == 5:
                PlayerValues.setEndTime(time.time())
                # m = que.get()
                m = "Congrats!"

                pausedTime = 0
                phealth = len(PlayerValues.getHealth())
                gameState = gameStateList[5]

                GameTime = PlayerValues.getEndTime()
                MinuteTime = 0
                SecondTime = GameTime

                if GameTime >= 60:
                    MinuteTime, SecondTime = (GameTime // 60, GameTime % 60)

                message = m + f'\nYou had {phealth:.0f} hearts remaining\nYou got {numberOfCollected:.0f} collectibles\n' + squad + f"\nTotal Run Time: {MinuteTime:.0f} minutes {SecondTime:.0f} seconds"
                firstChoice = gameState.getChoice1()
                secondChoice = gameState.getChoice2()
                thirdChoice = gameState.getChoice3()
                deathChoice = gameState.getChoiceDeath()
            else:
                print(gameStateNum)
                gameState = gameStateList[gameStateNum]

                message = gameState.getMessage()
                firstChoice = gameState.getChoice1()
                secondChoice = gameState.getChoice2()
                thirdChoice = gameState.getChoice3()
                deathChoice = gameState.getChoiceDeath()

        result.config(text=consequence)

        if not gameStateNum == 0:
            lcd.close(clear=True)
            lcd.write_string(lcdmessages)
            lcd.crlf()

        pausemsg = "Pause (Press the small button)"

        centerTextBox.config(text=message)
        choice1Button.config(text=firstChoice)
        choice2Button.config(text=secondChoice)
        choice3Button.config(text=thirdChoice)
        choice4Button.config(text=deathChoice)
        pauseButton.config(text=pausemsg)


        health.config(text="Health: " + str(PlayerValues.getHealth()))

        if gameStateNum == 5 or PlayerValues.isDead():
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=DISABLED)
            choice3Button.config(state=DISABLED)
            choice4Button.config(state=DISABLED)
            pauseButton.config(state=DISABLED)


        elif gameStateNum == 4:
            if not PlayerValues.hasKey():
                choice1Button.config(state=DISABLED)
            if not PlayerValues.hasDynamite():
                choice2Button.config(state=DISABLED)

        elif gameStateNum == 3 and not PlayerValues.hasDisguises():
            choice1Button.config(state=DISABLED)

        elif gameStateNum == 2:
            if not (PlayerValues.hasBandages() and PlayerValues.hasEscapeMap()):
                choice1Button.config(state=DISABLED)
            if not (PlayerValues.hasNormalMap() or PlayerValues.hasEscapeMap()):
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

    def choice1(event):
        # print("why")
        # message = "You chose Choice 1!"
        # centerTextBox.config(text=message)
        # messagebox.showinfo( "Choice 1", "You choose Choice 1!")
        # choice1.config(text="Test")
        global gameStateNum
        global consequence
        global PlayerValues
        global lcdmessages

        if PlayerValues.isDead():
            # global collectiblesList
            # collectiblesList = "Collectibles: "

            PlayerValues.reset()
            numberOfCollected = 0
            BlueLights.off()

            consequence = ""
            gameStateNum = -1

        if gameStateNum == 0:
            consequence = "You find bandages."
            lcdmessages = "You found bandages!"
            PlayerValues.unlockBandages()

        if gameStateNum == 1:
            consequence = "One of Armstrongs teammates finds an escape map!"
            lcdmessages = "You found the escape map!"
            PlayerValues.unlockEscapeMap()

        if gameStateNum == 2:
            consequence = "You find some clothes you might be able to use as disguises."
            lcdmessages = "You found disguises!"
            PlayerValues.unlockDisguises()

        if gameStateNum == 3:
            consequence = """You find a key labeled "Emergency Escape Hatch"."""
            lcdmessages = "You found the Escape Hatch!"
            PlayerValues.unlockKey()

        if gameStateNum == 4:
            consequence = "You successfully escape!"
            lcdmessages = "You escaped!!"

        if gameStateNum == 5:
            global collectiblesList
            collectiblesList = "Collectibles: "

            PlayerValues.reset()
            BlueLights.off()

            consequence = ""
            gameStateNum = -1

        if gameStateNum == 99:
            gameStateNum = 0
            PlayerValues.reset()
        else:
            gameStateNum += 1

        updateGameValues()

    def choice2(event):
        # message = "You chose Choice 2!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence
        global lcdmessages

        if gameStateNum == 0:
            consequence = "You find some food for your squad. You eat your portion. +1 HP"
            lcdmessages = "+1 HP to your Health"
            PlayerValues.unlockFood()
            PlayerValues.changeHealth(1)

        if gameStateNum == 1:
            consequence = "You find a normal map."
            lcdmessages = "You found the normal map!"
            PlayerValues.unlockNormalMap()

        if gameStateNum == 2:  # requires escape map OR normal map
            consequence = "You find dynamite!"
            lcdmessages = "You found the dynamite!"
            PlayerValues.unlockDynamite()

        if gameStateNum == 3:
            consequence = "Nothing happens - you keep moving."

        if gameStateNum == 4:
            consequence = "You escape with minor injuries but it's only a matter of time before they find you. -1 HP"
            lcdmessages = "-1 HP to your Health"
            PlayerValues.changeHealth(-1)

        # if gameStateNum == 2:
        #     PlayerValues.unlockDynamite()

        gameStateNum += 1
        updateGameValues()

        # what did you find

    def choice3(event):
        # message = "You chose Choice 3!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence
        global lcdmessages

        if gameStateNum == 0:
            consequence = "You trip on a wire and you are injured by a trap in the wall. 'ITS A TRAP! AAGH' -1 HP"
            lcdmessages = "-1 HP to your Health"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 1:
            consequence = "You find nothing and step on a rusty nail. 'WHO LEAVES A RUSTY NAIL THERE?' -1 HP"
            lcdmessages = "-1 HP to your Health"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 2:
            consequence = "You step on a rusty nail AGAIN. 'WHO LEAVES TWO RUSTY NAILS ON THE GROUND??' -1 HP"
            lcdmessages = "-1 HP to your Health"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 3:
            consequence = "It ricochets back at you. 'ROCK LEE WHY HAVE YOU FORSAKEN ME' -1 HP"
            lcdmessages = "-1 HP to your Health"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 4:
            consequence = "You cannot unlock the escape hatch, oh no the enemy sees you. Enjoy prison!"
            lcdmessages = "-1 HP to your Health"
            PlayerValues.die()

        gameStateNum += 1
        updateGameValues()

    def choice4(event):
        # message = "You chose Choice 4!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence
        global lcdmessages

        if gameStateNum == 0:
            consequence = "You get hit by a motar round. Your bits fly everywhere."
            lcdmessages = "YOU DIED!"

        if gameStateNum == 1:
            consequence = "A self destruct sequences starts and the building blows up. Oof."
            lcdmessages = "YOU DIED!"

        if gameStateNum == 2:
            consequence = "Your convincing skills were subpar. You got captured."
            lcdmessages = "YOU DIED!"

        if gameStateNum == 3:
            consequence = "A grandma beats you to death for cutting in front of her in line."
            lcdmessages = "YOU DIED!"

        gameStateNum += 1

        PlayerValues.die()

        updateGameValues()

    canvas = tk.Canvas(root, height=700, width=700, bg="#f0f0f0")
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

    if gameStateNum == 99:
        # global pausedTime
        # pausedTime += time.time()

        centerMessage = 'Press "Start" to start! (Press smalled Button)'

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
        collectiblesList = ""

        collectibles = Label(
            root,
            text=collectiblesList,
            justify=LEFT,
            anchor='n'
        )

        # centerTextBox.
        collectibles.place(relwidth=0.1, relheight=0.076, relx=0.1, rely=0.51)

        buttonWidth = 80

        posy_choices = [0.69, 0.76, 0.83, 0.90]
        # random.shuffle(posy_choices)
        # print(posy_choices[1])

        choice1msg = "Start"
        choice1Button = tk.Button(root,
                                  text=choice1msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice1)
        choice1Button.place(relx=0.5, rely=posy_choices[0], anchor=CENTER)

        choice2msg = ""
        choice2Button = tk.Button(root,
                                  text=choice2msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice2)
        choice2Button.place(relx=0.5, rely=posy_choices[1], anchor=CENTER)

        choice3msg = ""
        choice3Button = tk.Button(root,
                                  text=choice3msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice3)
        choice3Button.place(relx=0.5, rely=posy_choices[2], anchor=CENTER)

        choice4msg = ""
        choice4Button = tk.Button(root,
                                  text=choice4msg,
                                  state=ACTIVE,
                                  width=buttonWidth,
                                  padx=5, pady=5,
                                  fg="black",
                                  bg="#f0f0f0",
                                  command=choice4)
        choice4Button.place(relx=0.5, rely=posy_choices[3], anchor=CENTER)

        #"Pause (Press the small button)"
        pausemsg = ""
        pauseButton = tk.Button(root,
                                text=pausemsg,
                                state=ACTIVE,
                                width=30,
                                padx=5, pady=5,
                                fg="black",
                                bg="#f0f0f0",
                                command=pause)
        pauseButton.place(relx=0.5, rely=0.97, anchor=CENTER)

        #Temp until we can forward it to LCD
        runningClock = Label(root,
                             font=("times", 10, "bold"),
                             bg="#406870")
        runningClock.place(relx=0.4, rely=0.01)

    GPIO.add_event_detect(17, GPIO.RISING, callback=relayToTkinterY, bouncetime=300) #Yellow Button
    GPIO.add_event_detect(22, GPIO.RISING, callback=relayToTkinterR, bouncetime=300) #Red Button
    GPIO.add_event_detect(27, GPIO.RISING, callback=relayToTkinterG, bouncetime=300) #Green Button
    GPIO.add_event_detect(24, GPIO.RISING, callback=relayToTkinterB, bouncetime=300) #Blue Button
    GPIO.add_event_detect(16, GPIO.RISING, callback=relayToTkinterS, bouncetime=300) #Small Button

    root.bind('<<yellow>>', choice1)
    root.bind('<<red>>', choice2)
    root.bind('<<green>>', choice3)
    root.bind('<<blue>>', choice4)
    root.bind('<<small>>', keydown)

    tick()

    frame = Frame(root, width=0, height=0)
    frame.pack()
    frame.focus_set()
    root.mainloop()

main()
