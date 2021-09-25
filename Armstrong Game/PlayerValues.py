class PlayerValues:
    # __hasDynamite = False

    def __init__(self):
        self.__hasDynamite = False
        self.__hasBandages = False
        self.__hasFood = False
        self.__hasNormalMap = False
        self.__hasEscapeMap = False
        self.__hasDisguises = False
        self.__hasKey = False
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

    def changeHealth(self, value):
        self.__health += value

    def getHealth(self):
        return self.__health

    def die(self):
        self.__health = 0

    def isDead(self):
        if self.__health == 0:
            return True



