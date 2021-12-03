from tkinter import *
import tkinter as tk
from tkinter import LEFT, ACTIVE, DISABLED
from tkinter.ttk import Frame
from RPi import GPIO
from RPLCD import i2c
from gpiozero import LEDBoard
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

global yellowIsDisabled
global redIsDisabled
global greenIsDisabled
global blueIsDisabled
global smallIsDisabled


# The following code statements are utilized to setup the reference for the 16x2 LCD Screen's object. This object has multiple methods that allow
# us to send string data to the screen, manage format of on screen data and manage the screen itself (Such as cutting the screen on or off based on user activity).
# These variables are primarily meant to map the LCD's designation within the PI in order for the device to be recongized by the PI, as well as designate the specific
# output format the LCD will be managed through.
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'

address = 0x27
port = 1

# This statement creates the intractable LCD reference object utilizing the above variables.
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

# The congrats method is a formal method that is utilized by the thread library as a callback method
# with its only function being that it returns its argument parameter.
def congrats(t):
    return t

def main():
    # Since we utilize a ton of methods to create our useable game environment, globals are utilizied extensively to allow for references to the same variable across methods and
    # classes. Although, if we had more time we would move a lot of these variables into their own classes to help clean up the code.
    global yellowIsDisabled
    global redIsDisabled
    global greenIsDisabled
    global blueIsDisabled
    global smallIsDisabled
    global m

    # These methods check if the game is in its prestart gamestate (99), which is basically just the start menu for the game. If it detects that the gamestate is still at its
    # default 99 value, then it will disable buttons so that no conflicts can occur if a player clicks any other button besides the start button. So when in gamestate 99 the
    # pause button is the only activated button and in any other situation all other buttons would be activated.
    if gameStateNum == 99:
        yellowIsDisabled = True
        redIsDisabled = True
        greenIsDisabled = True
        blueIsDisabled = True
        smallIsDisabled = False
    else:
        yellowIsDisabled = False
        redIsDisabled = False
        greenIsDisabled = False
        blueIsDisabled = False
        smallIsDisabled = False

    # These 3 statements setup the baseline portion of our GUI, with the root object acting as the reference for our GUI as a whole. Any changes to the GUI will call on
    # this root object in order to change or update information since anything outside of this object will be ignored by the Tkinter library while running the GUI's
    # thread. In this case, we set the root object to a default 1920x1080 screen resolution and have it set to scale with the size of any monitor or output device it runs on.
    root = tk.Tk()
    root.geometry("1920x1080")
    root.tk.call('tk', 'scaling', 2.0)

    # These statements are the bread and butter to our threading management outside of the Tkinter library. In this case we are utilizing the Python library,
    # in order to create a thread que where a thread is initialized utilizing the callback congrats method and will be storing the "Congrats!" string data. After the thread
    # has ran, its data is grabbed from the que and stored within global variable m.
    que = Queue()
    t = Thread(target=lambda c, arg1: c.put(congrats(arg1)),args=(que,"Congrats!"))
    t.start()
    t.join()
    m = que.get()

    # This enables the LCD screen upon main method initialization
    lcd.backlight_enabled

    # GameState methods are essentially containers for each game scenario. Using this list,
    # we can iterate the gameStateNum variable to move on to the next scenario.
    gameStateList = [
        GameState(  # gamestate 0
            "You're on the battlefield, soldier. What do you do next?",  # prompt

            "Look for medical items in order to patch up the injured squad.",  # result: hasSquad()
            "Look for food for yourself - you're famished.",    # result: hasFood()
            "You ignore the cabinets and keep walking.",  # result: you step on a wire -1 hp
            "This situation is too bleak - make a run for it."  # death
        ),
        GameState(  # gamestate 1
            "You go back to your squad. You see a strange room, a chest, and a mysterious red button on the wall.",  # prompt

            "You have your team search around.",
            "Open the chest",
            "Explore the room.",  # choice 3
            "Push the mysterious button."  # death
        ),
        GameState(  # gamestate 2
            "You're now passing the enemy's basecamp. What will you do?",  # prompt

            "Using a map, you find a soldier's barracks and steal disguises for your team",  # button 1
            "Check out the armory.",  # button 2
            "You don't know what's in there so you avoid it entirely.",  # button 3
            "Try to convince a guard to help you out."  # death
        ),
        GameState(  # gamestate 3
            "You're now at the enemy checkpoint to leave the battlefield. What do you want to do?",  # prompt

            "Your squad puts on disguises and enters the checkpoint office to see if there is anything useful there.",
            # button 2
            "Let's not risk anything and keep moving!",
            "You try to throw a rock at the guards to distract them. ",  # button 3
            "You see a break in the crowd at the checkpoint. Run for it!"  # death
        ),
        GameState(  # gamestate 4
            "You encounter a maze.",  # prompt

            "Using the map and the key, try to escape!",  # Good option
            "Use the dynamite to blow through the maze.",  # Less good option
            "Try to make it through the maze blind.",  # Death ending
            ""
        ),
        GameState(  # finale
            "",

            "Restart game", # Restart game option
            "",
            "",
            ""
        )
    ]

    # These relay methods take in the input from the GPIO handler as a "channel" and then generate a virtual event within the
    # root's main thread which is detected and then interrupts the main thread to execute a specific action, in our case
    # an action would be the choice1, choice2, choice3, choice4 or pause buttons being clicked. After the interruption the thread is
    # reinstated and continues to run until the next virtual event.

    # Relay method to the yellow button on the PI Controller
    def relayToTkinterY(channel):
        if not yellowIsDisabled:
            root.event_generate('<<yellow>>', when='tail')

    # Relay method to the red button on the PI Controller
    def relayToTkinterR(channel):
        if not(gameStateNum == 5 or PlayerValues.isDead() or redIsDisabled):
            root.event_generate('<<red>>', when='tail')

    # Relay method to the green button on the PI Controller
    def relayToTkinterG(channel):
        if not (gameStateNum == 5 or PlayerValues.isDead() or greenIsDisabled):
            root.event_generate('<<green>>', when='tail')

    # Relay method to the blue button on the PI Controller
    def relayToTkinterB(channel):
        if not (gameStateNum == 5 or PlayerValues.isDead() or blueIsDisabled):
            root.event_generate('<<blue>>', when='tail')

    # Relay method to the small/pause button on the PI Controller
    def relayToTkinterS(channel):
        if not (gameStateNum == 5 or PlayerValues.isDead() or smallIsDisabled):
            root.event_generate('<<small>>', when='tail')

    # This method is the handler utilized to light up the on board LCD bulbs based on numberOfCollected's value. Although logically, a player should not be able to collect
    # more then 4 collectibles at a time, the method still checks for a max limit of 4 when being utilized. This is done in order to stop the program from hitting a null pointer error
    # when it tries to light up a 5th bulb that does not exist.
    def checkLights(numberOfCollected):
        for x in range(0, numberOfCollected):
            if x == 4:
                break
            else:
                BlueLights.on(x)

    # The tick method does not take in any specific parameters, however it does act as an interrupt method within the Tkinter GUI loop in order to keep track of the current
    # running time within the specific user's game. This method parses out a string output to send to both the Tkinter GUI and LCD Screen every time the tick method updates the
    # internal game clock. With the flow of it stopping during a pause screen event, and resumed once the event is over.
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

            # The following is an example of how the LCD Screen object is utlized to send data into the 16x2 LCD screen. In this case, string formating and
            # the write_string command were used in order to output string data onto the lcd during each tick method iteration. The close method is utilized to clear off the screen of
            # any previous string texts so that no string data errors are caused during output by previous outputs and the .crtlf method is a line feed method that sends the data off
            # towards the LCD screen for output.
            lcd.close(clear=True)
            lcd.write_string(f'{MinuteTime:.0f} minutes')
            lcd.crlf()
            lcd.write_string(f'{SecondTime:.0f} seconds')
            lcd.crlf()

            runningClock.config(text=f"Current Run Time: {MinuteTime:.0f} minutes {SecondTime:.0f} seconds", bg="#f0f0f0")
            runningClock.after(225, tick)

    # This method activates when the player activates the pause_button and takes in no parameters. This function primarily handles
    # updating game values when the game is starting for the first time (Since start menu utilizes the same button as the pause menu)
    # and updating key GUI centric varibles such as boolean variables concerning which buttons are disabled from use and in-game time.
    def pause():
        global paused
        global pausedTime
        global gameStateNum
        global yellowIsDisabled
        global redIsDisabled
        global greenIsDisabled
        global blueIsDisabled
        global smallIsDisabled

        # the 99 gameStateNum is the paused gameState
        if gameStateNum == 99:
            gameStateNum = 0
            PlayerValues.reset()
            updateGameValues()

        # if the game isn't paused, then the user is trying to pause.
        elif paused == False:
            choice1Button.config(state=DISABLED)
            choice2Button.config(state=DISABLED)
            choice3Button.config(state=DISABLED)
            choice4Button.config(state=DISABLED)

            yellowIsDisabled = True
            redIsDisabled = True
            greenIsDisabled = True
            blueIsDisabled = True

            paused = True
            pausedTime -= time.time()

        # if the game IS paused, then the user is trying to unpause the game.
        else:
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=ACTIVE)
            choice3Button.config(state=ACTIVE)
            choice4Button.config(state=ACTIVE)

            yellowIsDisabled = False
            redIsDisabled = False
            greenIsDisabled = False
            blueIsDisabled = False

            paused = False
            pausedTime += time.time()

    # This is a passthrough method used to call upon the pause function when a keydown is detected. It was primarily used during debugging and development
    # on windows, however not it serves no functionality when paired with the controller.
    def keydown(e):
        pause()

    # This method will update various game values, as well as on-screen
    # GUI labels and buttons, depending on both the gameState and the choices
    # the player has made so far.
    def updateGameValues():
        global collectiblesList, numberOfCollected, pausedTime, yellowIsDisabled, redIsDisabled, greenIsDisabled, blueIsDisabled, smallIsDisabled, m

        # Current squad value that is utilized at the end of the game to notify you if you saved your squad or not
        squad = "You did not save your squad!"

        # This is a running total value that tracks how many collectibles the player has and is recalculated everytime a updateGameValues method is called.
        numberOfCollected = 0

        # Although there are more efficent methods of doing this, the idea is that the program is checking everytime the game updates, whether the player has specific
        # collectibles, and if so it adds +1 to the numberOfCollected variable. And in cases such as hasBandages, it will also change the outcome concerning if
        # the player saved their squad or not.
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

        # Once collectibles have been checked, the final numberOfCollected value is sent to the checkLights method to turn on the appropriate
        # amount of the LCD Bulbs based on the value.
        checkLights(numberOfCollected)

        # This if statement checks if the player has died within the game due to a consequence. If this does occur,
        # the game will then reset the player's values, as well as prepare the game's end screen value.
        if PlayerValues.isDead():
            PlayerValues.setEndTime(time.time()) #This setEndTime method simply records the exact clock time the player finished, this can either be from game death or escape

            pausedTime = 0 # Pause time is set to 0 for the next game
            phealth = len(PlayerValues.getHealth()) # Player total health is calculated
            gameState = gameStateList[5] # Gamestate is updated to death state

            GameTime = PlayerValues.getEndTime() # Total time is retrieved from the player's earlier set end time
            MinuteTime = 0
            SecondTime = GameTime

            # This if statement formats out the game time into minutes and seconds
            if GameTime >= 60:
                MinuteTime, SecondTime = (GameTime // 60, GameTime % 60)

            # This group of statements handles the string text that will be sent for the player to view at the end of the game after a player death.
            # It will update the choices based on the current gameState, update the LCD's text and push a string message into the message varibles
            # that will be outputted in the end screen.
            message = f'\nYou had {phealth:.0f} hearts remaining\nYou got {numberOfCollected:.0f} collectibles\n' + squad + f"\nTotal Run Time: {MinuteTime:.0f} minutes {SecondTime:.0f} seconds"
            firstChoice = gameState.getChoice1()
            secondChoice = gameState.getChoice2()
            thirdChoice = gameState.getChoice3()
            deathChoice = gameState.getChoiceDeath()
            lcdmessages = "YOU DIED!!!"

        else:
            # If the player did not die, but the gameState was updated to 5. This means they have finished the game and received one of the multiple endings.
            if gameStateNum == 5:
                PlayerValues.setEndTime(time.time()) #This setEndTime method simply records the exact clock time the player finished

                pausedTime = 0  # Pause time is set to 0 for the next game
                phealth = len(PlayerValues.getHealth())  # Player total health is calculated
                gameState = gameStateList[5]  # Gamestate is updated to death state

                GameTime = PlayerValues.getEndTime()  # Total time is retrieved from the player's earlier set end time
                MinuteTime = 0
                SecondTime = GameTime

                # This if statement formats out the game time into minutes and seconds
                if GameTime >= 60:
                    MinuteTime, SecondTime = (GameTime // 60, GameTime % 60)

                # This group of statements handles the string text that will be sent for the player to view at the end of the game.
                # It will update the choices based on the current gameState, update the LCD's text and push a string message into the message varibles
                # that will be outputted in the end screen.
                message = m + f'\nYou had {phealth:.0f} hearts remaining\nYou got {numberOfCollected:.0f} collectibles\n' + squad + f"\nTotal Run Time: {MinuteTime:.0f} minutes {SecondTime:.0f} seconds"
                firstChoice = gameState.getChoice1()
                secondChoice = gameState.getChoice2()
                thirdChoice = gameState.getChoice3()
                deathChoice = gameState.getChoiceDeath()
                lcdmessages = "You escaped!!!"
            else:
                # If the player has not escaped or died, the game will simply update the next screen's options and push the next gameState values onto
                # the GUI.
                print(gameStateNum)
                gameState = gameStateList[gameStateNum] # New gameState is retrieved

                # Main text box values and game option values are updated based on the new gameState
                message = gameState.getMessage()
                firstChoice = gameState.getChoice1()
                secondChoice = gameState.getChoice2()
                thirdChoice = gameState.getChoice3()
                deathChoice = gameState.getChoiceDeath()

        result.config(text=consequence)

        # If the user has finished the game or died, clear the LCDs.
        if gameStateNum == 5 or PlayerValues.isDead():
            lcd.close(clear=True)
            lcd.write_string(lcdmessages)
            lcd.crlf()

        # This statement initializes the pause button's text
        pausemsg = "Pause (Press the small button)"

        # This set of statements update the GUI elements
        centerTextBox.config(text=message)
        choice1Button.config(text=firstChoice)
        choice2Button.config(text=secondChoice)
        choice3Button.config(text=thirdChoice)
        choice4Button.config(text=deathChoice)
        pauseButton.config(text=pausemsg)

        yellowIsDisabled = False
        redIsDisabled = False
        greenIsDisabled = False
        blueIsDisabled = False
        smallIsDisabled = False

        # Dynamically updates the health bar based on the user's current HP
        health.config(text="Health: " + str(PlayerValues.getHealth()))  

        # If the game has ended or the player has died, only the first button (Start) 
        # should be clickable, so this set of statements disables all but the first button.
        if gameStateNum == 5 or PlayerValues.isDead():
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=DISABLED)
            choice3Button.config(state=DISABLED)
            choice4Button.config(state=DISABLED)
            pauseButton.config(state=DISABLED)

            yellowIsDisabled = False
            redIsDisabled = True
            greenIsDisabled = True
            blueIsDisabled = True
            smallIsDisabled = True


        elif gameStateNum == 4:
            # If the player does not have a key, the first choice for scenario (gameState) 4 is locked to them.
            if not PlayerValues.hasKey(): 
                choice1Button.config(state=DISABLED)
                yellowIsDisabled = True

            # If the player does not have dynamite, the second choice for scenario (gameState) 4 is locked to them.
            if not PlayerValues.hasDynamite():
                choice2Button.config(state=DISABLED)
                redIsDisabled = True
                
            blueIsDisabled = True

        elif gameStateNum == 3 and not PlayerValues.hasDisguises():
            # If the player does not have dynamite, the first choice for scenario (gameState) 3 is locked to them.
            choice1Button.config(state=DISABLED)
            yellowIsDisabled = True

        elif gameStateNum == 2:
            # If the player does not have bandages, the first choice for scenario (gameState) 2 is locked to them.
            if not (PlayerValues.hasBandages() and PlayerValues.hasEscapeMap()):
                choice1Button.config(state=DISABLED)
                yellowIsDisabled = True

            # If the player does not have the Normal Map, the second choice for scenario (gameState) 2 is locked to them.
            if not (PlayerValues.hasNormalMap() or PlayerValues.hasEscapeMap()):
                choice2Button.config(state=DISABLED)
                redIsDisabled = True
            
        # If the player does not have bandages, the first choice for scenario (gameState) 1 is locked to them.
        elif gameStateNum == 1 and not PlayerValues.hasBandages():
            choice1Button.config(state=DISABLED)
            yellowIsDisabled = True

        # gameState 0 indicates the game has just begun, so all buttons should be made active - all choices are available
        # in this first (0th) scenario.
        elif gameStateNum == 0:
            choice1Button.config(state=ACTIVE)
            choice2Button.config(state=ACTIVE)
            choice3Button.config(state=ACTIVE)
            choice4Button.config(state=ACTIVE)
            pauseButton.config(state=ACTIVE)

            yellowIsDisabled = False
            redIsDisabled = False
            greenIsDisabled = False
            blueIsDisabled = False
            smallIsDisabled = False

        # The gameState must be 99, which indicates that the game hasn't started yet, so the first option (Start) must
        # be made available to the user.
        else:
            choice1Button.config(state=ACTIVE)
            yellowIsDisabled = False

    # The method for the first choice button. This method will check which gameState the user is in
    # and react accordingly.
    def choice1(event):
        global gameStateNum
        global consequence
        global PlayerValues

        # If the player is dead, all of their values along with the game values are wiped.
        if PlayerValues.isDead():
            PlayerValues.reset()
            numberOfCollected = 0
            BlueLights.off()

            consequence = ""
            gameStateNum = -1

        # Check which scenario the user was in when they clicked the button and give them the corresponding
        # consequence to display and update their player values.
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

        # The player has escaped, the game is over. Reset all values.
        if gameStateNum == 5:
            global collectiblesList
            collectiblesList = "Collectibles: "

            PlayerValues.reset()
            BlueLights.off()

            consequence = ""
            gameStateNum = -1

        # The game is over and the user has clicked "Restart", so the game is reset by wiping all
        # game values and bringing the user back to the first scenario (gameState 0)
        if gameStateNum == 99:
            gameStateNum = 0
            PlayerValues.reset()
        else:
            gameStateNum += 1

        # Update all game values
        updateGameValues()

    # The method for the second choice button. This method will check which gameState the user is in
    # and react accordingly.
    def choice2(event):
        # message = "You chose Choice 2!"
        # centerTextBox.config(text=message)
        global gameStateNum
        global consequence

        # Check which scenario the user was in when they clicked the button and give them the corresponding
        # consequence to display and update their player values.
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

        # Iterate the gameState
        gameStateNum += 1

        # Update all game values
        updateGameValues()

    # The method for the third choice button. This method will check which gameState the user is in
    # and react accordingly.
    def choice3(event):
        global gameStateNum
        global consequence

        # Check which scenario the user was in when they clicked the button and give them the corresponding
        # consequence to display and update their player values.
        if gameStateNum == 0:
            consequence = "You trip on a wire and you are injured by a trap in the wall. 'ITS A TRAP! AAGH' -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 1:
            consequence = "You find nothing and step on a rusty nail. 'WHO LEAVES A RUSTY NAIL THERE?' -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 2:
            consequence = "You step on a rusty nail AGAIN. 'WHO LEAVES TWO RUSTY NAILS ON THE GROUND??' -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 3:
            consequence = "It ricochets back at you. 'ROCK LEE WHY HAVE YOU FORSAKEN ME' -1 HP"
            PlayerValues.changeHealth(-1)

        if gameStateNum == 4:
            consequence = "You cannot unlock the escape hatch, oh no the enemy sees you. Enjoy prison!"
            PlayerValues.die()

        # Iterate the gameState
        gameStateNum += 1

        # Update all game values
        updateGameValues()

    # The method for the fourth choice button. This method will check which gameState the user is in
    # and react accordingly.
    def choice4(event):
        global gameStateNum
        global consequence

        # Check which scenario the user was in when they clicked the button and give them the corresponding
        # consequence to display and update their player values.
        if gameStateNum == 0:
            consequence = "You get hit by a motar round. Your bits fly everywhere."

        if gameStateNum == 1:
            consequence = "A self destruct sequences starts and the building blows up. Oof."

        if gameStateNum == 2:
            consequence = "Your convincing skills were subpar. You got captured."

        if gameStateNum == 3:
            consequence = "A grandma beats you to death for cutting in front of her in line."

        gameStateNum += 1

        # Since this is the button that causes death, the user always dies after clicking it.
        PlayerValues.die()

        # Update all game values
        updateGameValues()


    # This set of statements initializes and places the main background screen elements that the other elements
    # will be placed on.
    canvas = tk.Canvas(root, height=700, width=700, bg="#f0f0f0")
    canvas.pack()

    frame = tk.Frame(root, bg="#263D42")
    frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

    textFrame = tk.Frame(root, bg="#406870")
    textFrame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

    textFrame = tk.Frame(root, bg="#263D42")
    textFrame.place(relwidth=0.85, relheight=0.56, relx=0.0735, rely=0.07)


    # If the gameState is such that the game has just begun, create all of the screen elements
    # and set their values such that they are all in the correct positions on the screen and all
    # buttons upon interaction will react with the correct methods.
    if gameStateNum == 99:
        centerMessage = 'Press "Start" to start! (Press smalled Button)'

        # Initialize the GUI element with the height, width, and text set.
        centerTextBox = Label(
            root,
            height=100,
            width=100,
            padx=30,
            pady=10,
            text=centerMessage
        )
        # Place the GUI element on the screen
        centerTextBox.place(relwidth=0.8, relheight=0.5, relx=0.0959, rely=0.095)

        # Initialize the GUI element with the height, width, and text set.
        result = Label(
            root,
            height=10,
            width=10,
            padx=5,
            pady=5,
            text=""
        )

        # Place the GUI element on the screen
        result.place(relwidth=0.7, relheight=0.05, relx=0.5, rely=0.2, anchor=CENTER)

        # Initialize the GUI element with the height, width, and text set.
        health = Label(
            root,
            height=10,
            width=20,
            padx=5,
            pady=5,
            text="Health: " + str(PlayerValues.getHealth())
        )

        # Place the GUI element on the screen
        health.place(relwidth=0.1, relheight=0.05, relx=0.1, rely=0.1)

        global collectiblesList
        collectiblesList = ""

        # Initialize the GUI element with the height, width, and text set.
        collectibles = Label(
            root,
            text=collectiblesList,
            justify=LEFT,
            anchor='n'
        )

        # Place the GUI element on the screen
        collectibles.place(relwidth=0.1, relheight=0.076, relx=0.1, rely=0.51)

        buttonWidth = 80

        posy_choices = [0.69, 0.76, 0.83, 0.90]

        # Initialize all GUI buttons with the height, width, text, and command method (what will result upon
        # clicking the button) set.
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

    # This grouping of GPIO statements act as the intial handler for all GPIO input connections. Once it detects a completed circuit
    # on the controller whichi is designated as GPIO.RISING, it will callback to one of the relay methods based on the specific GPIO connection
    # that it was detected from. In total the buttons are handled by GPIO pins 17, 22, 27, 24 and 16. Each method in the handler also has a bouncetime
    # which is similar to a timer interrupt, it gives the method the alloted amount of time to respond and if the handler does not get a response, it
    # will ignore the signal.

    GPIO.add_event_detect(17, GPIO.RISING, callback=relayToTkinterY, bouncetime=300) # Yellow Button
    GPIO.add_event_detect(22, GPIO.RISING, callback=relayToTkinterR, bouncetime=300) # Red Button
    GPIO.add_event_detect(27, GPIO.RISING, callback=relayToTkinterG, bouncetime=300) # Green Button
    GPIO.add_event_detect(24, GPIO.RISING, callback=relayToTkinterB, bouncetime=300) # Blue Button
    GPIO.add_event_detect(16, GPIO.RISING, callback=relayToTkinterS, bouncetime=300) # Small Button

    # 
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
