from util import *
import csv
import math
import os
# This solver code is my own written creation (Anthony Ling). You can find the source code 
# at https://github.com/Ant1ng2/Gamesolver

# util module not included

class Solver():

    def __init__(self, name=None):
        self.memory = {}
        self.remoteness = {}
        path = os.path.join(os.getcwd() + r'/solved/', name)
        try:
            with open(path, 'r') as f:
                reader = csv.reader(f)
                self.memory = {rows[0]:rows[1] for rows in reader}
                del self.memory['key']
        except:
            print("Automatically solving manually as path not found: " + path)

    def resetMemory(self):
        self.memory.clear()

    def writeMemory(self, name=r'untitled.csv'):        
        path = os.path.join(os.getcwd() + r'/solved/', name)
        with open(path, 'w') as f:
            f.write("%s,%s\n"%("key", "value"))
            for key in self.memory.keys():
                f.write("%s,%s\n"%(key, self.memory[key]))

    def numValues(self, value):
        return len([i for i in self.memory.values() if i == value])

    def getRemoteness(self, game):
        serialized = game.serialize()
        if serialized in self.remoteness:
            return self.remoteness[serialized]

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
            newGame = game.doMove(move)
            if self.solve(newGame) == Value.LOSE:
                self.memory[serialized] = Value.WIN
                return Value.WIN # Not necessarily traverse all subtree
            if self.solve(newGame) == Value.TIE:
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
        # if len(self.memory) % 1000 == 0: print(len(self.memory))

        if serialized in self.memory:
            return self.memory[serialized]
        primitive = game.primitive()

        if primitive != Value.UNDECIDED:
            self.memory[serialized] = primitive
            self.remoteness[serialized] = 0
            return primitive

        min_remote = math.inf
        for move in game.generateMoves():
            newTicTacToe = game.doMove(move)
            value = self.solveTraverse(newTicTacToe)
            remote = self.remoteness[newTicTacToe.serialize()] + 1
            if value == Value.LOSE:
                if (tieFlag and not winFlag) or remote < min_remote: 
                    min_remote = remote
                winFlag = True
            if value == Value.TIE:
                if not winFlag: min_remote = remote
                tieFlag = True
            if value == Value.WIN and not winFlag or tieFlag: min_remote = min(min_remote, remote)
        if not winFlag: # There does not exist a losing child
            if tieFlag: # There exists a tie
                self.memory[serialized] = Value.TIE
            else: # There is no tie
                self.memory[serialized] = Value.LOSE
        else:
            self.memory[serialized] = Value.WIN
        self.remoteness[serialized] = min_remote
        return self.memory[serialized]

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
