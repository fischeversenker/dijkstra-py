#!/usr/bin/env python

import sys

OBSTACLE = '*'
ROBOT = 'R'
GOAL = 'X'


class Position:
    def __init__(self, x: int, y: int):
      self.x = x
      self.y = y

    def __eq__(self, other):
      return self.x == other.x and self.y == other.y

    def __str__(self):
      return f"({self.x}, {self.y})"

class Move:
  def __init__(self, current: Position, to: Position, cost: int):
    self.current = current
    self.to = to
    self.cost = cost

  def __str__(self):
    return f"Move:\tfrom: {self.current}\tto: {self.to}\tcost: {self.cost}"

  @staticmethod
  def make(start, end):
    return Move(start, end, Move.get_move_cost(start, end))

  @staticmethod
  def get_move_cost(start: Position, end: Position):
    if abs(start.x - end.x) > 0 and abs(start.y - end.y) > 0:
      return 10
    if abs(start.x - end.x) > 0:
      return 5
    if abs(start.y - end.y) > 0:
      return 6

class Path:
  def __init(self, moves: [Move]):
    self.moves = moves

  def addMove(self, move: Move):
    self.moves.append(move)

  def getCosts(self):
    return sum(list(map(lambda move: move.cost, self.moves)))


class Pathfinder:
  def __init__(self, matrix):
    self.matrix = matrix
    self.matrix_width = len(matrix)
    self.matrix_height = len(matrix[0])

    self.explored: [Position] = []
    self.frontier: [Move] = []

    self.find_robot_and_goal()

  def find_robot_and_goal(self):
    for i in range(self.matrix_width):
      for j in range(self.matrix_height):
        if self.matrix[i][j] == ROBOT:
          self.robot = Position(i,j)
          self.explored.append(self.robot)
        if self.matrix[i][j] == GOAL:
          self.goal = Position(i,j)

  def get_frontier(self, currentPosition: Position):
    x = currentPosition.x
    y = currentPosition.y
      # all theoretically possible moves
    possible_moves = [(x-1, y), (x, y-1), (x-1, y-1), (x+1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
    # filter out the moves leading outside of the field and remove the moves leading to rocks and the already explored positions
    return [Position(x,y) for (x,y) in possible_moves if self.is_field_reachable(x, y)]

  def is_field_reachable(self, x, y):
    is_inside_matrix = x >= 0 and y >=0 and x < self.matrix_width and y < self.matrix_height
    is_free = self.matrix[x][y] != OBSTACLE
    is_unexplored = not self.is_explored(Position(x,y))
    return is_inside_matrix and is_free and is_unexplored

  def sort_frontier_and_add_cost(self, frontier: [Move]):
    moves = self.sort_costs(list(map(lambda move: Move.make(self.robot, move), frontier)))
    # for move in moves:
    #   print(move)
    return moves

  def is_explored(self, node: Position):
    for position in self.explored:
      if position == node:
        return True
    return False

  def sort_costs(self, frontier: [Move]):
    frontier.sort(key=lambda x: x.cost, reverse=True)
    return frontier

  def start(self):
    # algorithm: get possible moves, filter them, sort them, choose next
    length = 5
    i = 0
    while i < length:
      print(f"Robot is at {self.robot}")
      #if frontier.length == 0:
      #  return "No possible path!"
      # get possible moves (filtered) and sort them
      frontier = self.get_frontier(self.robot)
      #print(frontier)
      # sort moves
      frontier = self.sort_frontier_and_add_cost(frontier)
      newPosition = frontier.pop().to
      self.robot = Position(newPosition.x, newPosition.y)
      self.explored.append(self.robot)
      i = i + 1

  # print(get_frontier(self.robot))

  # x = get_move_costs(get_frontier(self.robot))
  # sort_frontier(x)





def read_and_matrisize(file):
    contents = open(file).read()
    # split where there is a new line and remove the unneeded last new line
    return [line.split() for line in contents.split('\n')[:-1]][:-1]

pathfinder = Pathfinder(read_and_matrisize(sys.argv[1]))
pathfinder.start()
