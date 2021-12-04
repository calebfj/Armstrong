# This class is simply a container for all of the GameState objects to store their preset information.
# This class only stores string text concerning a gamestate's 4 choices and main menu text message.
class GameState:
    def __init__(self, message, choice1, choice2, choice3, choiceDeath):
        self.__choiceDeath = choiceDeath
        self.__choice3 = choice3
        self.__choice2 = choice2
        self.__choice1 = choice1
        self.__message = message

    def getMessage(self):
        return self.__message

    def getChoice1(self):
        return self.__choice1

    def getChoice2(self):
        return self.__choice2

    def getChoice3(self):
        return self.__choice3

    def getChoiceDeath(self):
        return self.__choiceDeath
