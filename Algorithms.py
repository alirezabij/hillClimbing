from Puzzle import Puzzle
from Queen import Queen
import random
import math
from pprint import pprint
import time
import sys

def hillClimbing(problem, hardrate):
    cost = 0
    optimalCost = None

    problem.generateRandomBoard(hardrate)
    initialH = problem.heuristic()
    current = (problem, initialH, [])
    
    while(True):
        successors = current[0].getSuccessors()
        successor = successors[0]
        if successor[1] >= current[1]:
            answer = current
            break
        current = (successor[0], successor[1], current[2] + successor[2])

    
    accuracy = 1 - float(answer[1]) / float(initialH) if initialH and answer[1] else 1
    isGoal = answer[0].isGoal()
    cost = len(answer[2])
    if isGoal: optimalCost = cost 

    answer = answer + (isGoal, accuracy, problem, cost, optimalCost)
    return answer

def simulatedAnnealing(problem, hardrate):
    cost = 0
    optimalCost = None

    calls = 0
    maxCalls = 100
    temperature = 10
    coolingRate = .3
    problem.generateRandomBoard(hardrate)
    initialH = problem.heuristic()
    current = (problem, initialH, [])
    answer = None

    while(calls < maxCalls):
        answer = current
        if(current[0].isGoal()):
            break

        successors = current[0].getSuccessors()
        successor = successors[random.randrange(len(successors))]

        if(random.uniform(0, 1) < probability(successor[1], current[1], temperature)):
            current = (successor[0], successor[1], current[2] + successor[2])

        temperature = temperature - temperature * coolingRate
        calls += 1

    accuracy = 1 - float(answer[1]) / float(initialH) if initialH and answer[1] else 1
    isGoal = answer[0].isGoal()
    cost = len(answer[2])
    if isGoal: optimalCost = cost 

    answer = answer + (isGoal, accuracy, problem, cost, optimalCost)
    return answer

def probability(e1, e2, t):
    de = e2 - e1
    return 1 if de > 0 else math.exp(de / t)

def solve(testNum, problem, algorithm, trace):
    trueSum = 0
    overallAccuracy = 0
    overallCost = 0
    hardrate = 20
    for i in range (testNum):
        if algorithm == 'hillClimbing':
            answer = hillClimbing(problem, hardrate)
        elif algorithm == 'simulatedAnnealing':
            answer = simulatedAnnealing(problem, hardrate)
        else:
            return
        solution, h, path, isGoal, accuracy, initialState, cost, optimalCost = answer
        if(isGoal):
            trueSum += 1
        overallAccuracy += accuracy
        overallCost += cost
        if(trace):
            print("------------------------------------------------")
            print("problem, h: \t\t" + str((initialState.getState(), initialState.heuristic())))
            print("solution, h: \t\t" + str((solution.getState(), solution.heuristic())))
            print("path: \t\t\t" + str(path))
            print("win: \t\t\t" + str(isGoal))
            print("cost: \t\t\t" + str(cost))
            print("optimal cost: \t\t" + str(optimalCost))
            print("accuracy: \t\t" + str('%.2f' % accuracy))

    print("------------------------------------------------")
    print "algorithm: \t\t" + str(algorithm)
    print "problem: \t\t" + str(problem.__class__.__name__)
    print 'overall win: \t\t' + str(int(float(trueSum) / float(testNum) * 100)) + "%"
    print 'overall accuracy: \t' + str(int(float(overallAccuracy) / float(testNum) * 100)) + "%"
    print 'overall cost: \t\t' + str((float(overallCost) / float(testNum)))
    print("------------------------------------------------")

solve(12, Puzzle(64), "hillClimbing", "")
solve(12, Puzzle(64), "simulatedAnnealing", "")
solve(12, Queen(8), "hillClimbing", "")
solve(12, Queen(8), "simulatedAnnealing", "")
