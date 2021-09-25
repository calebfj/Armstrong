class PlayerValues:
    # __hasDynamite = False

    def __init__(self):
        self.__hasDynamite = False
        self.__hasBandages = False
        self.__hasFood = False
        self.__health = 4

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

    def changeHealth(self, value):
        self.__health += value

    def getHealth(self):
        return self.__health

    def die(self):
        self.__health = 0

    def isDead(self):
        if self.__health == 0:
            return True




