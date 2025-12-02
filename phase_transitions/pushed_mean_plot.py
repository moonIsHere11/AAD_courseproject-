import random
import matplotlib.pyplot as plt
from pysat.solvers import Glucose3
import numpy as np

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
        stats = solver.accum_stats()
        return stats.get('conflicts', 0)

# --- CONFIGURATION ---
N = 75
ALPHA = 3.8
TRIALS = 1000 # High sample size for a smooth histogram

print(f"Running Distribution Analysis: N={N}, Alpha={ALPHA}, Trials={TRIALS}...")

conflicts_data = []
for i in range(TRIALS):
    c = measure_conflicts(N, ALPHA)
    conflicts_data.append(c)
    if (i+1) % 50 == 0:
        print(f"  Completed {i+1}/{TRIALS}...", end='\r')

# --- PLOTTING ---
plt.figure(figsize=(10, 6))

# Histogram with log scale on y-axis to show the tail
counts, bins, patches = plt.hist(conflicts_data, bins=50, color='purple', edgecolor='black', alpha=0.7, log=True)

# Add Mean and Median lines
mean_val = np.mean(conflicts_data)
median_val = np.median(conflicts_data)

plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean ({int(mean_val)})')
plt.axvline(median_val, color='yellow', linestyle='dashed', linewidth=2, label=f'Median ({int(median_val)})')

plt.title(f'Evidence of Computational Chaos: Distribution of Hardness (N={N})', fontsize=14)
plt.xlabel('Computational Cost (Conflicts)', fontsize=12)
plt.ylabel('Frequency (Log Scale)', fontsize=12)
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.3)

filename = "heavy_tail_distribution.png"
plt.savefig(filename)
print(f"\nPlot saved as '{filename}'")
plt.show()