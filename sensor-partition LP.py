import xlrd
from math import sqrt
from ortools.linear_solver import pywraplp


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __repr__(self):
    try:
      return f'T{self.index}'
    except:
      return f'Point({round(self.x, 2)},{round(self.y, 2)})'

  def distance(self, other):
    return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

  def midpoint(self, other):
    return Point(self.x/2 + other.x/2, self.y/2 + other.y/2)


def left_intersect(p1, p2, r):
  c = sqrt(r**2 / p1.distance(p2)**2 - 1/4)
  X = p1.x/2 + p2.x/2 + c*p1.y - c*p2.y
  Y = p1.y/2 + p2.y/2 - c*p1.x + c*p2.x
  return Point(X, Y)

def right_intersect(p1, p2, r):
  c = sqrt(r**2 / p1.distance(p2)**2 - 1/4)
  X = p1.x/2 + p2.x/2 - c*p1.y + c*p2.y
  Y = p1.y/2 + p2.y/2 + c*p1.x - c*p2.x
  return Point(X, Y)

def sorted_counterclockwise(set_points, p):
  Above, Below = [], []
  for p1 in set_points:
    if p1.y < p.y:
      Below.append(p1)
    else:
      Above.append(p1)
  Below.sort(key=lambda p1: (p1.x-p.x) / p.distance(p1))
  Above.sort(key=lambda p1: (p.x-p1.x) / p.distance(p1))
  return Below + Above

def clear_subset(list_s):
  i = 0
  while(i < len(list_s)):
    j = i + 1
    old = list_s[i]
    while(j < len(list_s)):
      cur = list_s[j]
      if old.issubset(cur):
        old = list_s[i] = cur
        list_s.pop(j)
      elif cur.issubset(old):
        list_s.pop(j)
      else:
        j += 1
    i += 1

def create_data_model(binary_matrix):
  data = {}
  data['constraint_coeffs'] = binary_matrix
  data['num_vars'] = len(data['constraint_coeffs'][0])
  data['num_constraints'] = len(data['constraint_coeffs'])
  return data

def main():
  wb = xlrd.open_workbook("D:/testCLique2/test 31 30.xlsx")
  sheet0 = wb.sheet_by_index(0)
  #sheet1 = wb.sheet_by_index(1)
  uncovered = []
  for i in range(1, sheet0.nrows):
    T = Point(sheet0.cell_value(i, 1), sheet0.cell_value(i, 2))
    uncovered.append(T)
    T.index = i - 1
  r = 30#sheet1.cell_value(1, 4)
  chosen_regions = []
  optm_regions = []
  targets = set(uncovered)

  for T in targets:
    left_ints, right_ints, neighbors, anchor_points = [], [], [], []
    neighbors = [T1 for T1 in uncovered if 0 < T1.distance(T) <= 2*r]
    if len(neighbors) == 0:
      chosen_regions.append({T})
      uncovered.remove(T)
      continue
    left_ints = [left_intersect(T, T1, r) for T1 in uncovered
                 if 0 < T1.distance(T) <= 2*r]
    right_ints = [right_intersect(T, T1, r) for T1 in uncovered
                  if 0 < T1.distance(T) <= 2*r]
    tot_ints = right_ints + left_ints
    tot_ints = sorted_counterclockwise(tot_ints, T)
    first = tot_ints[0]
    last = tot_ints[len(tot_ints)-1]
    if last in right_ints and first in left_ints:
      anchor_points.append(first.midpoint(last))

    for i in range(len(tot_ints)-1):
      curr = tot_ints[i]
      next_ = tot_ints[i+1]
      if curr in right_ints and next_ in left_ints:
        anchor_points.append(curr.midpoint(next_))
        
    for p in anchor_points:
      R = {T}
      R.update([T2 for T2 in neighbors if p.distance(T2) <= r])
      optm_regions.append(R)
  clear_subset(optm_regions)
  
  while(True):
    new_covered = set()
    new_regions = []
    for T in uncovered:
      count = 0
      for R in optm_regions:
        if T in R:
          count += 1
          if count > 1: break
          R1 = R
      if count == 1:
        if R1 not in new_regions:
          new_regions.append(R1)
    if new_regions == []: break
    new_covered.update(*new_regions)
    optm_regions = [R.difference(new_covered) for R in optm_regions]
    clear_subset(optm_regions)
    uncovered = [T for T in uncovered if T not in new_covered]
    chosen_regions += new_regions

  while(len(uncovered) > 0):
    division = [optm_regions[0]]
    div_covered = set()
    new_covered = optm_regions[0]
    optm_regions.pop(0)
    while(len(new_covered) > 0):
      new_regions = []
      div_covered.update(new_covered)
      for T in new_covered:
        for R in optm_regions:
          if T in R and R not in division:
            division.append(R)
            new_regions.append(R)
      optm_regions = [R for R in optm_regions if R not in new_regions]
      in_new_regions = set()
      in_new_regions.update(*new_regions)
      new_covered = in_new_regions.difference(new_covered)
      div_covered.update(new_covered)
    uncovered = [T for T in uncovered if T not in div_covered]

    binary_matrix = []
    for T in div_covered:
      binary_list = []
      for R in division:
        if T in R:
          binary_list.append(1)
        else:
          binary_list.append(0)
      binary_matrix.append(binary_list)
  
    data = create_data_model(binary_matrix)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()
    x = {}
    for j in range(data['num_vars']):
      x[j] = solver.IntVar(0, 1, f'x[{j}]')
    for i in range(data['num_constraints']):
      constraint = solver.RowConstraint(1, infinity, '')
      for j in range(data['num_vars']):
        constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
    objective = solver.Objective()
    for j in range(data['num_vars']):
      objective.SetCoefficient(x[j], 1)
    objective.SetMinimization()
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
      chosen_regions += [division[j] for j in range(data['num_vars'])
                         if x[j].solution_value() == 1]
    else:
      print('The problem does not have an optimal solution.')
  
  print('Chosen regions:')
  for R in chosen_regions:
    print(*R)
  print()
  print('Total:', len(chosen_regions))

  covered = set()
  for set_ in chosen_regions:
    covered.update(set_)
  print('All covered?', targets == covered)
if __name__ == '__main__':
  main()