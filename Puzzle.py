import random
from copy import deepcopy, copy
from enum import Enum
import math


class Puzzle:

    puzzles_width = 3
    goal = []
    board = []

    def __init__(self, n):
        self.puzzles_width = int(math.log(n, 2))
        self.setGoal()
        self.setBoard(self.goal)

    # board setter
    def setBoard(self, board):
        self.board = board
    
    def isGoal(self):
        return self.board == self.goal

    def getState(self):
        return self.board

    # setting the problem goal 
    def setGoal(self):
        self.goal = []
        value = 1
        for i in range(self.puzzles_width):
            temp = []
            for j in range(self.puzzles_width):
                if(value == math.pow(self.puzzles_width, 2)):
                    value = 0
                temp.append(value)
                value += 1
            self.goal.append(temp)  

    # getting the best successor for a given problem
    def getSuccessors(self):
        successors = []
        for direction in Directions:
            successor = self.move(direction)
            if len(successor.board) > 0:
                successorH = successor.heuristic()
                successors.append((successor, successorH, [direction.name]))
        return sorted(successors, key = lambda x: x[1])

    def move(self, direction):
        x, y = self.getIndex(self.board, 0)
        next = Puzzle(int(math.pow(2, self.puzzles_width)))
        next.setBoard(deepcopy(self.board))
        blockDirections = self.getBlockDirections((x, y))

        # checking the what directions are blocked
        if direction in blockDirections:
            next.setBoard([])
            return next

        # calculate next position after doing directions
        x2, y2 = self.getTargetState((x, y), direction)

        # swap
        target = next.board[x2][y2]
        next.board[x2][y2] = 0
        next.board[x][y] = target

        return next

    # calculating block directions of a given state
    def getBlockDirections(self, state):
        x, y = state
        blockDirections = []
        if x == 0:
            blockDirections.append(Directions.up)
        elif x == self.puzzles_width - 1:
            blockDirections.append(Directions.down)
        if y == 0:
            blockDirections.append(Directions.left)
        elif y == self.puzzles_width - 1:
            blockDirections.append(Directions.right)

        return blockDirections

    # calculate target state after a given state move towards a given direction
    def getTargetState(self, state, direction):
        x, y = state
        if(direction == Directions.up):
            x2, y2 = x - 1, y
        elif(direction == Directions.down):
            x2, y2 = x + 1, y
        elif(direction == Directions.left):
            x2, y2 = x, y - 1
        elif(direction == Directions.right):
            x2, y2 = x, y + 1
        
        return (x2, y2)

    # find a value's position in board
    def getIndex(self, board,value):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if board[i][j] == value:
                    return (i, j)
    
    # manhatan heuristic: dx + dy
    def heuristic(self):
        h = 0
        for k in range(1, int(math.pow(self.puzzles_width, 2))):
            x1, y1 = self.getIndex(self.board, k)
            x2, y2 = self.getIndex(self.goal, k)
            h += math.fabs(x2 - x1) + math.fabs(y2 - y1)
        return h

    # changes the problems board to a random solvable board
    def generateRandomBoard(self, hardrate):
        problem = self
        problem.board = self.goal
        directionsList = []
        for d in Directions:
            directionsList.append(d)
        
        for i in range(hardrate):
            r = random.randrange(0, 4)
            temp = problem.move(directionsList[r])
            while len(temp.board) == 0:
                r = random.randrange(0, 4)
                temp = problem.move(directionsList[r])
            problem = temp
        self.setBoard(problem.board)

        
class Directions(Enum):
    up = 1,
    down = 2,
    left = 3,
    right = 4
