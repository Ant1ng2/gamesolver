from copy import copy, deepcopy

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from Game import Game
import Solver
from GameManager import *
from util import Value

class TicTacToe(Game):

    def __init__(self, size=3, code=None, turn="X"):
        self.board = []
        self.count = 0
        if code:
            row = []
            for i in code[:-1]:
                if (i == '0'):
                    row.append(" ")
                if (i == '1'):
                    row.append("X")
                    self.count += 1
                if (i == '2'):
                    row.append("O")
                    self.count += 1
                if len(row) == size:
                    self.board.append(row)
                    row = []
            self.turn = code[-1]
        else:
            for i in range(size):
                self.board += [[" " for _ in range(size)]]
            self.turn = turn
            self.count = 0
        self.len = len(self.board)
    
    def addPiece(self, x, y):
        if self.getPiece(x, y) == " ":
            self.count += 1
            self.board[x][y] = self.turn
            if self.turn == "X":
                self.turn = "O"
            else:
                self.turn = "X"

    def getPiece(self, x, y):
        if x >= 0 and x < self.len and y >= 0 and y < self.len:
            return self.board[x][y]
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
            if self.getPiece(i % self.len, i // self.len) == " ":
                moves += [[i % self.len, i // self.len]]
        return moves

    def doMove(self, move):
        if self.count >= self.len * self.len:
            return self
        if move in self.generateMoves():
            game = TicTacToe(self.len, self.hash(), self.turn)
            game.addPiece(move[0], move[1])
        return game

    def primitive(self):
        for i in range(self.len * self.len):
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

        if self.count >= self.len * self.len:
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
        string = ""
        stringHashes = []
        cur_board = self.board
        for _ in range(2):
            for _ in range(4):            
                for row in cur_board:
                    for char in row:
                        if char == " ":
                            string += "0"            
                        if char == "X":
                            string += "1"
                        if char == "O":
                            string += "2"
                string += self.turn
                stringHashes += [string]
                cur_board = [row[0] for row in zip(cur_board[::-1])]
            cur_board = [row[::-1] for row in cur_board]
        return min(stringHashes)

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