import time

# This class is utilized to store all information concerning a player's progress and stats within the game.
# Similar to the gamestate class, this class is primarily for information storage concerning player data,
# however it is also utilized to manipulate player data based on what occurs within the game. This is done to
# create an easier method of managing player data across resets and new games with possible data conflicting.
# Or overcomplicated code stuck in the middle of ScreenTemp.py clustering the readability of the file.
class PlayerValues:
    # Once a playerValues object has been initialized it will set the player to default values which
    # include full health, no collectibles, no end time recorded and a new start time value.
    def __init__(self):
        self.__hasDynamite = False
        self.__hasBandages = False
        self.__hasFood = False
        self.__hasNormalMap = False
        self.__hasEscapeMap = False
        self.__hasDisguises = False
        self.__hasKey = False
        self.__health = "♥♥♥♥"
        self.__healthValue = 4
        self.__endTime = 0
        self.__startTime = time.time()

    # The reset method allows players to utilize the same values object for storing their data
    # by resetting the same value object when the player either dies or restarts the game after
    # escaping to the player's default vales.
    def reset(self):
        self.__hasDynamite = False
        self.__hasBandages = False
        self.__hasFood = False
        self.__hasNormalMap = False
        self.__hasEscapeMap = False
        self.__hasDisguises = False
        self.__hasKey = False
        self.__health = "♥♥♥♥"
        self.__healthValue = 4
        self.__endTime = 0
        self.__startTime = time.time()

    # Every method, excluding the last 3, below is simply setter methods for each collectible within the game.
    # If a player finds an item, the collectible's value is set to true and vice versa when the player does
    # not have an item. This allows easy management over collectibles management within the game.
    def hasDynamite(self):
        return self.__hasDynamite

    def unlockDynamite(self):
        self.__hasDynamite = True

    def hasBandages(self):
        return self.__hasBandages

    def unlockBandages(self):
        self.__hasBandages = True

    def hasFood(self):
        return self.__hasFood

    def unlockFood(self):
        self.__hasFood = True

    def hasNormalMap(self):
        return self.__hasNormalMap

    def unlockNormalMap(self):
        self.__hasNormalMap = True

    def hasEscapeMap(self):
        return self.__hasEscapeMap

    def unlockEscapeMap(self):
        self.__hasEscapeMap = True

    def hasDisguises(self):
        return self.__hasDisguises

    def unlockDisguises(self):
        self.__hasDisguises = True

    def hasKey(self):
        return self.__hasKey

    def unlockKey(self):
        self.__hasKey = True

    def getEndTime(self):
        return self.__endTime

    def setEndTime(self, float):
        self.__endTime = float - self.__startTime

    def getStartTime(self):
        return self.__startTime

    def getHealth(self):
        return self.__health

    # The change health method takes in one value parameter which simply adds health to the player's
    # total health value variable, the method then updates the string variable within the GUI to reflect this
    # by showing the hearts for each whole number of health the player has.
    def changeHealth(self, value):
        self.__healthValue += value
        if value < 0:
            self.__health = self.__health[:len(self.__health) + value]
        else:
            self.__health += "♥"

    # The die method simply sets the player's health to 0 and sets their bar to show 0 hearts. This method is
    # utilized when the player selects a death ending.
    def die(self):
        self.__healthValue = 0
        self.__health = ""

    # This method checks if the player has 0 health, if so then the player is noted as dead and the appropriate
    # values are then set within the ScreenTemp class to the GUI and to the PlayerValues object.
    def isDead(self):
        if self.__healthValue == 0:
            return True
