from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import sys
sys.path.append('../')

from logic.Games import TTT
from logic.Solvers.Solver import Solver

import re

# Create your views here.

class Cache:
    def __init__(self, solver):
        self.solver = solver

    def solve(self, game):
        return self.solver.solve(game)

    def generateMove(self, game):
        return self.solver.generateMove(game)

cache = Cache(Solver(name=r'TTT4AndRemotenessOptimized.csv', read=True))

def index(request, turn, code):
    code = code.replace("_", TTT.NONE)
    reg = re.compile('^['+ TTT.FIRST + TTT.SECOND + TTT.NONE + ']{16}$')
    if not reg.match(code):
        return HttpResponse(status=404)

    game = TTT.TTT(code=code)
    context = {
        "prediction" : cache.solve(game),
        "turn" : game.getTurn(),
        "board" : game.toString(),
        "moves" : game.generateMoves(),
        "primitiveState" : game.primitiveState(), 
        "solution" : cache.generateMove(game)
    }
    return JsonResponse(context)
