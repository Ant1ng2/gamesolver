from copy import copy, deepcopy

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from Game import Game
import Solver
from GameManager import *
from util import Value
import math

class TicTacToe(Game):

    def __init__(self, length=3, code=None, turn="X"):
        if code:
            self.board = list(code[:-1])
            self.boardsize = len(self.board)
            self.len = length
            self.turn = code[-1]
            self.x = len([i for i in self.board if i == "X"])
            self.o = len([i for i in self.board if i == "O"])
        else:
            self.board = [" " for i in range(length * length)]
            self.boardsize = len(self.board)
            self.len = length
            self.turn = turn
            self.x = 0
            self.o = 0
    
    def addPiece(self, x, y):
        # Mutable function on board
        if self.getPiece(x, y) == " ":
            self.board[y * self.len + x] = self.turn
            if self.turn == "X":
                self.x += 1
                self.turn = "O"
            else:
                self.o += 1
                self.turn = "X"

    def getPiece(self, x, y):
        if x >= 0 and x < self.len and y >= 0 and y < self.len:
            return self.board[y * self.len + x]
        return " "

    def getTurn(self):
        return self.turn

    def getFirstPlayer(self):
        return "X"

    def getSecondPlayer(self):
        return "O"

    def generateMoves(self):
        moves = []

        for i in range(self.len * self.len):
            if self.getPiece(i // self.len, i % self.len) == " ":
                moves += [[i % self.len, i // self.len]]
        return moves

    def doMove(self, move):
        if self.x + self.o >= self.boardsize:
            return self
        if move in self.generateMoves():
            game = TicTacToe(self.len, self.hash(), self.turn)
            game.addPiece(move[0], move[1])
        return game

    def primitive(self):
        for i in range(self.boardsize):
            piece = self.getPiece(i % self.len, i // self.len)
            if piece != " ":
                for j in [(1, 0), (0, 1), (1, -1), (1, 1)]:
                    lineLen = 0
                    for k in range(-(self.len - 1), (self.len)):
                        if self.getPiece(i % self.len + k * j[0], i // self.len + k * j[1]) == piece:
                            lineLen += 1
                        else:
                            lineLen = 0
                        if lineLen >= self.len:
                            if piece != self.turn:
                                return Value.LOSE
                            if piece == self.turn:
                                return Value.WIN

        if self.x + self.o >= self.boardsize:
            return Value.TIE
        else:
            return Value.UNDECIDED

    def toString(self):
        string = ""

        for i in range(self.len * self.len):
            if i % self.len == 0:
                string += "\n"
            string += self.getPiece(i % self.len, i // self.len)
        return string

    def serialize(self):
        return self.hash()
        
    def hash(self):
        """def bias():
            boardsize = self.size * self.size
            return math.factorial(boardsize) /  math.factorial()
        """
        return str(self.board) + self.turn

    def moveFromInput(self, prompt):
        print(prompt)
        return [int(x.strip()) for x in input().split(',')]

    def solve(self):
        solver = Solver.Solver()
        return solver.solve(self)

    def generateBestMove(self):
        solver = Solver.Solver()
        return solver.generateMove(self)

if __name__ == '__main__':
    game = TicTacToe(3)
    solver = Solver.Solver()
    gameManager = GameManager(game, solver)
    gameManager.play()
