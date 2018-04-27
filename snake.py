from enum import Enum
from random import randint
import threading
import time
import os
import math
import collections
import curses

class Queue:
        
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class Directions(Enum):
    N = [-1, 0]
    E = [0, 1]
    S = [1, 0]
    W = [0, -1]

class Position(object):
    
    def __init__(self, i, j, name):
        self.i = i
        self.j = j
        self.name = name
        self.neighbors = []

    def __repr__(self):
        return "[" + str(self.i) + ", " + str(self.j) + "]"

    def __str__(self):
        return self.name

class Snake(object):

    def __init__(self, i, j, direction):
        self.direction = direction
        self.setBody(i, j)

    def setBody(self, i, j):
        self.body = [[i, j + idx] for idx in range(0, 4)]

    def walk(self, boundI, boundJ):
        currPos = self.body[0]
        newI = currPos[0] + self.direction.value[0]
        newJ = currPos[1] + self.direction.value[1]
        if 0 <= newI < boundI and 0 <= newJ < boundJ and not [newI, newJ] in self.body:
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i] = self.body[i - 1]
            self.body[0] = [newI, newJ]
            return True
        return False

    def walkIndex(self, pos):
        currPos = self.body[0]
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1]
            self.body[0] = [pos.i, pos.j]

    def eat(self, lastPos):
        self.body.append(lastPos)

    def findFood(self, goal, board):
        frontier = Queue()
        frontier.put(goal)
        came_from = {}
        came_from[goal] = None
        while not frontier.empty():
            current = frontier.get()
            for next in current.neighbors:
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current
        head = self.body[0]
        return came_from[board[head[0]][head[1]]]


class Board(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.setBoard(width, height)

    def __str__(self):
        horizontal = "".join(["-"] * (len(self.board[0]) + 2))
        string = horizontal + "\n"
        string += "|" + '\n|'.join([''.join([str(j) for j in i]) + "|" for i in self.board])
        string += "\n" + horizontal
        return string

    def setBoard(self, width, height):
        self.board = [[Position(i, j, " ") for j in range(width)] for i in range(height)]

    def setSnake(self, snake):
        self.snake = snake
        self.updateSnake()
        self.generateFood()

    def updateSnake(self):
        for b in self.snake.body:
            self.board[b[0]][b[1]] = Position(b[0], b[1], "O")

    def moveSnake(self):
        lastPos = self.snake.body[-1]
        if self.snake.walk(len(self.board), len(self.board[0])):
            firstPos = self.snake.body[0]
            self.board[firstPos[0]][firstPos[1]] = Position(firstPos[0], firstPos[1], "O")
            if(firstPos == self.food):
                self.snake.eat(lastPos)
            else:
                self.board[lastPos[0]][lastPos[1]] = Position(lastPos[0], lastPos[1], " ")
            return True
        return False
    
    def moveSnakeIndex(self, pos):
        lastPos = self.snake.body[-1]
        self.snake.walkIndex(pos)
        firstPos = self.snake.body[0]
        self.board[firstPos[0]][firstPos[1]] = Position(firstPos[0], firstPos[1], "O")
        if(pos == self.food):
            self.snake.eat(lastPos)
            self.generateFood()
        else:
            self.board[lastPos[0]][lastPos[1]] = Position(lastPos[0], lastPos[1], " ")

    def generateFood(self):
        i = randint(0, len(self.board) - 1)
        j = randint(0, len(self.board[0]) - 1)
        while [i, j] in self.snake.body:
            i = randint(0, len(self.board) - 1)
            j = randint(0, len(self.board[0]) - 1) 
        self.board[i][j] = Position(i, j, "\x1b[0;31;41m \x1b[0m")
        self.food = self.board[i][j]
        
    def updateNeighbors(self):
        for i in self.board:
            for j in i:
                j.neighbors = []
                # if 0 <= j.i - 1 < len(self.board) and 0 <= j.j < len(self.board[0]):
                #     j.neighbors.append(self.board[j.i - 1][j.j])
                # if 0 <= j.i + 1 < len(self.board) and 0 <= j.j < len(self.board[0]):
                #     j.neighbors.append(self.board[j.i + 1][j.j])
                # if 0 <= j.i < len(self.board) and 0 <= j.j - 1 < len(self.board[0]):
                #     j.neighbors.append(self.board[j.i][j.j - 1])
                # if 0 <= j.i < len(self.board) and 0 <= j.j + 1 < len(self.board[0]):
                #     j.neighbors.append(self.board[j.i][j.j + 1])

                if 0 <= j.i - 1 < len(self.board) and 0 <= j.j < len(self.board[0]):
                    pos = self.board[j.i - 1][j.j]
                    if not [pos.i, pos.j] in self.snake.body:
                        j.neighbors.append(pos)
                if 0 <= j.i + 1 < len(self.board) and 0 <= j.j < len(self.board[0]):
                    pos = self.board[j.i + 1][j.j] 
                    if not [pos.i, pos.j] in self.snake.body:
                        j.neighbors.append(pos)
                if 0 <= j.i < len(self.board) and 0 <= j.j - 1 < len(self.board[0]):
                    pos = self.board[j.i][j.j - 1]
                    if not [pos.i, pos.j] in self.snake.body:
                        j.neighbors.append(pos)
                if 0 <= j.i < len(self.board) and 0 <= j.j + 1 < len(self.board[0]):
                    pos = self.board[j.i][j.j + 1]
                    if not [pos.i, pos.j] in self.snake.body:
                        j.neighbors.append(pos)


def newBoard(w, h):
    b = Board(w, h)
    Hpos = int(round(len(b.board))/2)
    Wpos = int(round(len(b.board[0])/2))
    Wpos += int(round(Wpos/2))
    s = Snake(Hpos, Wpos, Directions.W)
    b.setSnake(s)
    return b

def newGame():
    b = newBoard(30, 20)
    b.updateNeighbors()
    for i in b.board:
        for j in i:
            print(repr(j))
            print(j.neighbors)
    while True:
        nextPos = b.snake.findFood(b.food, b.board)
        currPos = b.snake.body[0]
        # if not b.moveSnake():
        #     print("Perdeu...")
        #     break
        # print(str(b.snake.findFood(b.food, b.board)))
        b.moveSnakeIndex(nextPos)
        b.updateNeighbors()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(b))
        time.sleep(0.05)
        
newGame()