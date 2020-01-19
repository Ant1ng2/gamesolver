import pytest

from Games.TTT import TTT
from Solver import Solver 
import util

def test_primitive():
    game = TTT()
    solver = Solver()
    assert game.primitive() == util.GameValue.UNDECIDED
    assert solver.solve(game) == util.GameValue.TIE
