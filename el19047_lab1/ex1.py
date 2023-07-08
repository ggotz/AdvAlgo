from ortools.linear_solver import pywraplp

'''
Parameters:
  - points: a list of 2-dimensional tuples (x,y)

Returns:
  - (a,b): a tuple with the line's coefficients
'''
def fit_line(points):
  solver = pywraplp.Solver.CreateSolver('GLOP')
  a = solver.NumVar(-solver.infinity(), solver.infinity(), 'a')
  b = solver.NumVar(-solver.infinity(), solver.infinity(), 'b')
  d = {}

  for i in range(len(points)):
    d[i] = solver.NumVar(0, solver.infinity(), f"d_{i}")

  for i, (x, y) in enumerate(points):
    solver.Add(a * x  + b - y <= d[i])
    solver.Add(- a * x  - b + y <= d[i]) 

  solver.Minimize(sum(d.values()))

  status = solver.Solve()
  if status == pywraplp.Solver.OPTIMAL:
    a_opt = a.solution_value()
    b_opt = b.solution_value()

  return a_opt, b_opt