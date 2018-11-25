#!/usr/bin/env python

import sys
import json

OBSTACLE = '*'
ROBOT = 'R'
GOAL = 'X'


class Position:
    def __init__(self, x: int, y: int):
      self.x = x
      self.y = y

    def __eq__(self, other):
      return self.x == other.x and self.y == other.y

class Move:
  def __init__(self, current: Position, to: Position, cost: int):
    self.current = current
    self.to = to
    self.cost = cost

class Path:
  def __init(self, moves: [Move]):
    self.moves = moves

  def addMove(self, move: Move):
    self.moves.append(move)

  def getCosts(self):
    return sum(list(map(lambda move: move.cost, self.moves)))


def read_and_matrisize(file):
    contents = open(file).read()
    # split where there is a new line and remove the unneeded last new line
    return [line.split() for line in contents.split('\n')[:-1]][:-1]


field_matrix = read_and_matrisize(sys.argv[1])
robot = Position(0,0)
goal = Position(0,0)
explored = []

for i in range(len(field_matrix)):
    for j in range(len(field_matrix[0])):
      if field_matrix[i][j] == 'R':
          print("found goal")
          robot = Position(i,j)
      if field_matrix[i][j] == 'X':
            goal = Position(i,j)


def get_frontier(currentPosition: Position):
  x = currentPosition.x
  y = currentPosition.y
    # all theoretically possible moves
  possible_moves = [(x-1, y), (x, y-1), (x-1, y-1), (x+1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
  # filter out the moves leading outside of the field and remove the moves leading to rocks and the already explored positions
  possible_moves = [Position(x,y) for (x,y) in possible_moves if x >= 0 and y >=0 and field_matrix[x][y] != OBSTACLE and not is_explored(Position(x,y))]
  return possible_moves

def sort_frontier_and_add_cost(frontier):
  moves = sort_costs(list(map(lambda move: Move(robot, move, get_move_cost(robot, move)), frontier)))
  # for move in moves:
  #   print(move.current, move.to, move.cost)
  return moves

def is_explored(node: Position):
  for position in explored:
    if position == node:
      return True
  return False

def sort_costs(frontier):
  frontier.sort(key=lambda x: x.cost, reverse=True)
  return frontier

def get_move_cost(start: Position, end: Position):
  if abs(start.x - end.x) > 0 and abs(start.y - end.y) > 0:
    return 10
  if abs(start.x - end.x) > 0:
    return 5
  if abs(start.y - end.y) > 0:
    return 6


frontier = [robot]

# algorithm: get possible moves, filter them, sort them, choose next
length = 5
i = 0
while i < length:
  print("loop started")
  #if frontier.length == 0:
  #  return "No possible path!"
  # get possible moves (filtered) and sort them
  frontier = get_frontier(robot)
  #print(frontier)
  # sort moves
  frontier = sort_frontier_and_add_cost(frontier)
  newPosition = frontier.pop().to
  robot = Position(newPosition.x, newPosition.y)
  explored.append(robot)
  print(robot.x, robot.y)
  i = i + 1


# print(robot, goal)
# print(get_frontier(robot))

# x = get_move_costs(get_frontier(robot))
# sort_frontier(x)
