import pytest

from . TicTacToe.Tic import TicTacToe
from . Solver import Solver 
import util

def test_primitive():
    game = TicTacToe()
    solver = Solver()
    assert game.primitive() == util.Value.UNDECIDED
    assert solver.solve(game) == util.Value.TIE
