from ortools.linear_solver import pywraplp

def load1(order, truck):
  solver = pywraplp.Solver.CreateSolver('SAT')
  assignment = {}
  dep2fuel = {}

  for i in range(len(order)):
     dep2fuel[i] = {}

  for i, _ in enumerate(order):
    for j, c in enumerate(truck):
        dep2fuel[i][j] = solver.IntVar(0, 1, f'dep2fuel_{i}_{j}')


  for j in range(len(truck)):
     solver.Add(solver.Sum(dep2fuel[i][j] for i in range(len(order))) <= 1)
     
  for i in range(len(order)):
     assignment[i] = {}  

  for i, _ in enumerate(order):
    for j, c in enumerate(truck):
        assignment[i][j] = solver.NumVar(0, c , f'assignment_{i}_{j}')



  for i, x in enumerate(order):
    for j, c in enumerate(truck):
      solver.Add(assignment[i][j] <= c * dep2fuel[i][j])
      
  for i, x in enumerate(order):
      solver.Add(solver.Sum(assignment[i][j] for j in range(len(truck)))<= x)
  
  k = 0
  max_dep = truck[0]
  for i, c in enumerate(truck):
     if c > max_dep:
        max_dep = c
        k = i

  solver.Add(solver.Sum(assignment[i][k] for i in range(len(order))) >= 0.8 * truck[k])

  solver.Add(solver.Sum(assignment[i][0] for i in range(len(order))) >= 0.9 * truck[0])

  solver.Maximize(sum(sum(assign_i.values()) for assign_i in assignment.values()))
  status = solver.Solve()

  result = [[0.0 for _ in range(len(truck))] for _ in range(len(order))]

  if status == pywraplp.Solver.OPTIMAL:
      for i in range(len(order)):
        for j in range(len(truck)):
          result[i][j] = assignment[i][j].solution_value()
          
  val = sum(sum(result,[])) 
  return val, result


def load2(order, truck):
  solver = pywraplp.Solver.CreateSolver('SAT')
  assignment = {}
  dep2fuel = {}

  for i in range(len(order)):
     dep2fuel[i] = {}

  for i, _ in enumerate(order):
    for j, c in enumerate(truck):
        dep2fuel[i][j] = solver.IntVar(0, 1, f'dep2fuel_{i}_{j}')


  for j in range(len(truck)):
     solver.Add(solver.Sum(dep2fuel[i][j] for i in range(len(order))) <= 1)
     
  for i in range(len(order)):
     assignment[i] = {}  

  for i, _ in enumerate(order):
    for j, c in enumerate(truck):
        assignment[i][j] = solver.NumVar(0, c , f'assignment_{i}_{j}')



  for i, x in enumerate(order):
    for j, c in enumerate(truck):
      solver.Add(assignment[i][j] <= c * dep2fuel[i][j])
      
  for i, x in enumerate(order):
      solver.Add(solver.Sum(assignment[i][j] for j in range(len(truck)))<= x)
  
  k = 0
  max_dep = truck[0]
  for i, c in enumerate(truck):
     if c > max_dep:
        max_dep = c
        k = i

  solver.Add(solver.Sum(assignment[i][k] for i in range(len(order))) <= 0.2 * truck[k])

  solver.Add(solver.Sum(assignment[i][0] for i in range(len(order))) >= 0.9 * truck[0])

  solver.Maximize(sum(sum(assign_i.values()) for assign_i in assignment.values()))
  status = solver.Solve()

  result = [[0.0 for _ in range(len(truck))] for _ in range(len(order))]

  if status == pywraplp.Solver.OPTIMAL:
      for i in range(len(order)):
        for j in range(len(truck)):
          result[i][j] = assignment[i][j].solution_value()
          
  val = sum(sum(result,[])) 
  return val, result

def load(order, truck):
  total_load = sum(order)
  
  val1, res1 = load1(order, truck)
  if val1 == total_load:
    return res1  
    
  val2, res2 = load2(order, truck)
  if val2 == total_load:
    return res2  
  return []

def ex1_assign(n, m, compatibility):
  solver = pywraplp.Solver.CreateSolver('SAT')
  w = {}
  for (i, j) in compatibility:
    # Ορίζουμε μία τυχαία μεταβλητή, για κάθε επιτρεπτό συνδυασμό παραγγελίας - φορτηγού
    w[(i,j)] = solver.IntVar(0, 1, f'w_{(i,j)}')

  for i in range(1, n + 1):
    # Για κάθε παραγγελία, μπορεί να επιλεγεί το πολύ 1 φορτηγό
    solver.Add(solver.Sum(w[(i, j)] for (k, j) in w.keys() if k==i) <= 1)

  for j in range(1, m +1):
    # Κάθε φορτηγό, μπορεί να παραφώσει το πολύ μία παραγγελία
    solver.Add(solver.Sum(w[(i, j)] for (i, k) in w.keys() if k==j) <= 1)
  
  solver.Maximize(sum(w.values()))
  status = solver.Solve()

  result = []

  if status == pywraplp.Solver.OPTIMAL:
    result = [i for i in w if w[i].solution_value() > 0]

  return result

def assign(orders, trucks):
  compatibility = []
  result = {}
  for i in range(len(orders)):
    for j in range(len(trucks)):
      res = load(orders[i], trucks[j])
      if  res != []:
              compatibility.append((i, j))
              result[(i, j)] = res

  sol = ex1_assign(len(orders), len(trucks), compatibility)

  assignments = []
  for (x, y) in sol:
      assignments.append((x, y, result[(x, y)]))
  return assignments
