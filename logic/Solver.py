from util import *

class Solver():

    def __init__(self):
        self.memory = {}

    def resetMemory(self):
        self.memory.clear()

    def solveWeakWithoutMemory(self, game):
        primitive = game.primitive()
        if primitive != Value.UNDECIDED:
            return primitive
        for move in game.generateMoves():
            newTicTacToe = game.doMove(move)
            if self.solve(newTicTacToe) == Value.LOSE:
                return Value.WIN # Not necessarily traverse all subtree
        return Value.LOSE

    # this one will end when it finds the next instance as Win
    def solve(self, game):
        serialized = game.serialize()
        if serialized in self.memory:
            return self.memory[serialized]
        primitive = game.primitive()
        if primitive != Value.UNDECIDED:
            self.memory[serialized] = primitive
            return primitive
        tieFlag = False
        for move in game.generateMoves():
            newTicTacToe = game.doMove(move)
            if self.solve(newTicTacToe) == Value.LOSE:
                self.memory[serialized] = Value.WIN
                return Value.WIN # Not necessarily traverse all subtree
            if self.solve(newTicTacToe) == Value.TIE:
                tieFlag = True
        if tieFlag:
            self.memory[serialized] = Value.TIE
            return Value.TIE
        self.memory[serialized] = Value.LOSE
        return Value.LOSE

    # this one will traverse all subtree
    def solveTraverse(self, game):
        winFlag = False
        tieFlag = False
        serialized = game.serialize()

        if serialized in self.memory:
            return self.memory[serialized]
        primitive = game.primitive()

        if primitive != Value.UNDECIDED:
            self.memory[serialized] = primitive
            return primitive

        for move in game.generateMoves():
            newTicTacToe = game.doMove(move)
            if self.solve(newTicTacToe) == Value.LOSE:
                winFlag = True
            if self.solve(newTicTacToe) == Value.TIE:
                tieFlag = True

        if not winFlag: # There does not exist a losing child
            if tieFlag: # There exists a tie
                self.memory[serialized] = Value.TIE
                return Value.TIE
            else: # There is no tie
                self.memory[serialized] = Value.LOSE
                return Value.LOSE

        self.memory[serialized] = Value.WIN
        return Value.WIN

    def generateMove(self, game):
        if game.generateMoves():
            tieMove = game.generateMoves()[0]
            for move in game.generateMoves():
                newGame = game.doMove(move)
                # The AI could pick a winning position that doesn't directly end the game.
                # TODO: Pick a move to end the game
                if self.solve(newGame) == Value.LOSE:
                    return move
                if self.solve(newGame) == Value.TIE:
                    tieMove = move
            return tieMove
