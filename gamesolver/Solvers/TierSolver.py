from gamesolver.Solvers.Solver import Solver 
from gamesolver.util import *

class TierSolver(Solver):

    def __init__(self, *args, **kwargs):
        super(TierSolver, self).__init__(*args, **kwargs)
        self.solve = self.solveTier
        self.tier = None

    def solveTier(self, game):
        serial = game.serialize()
        if serial in self.memory: return self.memory[serial]
        if not self.tier: self.generateTierBoards(game.getBase())
        for i in range(game.getNumTiers(), -1, -1):
            for board in self.tiers[game.getCurTier()].values():
                if board.primitive() != GameValue.UNDECIDED: 
                    self.memory[board.serialize()] = board.primitive()
                    self.remoteness[board.serialize()] = 0
                else:
                    self.solveTraverse(board)
        return self.memory[serial]

    def generateTierBoards(self, game):
        self.tiers = { i:{} for i in range(game.getNumTiers()) }
        def helper(game):
            serialized = game.serialize()
            if serialized not in self.tiers[game.getCurTier()]:
                self.tiers[game.getCurTier()][serialized] = game
                for move in game.generateMoves():
                    helper(game.doMove(move))
        helper(game)