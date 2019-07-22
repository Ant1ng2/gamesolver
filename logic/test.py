import pytest

from . TicTacToe.Tic import TicTacToe
import util

def test_primitive():
    game = TicTacToe()
    assert game.primitive() == util.Value.UNDECIDED
