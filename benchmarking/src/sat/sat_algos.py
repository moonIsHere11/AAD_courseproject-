"""
3-SAT Problem Algorithms
Implements Bruteforce (Exact), Randomization (Approximation), and Flipping Literals (Local Search)
"""

import random
import time
from typing import List, Tuple, Dict, Optional


def bruteforce_sat(clauses: List[List[int]], n_vars: int, timeout: float = 60.0) -> Tuple[Optional[Dict[int, bool]], str]:
    """
    Bruteforce SAT solver - tries all 2^n assignments
    Complexity: O(2^n × m)
    
    Args:
        clauses: List of clauses, each clause is list of literals (negative = NOT)
        n_vars: Number of variables
        timeout: Maximum time in seconds
        
    Returns:
        (assignment dict, status) where status is 'SAT' or 'UNSAT'
    """
    start_time = time.time()
    
    # Try all 2^n assignments
    for i in range(2 ** n_vars):
        if time.time() - start_time > timeout:
            return None, 'TIMEOUT'
            
        # Create assignment from binary representation
        assignment = {}
        for var in range(1, n_vars + 1):
            assignment[var] = bool((i >> (var - 1)) & 1)
        
        # Check if this assignment satisfies all clauses
        if all(any((lit > 0 and assignment[abs(lit)]) or (lit < 0 and not assignment[abs(lit)]) 
                   for lit in clause) for clause in clauses):
            return assignment, 'SAT'
    
    return None, 'UNSAT'


def randomization_maxsat(clauses: List[List[int]], n_vars: int, max_tries: int = 1000, seed: Optional[int] = None) -> Tuple[Dict[int, bool], int]:
    """
    Randomization algorithm for MAX-3SAT
    Approximation Ratio: Expected 7/8 for MAX-3SAT
    Complexity: O(max_tries × m)
    
    Args:
        clauses: List of clauses
        n_vars: Number of variables
        max_tries: Number of random trials
        seed: Random seed for reproducibility
        
    Returns:
        (best assignment dict, number of satisfied clauses)
    """
    if seed is not None:
        random.seed(seed)
    
    best_assignment = None
    best_count = 0
    
    for _ in range(max_tries):
        # Random assignment: each variable is True with probability 1/2
        assignment = {var: random.choice([True, False]) for var in range(1, n_vars + 1)}
        
        # Count satisfied clauses
        count = sum(1 for clause in clauses 
                   if any((lit > 0 and assignment[abs(lit)]) or (lit < 0 and not assignment[abs(lit)]) 
                         for lit in clause))
        
        if count > best_count:
            best_count = count
            best_assignment = assignment.copy()
    
    return best_assignment, best_count


def flipping_literals_maxsat(clauses: List[List[int]], n_vars: int, max_steps: int = 10000, seed: Optional[int] = None) -> Tuple[Dict[int, bool], int]:
    """
    Local search for MAX-3SAT using greedy variable flipping
    Only flips variables from unsatisfied clauses
    Complexity: O(max_steps × k × m) where k is avg variables per unsatisfied clause
    
    Args:
        clauses: List of clauses
        n_vars: Number of variables
        max_steps: Maximum number of flipping steps
        seed: Random seed
        
    Returns:
        (assignment dict, number of satisfied clauses)
    """
    if seed is not None:
        random.seed(seed)
    
    # Start with random assignment
    assignment = {var: random.choice([True, False]) for var in range(1, n_vars + 1)}
    
    def count_satisfied():
        return sum(1 for clause in clauses 
                  if any((lit > 0 and assignment[abs(lit)]) or (lit < 0 and not assignment[abs(lit)]) 
                        for lit in clause))
    
    for _ in range(max_steps):
        current_count = count_satisfied()
        
        # Find unsatisfied clauses
        unsatisfied = [clause for clause in clauses 
                      if not any((lit > 0 and assignment[abs(lit)]) or (lit < 0 and not assignment[abs(lit)]) 
                                for lit in clause)]
        
        if not unsatisfied:
            # All clauses satisfied!
            return assignment, len(clauses)
        
        # Collect candidate variables from unsatisfied clauses
        candidates = set()
        for clause in unsatisfied:
            for lit in clause:
                candidates.add(abs(lit))
        
        # Try flipping each candidate and track best improvement
        best_var = None
        best_improvement = 0
        
        for var in candidates:
            # Flip variable
            assignment[var] = not assignment[var]
            new_count = count_satisfied()
            improvement = new_count - current_count
            
            # Flip back
            assignment[var] = not assignment[var]
            
            if improvement > best_improvement:
                best_improvement = improvement
                best_var = var
        
        # Perform best flip if it improves
        if best_improvement > 0 and best_var is not None:
            assignment[best_var] = not assignment[best_var]
        else:
            # Local optimum reached
            break
    
    final_count = count_satisfied()
    return assignment, final_count
