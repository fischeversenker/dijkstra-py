#!/usr/bin/env python

import sys, copy

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

class Field:
  def __init__(self, x: int, y: int, value: str, distance: int, predecessor = None):
    self.value = value
    self.position = Position(x, y)
    self.distance = distance
    self.explored = False
    self.predecessor = predecessor

  def __str__(self):
    return f"Field: ({self.position.x}, {self.position.y}), {self.value}\texplored: {self.explored}\tdistance: {self.distance}"

class Map:
  def __init__(self, fields: [[Field]]):
    self.fields = fields

  def __str__(self):
    rows = ''
    for row in self.fields:
      for col in row:
        rows = rows + f" {col.value}"
      rows = rows + "\n"
    return rows

  def copy(self):
    return Map(copy.deepcopy(self.fields))

class Move:
  def __init__(self, current: Field, to: Field, cost: int):
    self.current = current
    self.to = to
    self.cost = cost

  def __str__(self):
    return f"Move:\n\tfrom: {self.current}\n\tto: {self.to}\n\tcost: {self.cost}"

  @staticmethod
  def make(start: Field, end: Field):
    return Move(start, end, Move.get_move_cost(start, end))

  @staticmethod
  def get_move_cost(start: Field, end: Field):
    if abs(start.position.x - end.position.x) > 0 and abs(start.position.y - end.position.y) > 0:
      return 10
    if abs(start.position.x - end.position.x) > 0:
      return 5
    if abs(start.position.y - end.position.y) > 0:
      return 6


class Pathfinder:
  def __init__(self, matrix):
    self.map_width = len(matrix[0])
    self.map_height = len(matrix)

    self.map: Map = self.transform_matrix(matrix)

    self.find_robot_and_goal()

  def transform_matrix(self, matrix):
    transformed_matrix = []
    last_field: Field = None
    for y in range(len(matrix)):
      transformed_matrix.append([])
      for x in range(len(matrix[0])):
        last_field = Field(x, y, matrix[y][x], float('inf'), last_field)
        transformed_matrix[y].append(last_field)
    return Map(transformed_matrix)

  def find_robot_and_goal(self):
    for y in range(self.map_height):
      for x in range(self.map_width):
        if self.map.fields[y][x].value == ROBOT:
          self.robot = self.map.fields[y][x]
          self.map.fields[y][x].distance = 0
        if self.map.fields[y][x].value == GOAL:
          self.goal = self.map.fields[y][x]

  def get_frontier(self, field: Field):
    if field == None:
      return []
    x = field.position.x
    y = field.position.y
      # all theoretically possible moves
    possible_moves = [(x-1, y), (x, y-1), (x-1, y-1), (x+1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
    # filter out the moves leading outside of the field and remove the moves leading to rocks and the already explored positions
    moves = []
    for (x, y) in possible_moves:
      if self.is_coord_free(x, y) and not field.explored:
        next_field = self.map.fields[y][x]
        move = Move.make(field, next_field)
        moves.append(move)
    sorted_moves = sorted(moves, key=lambda x: x.cost)

    return sorted_moves

  def is_coord_free(self, x, y):
    is_inside_matrix = x >= 0 and y >=0 and x < self.map_width and y < self.map_height
    if is_inside_matrix:
      field = self.map.fields[y][x]
      is_free = not field.value == OBSTACLE
      return is_free
    return False

  def get_next_unexplored_field(self):
    next = Field(-1, -1, OBSTACLE, float("inf"), None)
    for y in range(self.map_height):
      for x in range(self.map_width):
        field = self.map.fields[y][x]
        if self.is_coord_free(x, y) and not field.explored and field.distance <= next.distance:
          next = field
    if next.position.x < 0:
      return None
    return next

  def add_distances(self, move: Move):
    if move.current.distance + move.cost < move.to.distance:
      move.to.distance = move.current.distance + move.cost
      move.to.predecessor = move.current

  def get_optimal_path(self):
    pre = self.goal
    res = []
    if self.goal.distance == float("inf"):
      return res
    else:
      while pre != None:
        res.append(pre.position)
        if pre.distance == 0:
          pre = None
        else:
          pre = pre.predecessor
    return res[::-1]


  def print_optimal_path(self):
    optimal_path = self.get_optimal_path()
    if len(optimal_path) > 0:
      optimal_path_str = list(map(lambda pos: f"{pos}", optimal_path))
      print(f"optimal path has a distance of {self.goal.distance}")
    else:
      print('no path found')

  def print_map_with_optimal_path(self):
    enhanced_map = self.map.copy()
    optimal_path = self.get_optimal_path()
    if len(optimal_path) > 0:
      for pos in optimal_path[1:-1]:
        enhanced_map.fields[pos.y][pos.x].value = '$'
    print(enhanced_map)

  def start(self):
    print(self.map)

    frontier = self.get_frontier(self.get_next_unexplored_field())
    while len(frontier) > 0:
      move = frontier[0]
      move.current.explored = True

      for other_move in frontier:
        self.add_distances(other_move)

      frontier = self.get_frontier(self.get_next_unexplored_field())

    self.print_map_with_optimal_path()
    self.print_optimal_path()


def read_and_matrisize(file):
    contents = open(file).read()
    # split where there is a new line and remove the unneeded last new line
    return [line.split() for line in contents.split('\n')[:-1]][:-1]

pathfinder = Pathfinder(read_and_matrisize(sys.argv[1]))
pathfinder.start()
