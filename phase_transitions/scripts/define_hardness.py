import time
import math
from pysat.solvers import Glucose3
import random

# --- Helper Functions ---

def generate_random_3sat(n_vars, alpha):
    """Generates a random 3-CNF formula."""
    n_clauses = int(n_vars * alpha)
    formula = []
    variables = list(range(1, n_vars + 1))
    
    for _ in range(n_clauses):
        clause_vars = random.sample(variables, 3)
        clause = [v * random.choice([-1, 1]) for v in clause_vars]
        formula.append(clause)
    return formula

def solve_with_dpll(formula):
    """Runs PySAT (Glucose3) and returns time and conflict count."""
    with Glucose3(bootstrap_with=formula) as solver:
        start_time = time.perf_counter()
        is_sat = solver.solve()
        end_time = time.perf_counter()
        
        stats = solver.accum_stats()
        conflicts = stats.get('conflicts', 0)
        
        return (end_time - start_time), conflicts, is_sat

def format_clause_to_text(clause):
    """Converts [1, -2, 3] to (x1 ∨ ¬x2 ∨ x3)."""
    literals = []
    for lit in clause:
        var = f"x{abs(lit)}"
        if lit < 0:
            literals.append(f"¬{var}")
        else:
            literals.append(var)
    return f"({' ∨ '.join(literals)})"

def print_expression_preview(formula, name):
    """Prints the first few clauses of the formula."""
    print(f"\n🔹 {name} Expression Preview (First 3 clauses of {len(formula)}):")
    
    # Convert first 3 clauses to string
    preview_clauses = [format_clause_to_text(c) for c in formula[:3]]
    expression_str = " ∧ ".join(preview_clauses)
    
    print(f"   {expression_str} ∧ ...")

# --- The Experiment ---

big_n = 100
big_alpha = 2.0 
small_n = 75
small_alpha = 4.26

print("Generating instances...")

# 1. Generate Big/Easy
formula_big = generate_random_3sat(big_n, big_alpha)
time_big, conflicts_big, sat_big = solve_with_dpll(formula_big)

# 2. Generate Small/Hard (Search for a good one)
print("Searching for a hard 'Small' instance...")
best_small_conflicts = -1
formula_small = None
time_small = 0
sat_small = False

for i in range(20):
    temp_formula = generate_random_3sat(small_n, small_alpha)
    t, c, s = solve_with_dpll(temp_formula)
    
    if c > best_small_conflicts:
        best_small_conflicts = c
        formula_small = temp_formula
        time_small = t
        sat_small = s
    
    if c > 50: break

# --- PRINTING THE EXPRESSIONS ---
print_expression_preview(formula_big, "BIG (Easy)")
print_expression_preview(formula_small, "SMALL (Hard)")

# --- RESULTS ---
print("\n[RESULTS]")
print("-" * 60)
print(f"{'METRIC':<20} | {'BIG (N=100)':<15} | {'SMALL (N=75)':<15}")
print("-" * 60)
print(f"{'Solve Time':<20} | {time_big:.5f} s       | {time_small:.5f} s")
print(f"{'Conflicts':<20} | {conflicts_big:<15} | {best_small_conflicts:<15}")
print(f"{'Status':<20} | {'SAT' if sat_big else 'UNSAT':<15} | {'SAT' if sat_small else 'UNSAT':<15}")
print("-" * 60)