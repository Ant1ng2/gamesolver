from util import *
from Game import *
from TicTacToe.Tic import TicTacToe

class GameManager:

    def __init__(self, game, solver=None):
        self.game = game
        self.solver = solver
        if solver:
            self.solver.solveTraverse(self.game)

    # Starts the GameManager
    def play(self):
        while self.game.primitive() == Value.UNDECIDED:
            self.printInfo()
            self.printTurn()
        self.printInfo()
        print("Game Over")

    # Prints the game info
    def printInfo(self):
        if self.solver:
            print("Solver:", self.solver.solve(self.game))
        print("Primitive:", self.game.primitive())
        print(self.game.getTurn(), "'s turn")
        code = self.game.hash()
        print(self.game.hash())
        print(TicTacToe(code=code).toString())
        print(self.game.toString())
        print(self.game.turn)
        print("Possible Moves:", self.game.generateMoves())

    # Prompts for input and moves
    def printTurn(self):
        if self.game.getTurn() == self.game.getFirstPlayer() or not self.solver:
            move = self.game.moveFromInput("Enter Piece: ")
            if move not in self.game.generateMoves():
                print("Not a valid move, try again")
            else:
                self.game = self.game.doMove(move)
        else:
            self.game = self.game.doMove(self.solver.generateMove(self.game))
        print("----------------------------")
