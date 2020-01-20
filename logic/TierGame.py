from abc import ABC, abstractmethod
from Game import Game

class TierGame(Game):

    @abstractmethod
    def getNumTiers(self):
        pass
    
    @staticmethod
    @abstractmethod
    def generateTierBoards(game, tier=0):
        pass