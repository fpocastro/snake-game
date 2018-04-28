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

class Snake(object):

    def __init__(self, i, j, length):
        self.length = length
        self.head = [i, j]
        self.body = []
        self.setBody(i, j + 1)

    def setBody(self, startI, startJ):
        self.body = [[startI, startJ + idx] for idx in range(0, self.length - 1)]

    def move(self, food, board):
        pos = self.getMovement(food, board)
        if pos == []:
            # TODO Think about best random movement
            neighbors = self.getNeighbors(self.head, board)
            pos = neighbors[randint(0, len(neighbors) - 1)]
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1]
        self.body[0] = self.head
        self.head = pos
    
    def eat(self, lastPos):
        self.body.append(lastPos)

    def getMovement(self, goal, board):
        frontier = Queue()
        frontier.put(goal)
        came_from = {}
        came_from[str(goal)] = None
        while not frontier.empty():
            current = frontier.get()
            neighbors = self.getNeighbors(current, board)
            for next in neighbors:
                if str(next) not in came_from:
                    frontier.put(next)
                    came_from[str(next)] = current
        try:
            movement = came_from[str(self.head)]
        except:
            movement = []
        return movement

    def getNeighbors(self, pos, board):
        neighbors = []
        i = pos[0]
        j = pos[1]
        if 0 <= i - 1 < len(board) and 0 <= j < len(board[0]) and board[i - 1][j] != 2:
            neighbors.append([i - 1, j])
        if 0 <= i + 1 < len(board) and 0 <= j < len(board[0]) and board[i + 1][j] != 2:
            neighbors.append([i + 1, j])
        if 0 <= i < len(board) and 0 <= j - 1 < len(board[0]) and board[i][j - 1] != 2:
            neighbors.append([i, j - 1])
        if 0 <= i < len(board) and 0 <= j + 1 < len(board[0]) and board[i][j + 1] != 2:
            neighbors.append([i, j + 1])
        return neighbors

class Board(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.setBoard(width, height)
        self.points = 0

    def __str__(self):
        horizontal = "".join(["\x1b[0;34;44m \x1b[0m"] * (len(self.board[0]) + 2))
        string = horizontal + "\n"
        string += "\x1b[0;34;44m \x1b[0m" + '\n\x1b[0;34;44m \x1b[0m'.join([''.join([self.getPositionRepr(j) for j in i]) + "\x1b[0;34;44m \x1b[0m" for i in self.board])
        string += "\n" + horizontal
        string += "\nPoints: " + str(self.points)
        return string

    def getPositionRepr(self, pos):
        return ["\x1b[0;30;40m \x1b[0m", "\x1b[0;37;42m \x1b[0m", "\x1b[0;37;47m \x1b[0m", "\x1b[0;31;41m \x1b[0m"][pos]
    
    def setBoard(self, width, height):
        self.board = [[0 for j in range(width)] for i in range(height)]

    def setSnake(self, snake):
        self.snake = snake
        self.updateSnake()

    def moveSnake(self):
        tail = self.snake.body[-1]
        self.snake.move(self.food, self.board)
        if(self.snake.head == self.food):
            self.points += 1
            self.snake.eat(tail)
            self.generateFood()
        else:
            self.board[tail[0]][tail[1]] = 0
    
    def updateSnake(self):
        head = self.snake.head
        self.board[head[0]][head[1]] = 1
        for b in self.snake.body:
            self.board[b[0]][b[1]] = 2

    def generateFood(self):
        i = randint(0, len(self.board) - 1)
        j = randint(0, len(self.board[0]) - 1)
        while [i, j] in self.snake.body or [i, j] == self.snake.head:
            i = randint(0, len(self.board) - 1)
            j = randint(0, len(self.board[0]) - 1) 
        self.board[i][j] = 3
        self.food = [i, j]

snakeStartLength = 4
b = Board(30, 20)
Hpos = int(round(len(b.board))/2)
Wpos = int(round(len(b.board[0]) - snakeStartLength - 4))
s = Snake(Hpos, Wpos, snakeStartLength)
b.setSnake(s)
b.generateFood()

# Game finishes on exception.

while True:
    oldPos = b.snake.head
    b.moveSnake()
    b.updateSnake()
    os.system("clear")
    print(b)
    time.sleep(0.02)

# # Used to run various games one after another to test snake efficiency.
# points = []
# while True:
#     snakeStartLength = 4
#     b = Board(30, 20)
#     Hpos = int(round(len(b.board))/2)
#     Wpos = int(round(len(b.board[0]) - snakeStartLength - 4))
#     s = Snake(Hpos, Wpos, snakeStartLength)
#     b.setSnake(s)
#     b.generateFood()
#     while True:
#         try:
#             oldPos = b.snake.head
#             b.moveSnake()
#             b.updateSnake()
#         except:
#             points.append(b.points)
#             break
#     os.system("clear")
#     print(str(points))