from ortools.linear_solver import pywraplp

'''
Parameters:
  - n: αριθμός παραγγελιών
  - m: αριθμός διαθέσιμων φορτηγών
  - compatibility: λίστα από tuples (x,y) που υποδηλώνουν ότι
    το φορτηγό y μπορεί να παραδώσει την παραγγελία x.
    Θα ισχύει ότι 1 <= x <= n και 1 <= y <= m

Returns:
  - assignment: μια λίστα με tuples (x,y) τα οποία υποδηλώνουν ότι η παραγγελία
    x θα παραδοθεί από το φορτηγό y.

Sample input:
  n = 3
  m = 2
  compatibility = [(1,1), (2,1), (3,1), (2,2), (3,2)]

Sample output:

  [(1,1), (2,2)]

Σημείωση: υπάρχουν και άλλες λύσεις στις οποίες ταξινομούνται 2 παραγγελίες,
π.χ. [(2,1), (3,2)]. Μπορείτε να επιστρέψετε οποιαδήποτε από αυτές θέλετε.
'''
def assign(n, m, compatibility):
  solver = pywraplp.Solver.CreateSolver('SAT')
  w = {}
  for (i, j) in compatibility:
    w[(i,j)] = solver.IntVar(0, 1, f'w_{(i,j)}')

  for i in range(1, n + 1):
    solver.Add(solver.Sum(w[(i, j)] for (k, j) in w.keys() if k==i) <= 1)

  for j in range(1, m +1):
    solver.Add(solver.Sum(w[(i, j)] for (i, k) in w.keys() if k==j) <= 1)
  
  solver.Maximize(sum(w.values()))
  status = solver.Solve()

  result = []

  if status == pywraplp.Solver.OPTIMAL:
    result = [i for i in w if w[i].solution_value() > 0]
  return result