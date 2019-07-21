from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from logic.TicTacToe import Tic
from logic.Solver import Solver

import re

# Create your views here.

class Cache:
    def __init__(self, solver):
        self.solver = solver

    def solve(self, game):
        return self.solver.solve(game)

    def generateMove(self, game):
        return self.solver.generateMove(game)

cache = Cache(Solver())

def index(request, turn, code):
    reg = re.compile('^[012]{9}$')
    if not reg.match(code):
        return HttpResponse(status=404)

    game = Tic.TicTacToe(code=code + turn)
    context = {
        "prediction" : cache.solve(game),
        "turn" : game.getTurn(),
        "board" : game.toString(),
        "moves" : game.generateMoves(),
        "solution" : cache.generateMove(game)
    }
    return JsonResponse(context)
