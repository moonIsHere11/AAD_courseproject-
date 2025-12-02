import random
import matplotlib.pyplot as plt
from pysat.solvers import Glucose3
import numpy as np
import pandas as pd

def generate_random_3sat(n_vars, n_clauses):
    variables = list(range(1, n_vars + 1))
    formula = []
    for _ in range(n_clauses):
        clause_vars = random.sample(variables, 3)
        clause = [v * random.choice([-1, 1]) for v in clause_vars]
        formula.append(clause)
    return formula

def measure_conflicts(n_vars, alpha):
    m = int(n_vars * alpha)
    formula = generate_random_3sat(n_vars, m)
    
    with Glucose3(bootstrap_with=formula) as solver:
        solver.solve()
        # The stats are tracked automatically, we just need to fetch them
        return solver.accum_stats().get('conflicts', 0)

# --- CONFIGURATION ---
N = 75
SAMPLES = 100 # Samples per point
# Scan closely around the transition
alphas = np.arange(3.0, 5.5, 0.1) 

results = []

print(f"Running Volatility Scan (N={N})...")

for alpha in alphas:
    conflicts_list = []
    for i in range(SAMPLES):
        conflicts_list.append(measure_conflicts(N, alpha))
    
    # Calculate Percentiles
    p50 = np.percentile(conflicts_list, 50) # Median
    p90 = np.percentile(conflicts_list, 90) # Hard
    p99 = np.percentile(conflicts_list, 99) # Nightmare
    
    results.append({
        'alpha': alpha,
        'p50': p50,
        'p90': p90,
        'p99': p99
    })
    print(f"  alpha={alpha:.1f} | Median={int(p50)} | 99th={int(p99)}")

df = pd.DataFrame(results)

# --- PLOTTING ---
plt.figure(figsize=(12, 7))

# Plot the lines
plt.plot(df['alpha'], df['p99'], 'r--', linewidth=2, label='99th Percentile')
plt.plot(df['alpha'], df['p90'], 'orange', linewidth=2, label='90th Percentile')
plt.plot(df['alpha'], df['p50'], 'b-', linewidth=2, label='Median')

# Fill the gap to visualize "Volatility"
plt.fill_between(df['alpha'], df['p50'], df['p99'], color='red', alpha=0.1, label='Zone of Volatility')

plt.axvline(x=4.26, color='k', linestyle=':', alpha=0.5, label='Critical Point')

plt.title(f'The Volatility Explosion: Percentiles of Hardness (N={N})', fontsize=16)
plt.xlabel('Clause-to-Variable Ratio', fontsize=12)
plt.ylabel('Conflicts (Deadends)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

# Save
plt.savefig('volatility_explosion.png')
print("Plot saved as 'volatility_explosion.png'")
plt.show()