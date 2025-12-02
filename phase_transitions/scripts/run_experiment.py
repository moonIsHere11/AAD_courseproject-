"""
Fresh start for 3-SAT Phase Transition Experiment
Captures BOTH P(SAT) and Difficulty (Conflicts)
(Corrected Version 2)
"""

import random
import numpy as np
import json
import os
import time
from pysat.solvers import Glucose3 # Using a fast, standard solver

def generate_random_formula(n_vars: int, n_clauses: int) -> list:
    """
    Generates a random 3-CNF formula.
    (This function is unchanged)
    """
    variables = list(range(1, n_vars + 1))
    formula = []
    
    for _ in range(n_clauses):
        clause_vars = random.sample(variables, 3)
        clause = [
            var * random.choice([-1, 1]) 
            for var in clause_vars
        ]
        formula.append(clause)
        
    return formula

def run_experiment(alpha_values: list, n_vars: int, samples_per_alpha: int) -> dict:
    """
    Runs the full experiment for BOTH tasks.
    """
    
    print(f"Starting Full Experiment: n={n_vars}, samples/alpha={samples_per_alpha}")
    print("=" * 60)
    
    results = {
        'n_variables': n_vars,
        'samples_per_alpha': samples_per_alpha,
        'alpha_values': [],
        'satisfiability_probability': [],
        'average_conflicts': []
    }
    
    for alpha in alpha_values:
        m_clauses = int(alpha * n_vars)
        satisfiable_count = 0
        conflict_counts = []
        
        print(f"\n[Testing α = {alpha:.2f}] (n={n_vars}, m={m_clauses})")
        start_time = time.time()
        
        for i in range(samples_per_alpha):
            formula = generate_random_formula(n_vars, m_clauses)
            
            with Glucose3(bootstrap_with=formula) as solver:
                is_sat = solver.solve()
                if is_sat:
                    satisfiable_count += 1
                
                # Get solver statistics (conflicts, decisions, etc.)
                stats = solver.accum_stats()
                conflicts = stats.get('conflicts', 0)
                conflict_counts.append(conflicts)
            
            if (i + 1) % 20 == 0:
                print(f"  ... completed {i+1}/{samples_per_alpha}", end='\r')
        
        prob = satisfiable_count / samples_per_alpha
        avg_conflicts = np.mean(conflict_counts)
        
        results['alpha_values'].append(alpha)
        results['satisfiability_probability'].append(prob)
        results['average_conflicts'].append(avg_conflicts)
        
        end_time = time.time()
        print(f"  -> P(SAT) = {prob:.3f} | Avg. Conflicts = {avg_conflicts:.2f} (in {end_time - start_time:.2f}s)")

    print("\n" + "=" * 60)
    print("Experiment finished.")
    return results

def save_results(results: dict, filename: str):
    """Saves the results dictionary to a JSON file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    # --- Experiment Parameters ---
    N_VALUES = [25, 50, 75]          # run experiments for these n values
    SAMPLES_PER_ALPHA = 150          # samples per alpha for each n (requested)
    RESULTS_DIR = 'data'
    # -----------------------------

    # Build the alpha sweep (same as before)
    alpha_values = []
    alpha_values.extend(np.arange(1.0, 3.0, 0.5))
    alpha_values.extend(np.arange(3.0, 6.0, 0.1))
    alpha_values.extend(np.arange(6.0, 8.5, 0.5))
    alpha_values = sorted(list(set([round(a, 2) for a in alpha_values])))

    # Run experiments for each n and save to a per-n JSON file
    for n in N_VALUES:
        print(f"\n=== Running experiments for n={n} (samples/alpha={SAMPLES_PER_ALPHA}) ===")
        results = run_experiment(alpha_values, n, SAMPLES_PER_ALPHA)
        out_file = os.path.join(RESULTS_DIR, f'full_experiment_results_n{n}.json')
        save_results(results, out_file)

    print("All runs complete.")