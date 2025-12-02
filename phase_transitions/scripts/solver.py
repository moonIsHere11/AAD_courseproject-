"""
3SAT Solver (PySAT-based) and Instance Generator
"""

import random
from typing import List, Tuple, Dict
from pysat.solvers import Glucose3  # Import the fast C++ solver

class Clause:
    """Represents a clause with exactly three literals."""
    
    def __init__(self, literals: Tuple[int, int, int]):
        if len(literals) != 3:
            raise ValueError("A clause must have exactly 3 literals")
        # Store as a list for PySAT
        self.literals = list(literals) 
    
    def __repr__(self):
        return f"({self.literals[0]} ∨ {self.literals[1]} ∨ {self.literals[2]})"


class ThreeSAT:
    """Represents a 3SAT instance, solvable with PySAT."""
    
    def __init__(self, n_variables: int, clauses: List[Clause]):
        self.n_variables = n_variables
        self.clauses = clauses
        self.m = len(clauses)
        self.alpha = self.m / self.n_variables if self.n_variables > 0 else 0
        
        # This is the format PySAT needs: a list of lists
        self.cnf_clauses = [c.literals for c in clauses]
    
    def is_satisfiable(self) -> Tuple[bool, dict]:
        """
        Check satisfiability using the Glucose3 solver.
        
        Returns:
            Tuple of (is_satisfiable, stats_dictionary)
        """
        stats = {'conflicts': 0, 'decisions': 0}
        
        with Glucose3(bootstrap_with=self.cnf_clauses) as solver:
            is_sat = solver.solve()
            
            # Get the solver's internal stats
            solver_stats = solver.accum_stats()
            if solver_stats:
                stats['conflicts'] = solver_stats.get('conflicts', 0)
                stats['decisions'] = solver_stats.get('decisions', 0)
        
        # This now returns the stats we need for the *next* task
        return is_sat, stats

    def __repr__(self):
        return f"3SAT(n={self.n_variables}, m={self.m}, α={self.alpha:.2f})"


def generate_random_3sat(n_variables: int, m_clauses: int, seed: int = None) -> ThreeSAT:
    """
    Generate a random 3SAT instance. (This is your code, it's perfect).
    """
    if seed is not None:
        random.seed(seed)
    
    clauses = []
    
    for _ in range(m_clauses):
        variables = random.sample(range(1, n_variables + 1), 3)
        literals = tuple(
            var if random.random() > 0.5 else -var
            for var in variables
        )
        clauses.append(Clause(literals))
    
    return ThreeSAT(n_variables, clauses)