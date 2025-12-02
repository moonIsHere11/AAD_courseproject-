"""
Set Cover Problem Algorithms
Implements Bruteforce (Exact) and Greedy (ln(n)-Approximation)
"""

import time
from typing import List, Set, Tuple, Optional
from itertools import combinations


def bruteforce_set_cover(universe: Set[int], sets: List[Set[int]], timeout: float = 60.0) -> Tuple[Optional[List[int]], dict]:
    """
    Bruteforce Set Cover - tries all combinations from size 1 to m
    Complexity: O(2^m × n) where m is number of sets
    
    Args:
        universe: Set of all elements to cover
        sets: List of sets
        timeout: Maximum time in seconds
        
    Returns:
        (list of set indices, metadata dict)
    """
    start_time = time.time()
    m = len(sets)
    
    # Try combinations of increasing size
    for k in range(1, m + 1):
        if time.time() - start_time > timeout:
            return None, {'status': 'TIMEOUT', 'num_sets': 0}
        
        for combo in combinations(range(m), k):
            # Check if this combination covers universe
            covered = set()
            for idx in combo:
                covered |= sets[idx]
            
            if covered >= universe:
                return list(combo), {'status': 'OPTIMAL', 'num_sets': k, 'coverage': len(covered)}
    
    return None, {'status': 'INFEASIBLE', 'num_sets': 0}


def greedy_set_cover(universe: Set[int], sets: List[Set[int]], timeout: float = 60.0) -> Tuple[List[int], dict]:
    """
    Greedy Set Cover (ln(n)-Approximation)
    Complexity: O(m × n)
    Approximation Ratio: H(n) ≤ ln(n) + 1
    
    Args:
        universe: Set of all elements to cover
        sets: List of sets
        timeout: Maximum time in seconds
        
    Returns:
        (list of set indices, metadata dict)
    """
    start_time = time.time()
    uncovered = universe.copy()
    selected = []
    
    while uncovered:
        if time.time() - start_time > timeout:
            return selected, {'status': 'TIMEOUT', 'num_sets': len(selected), 'coverage': len(universe) - len(uncovered)}
        
        # Find set covering most uncovered elements
        best_idx = None
        best_count = 0
        
        for idx, s in enumerate(sets):
            if idx not in selected:
                count = len(s & uncovered)
                if count > best_count:
                    best_count = count
                    best_idx = idx
        
        if best_idx is None or best_count == 0:
            # Can't cover more
            break
        
        selected.append(best_idx)
        uncovered -= sets[best_idx]
    
    if uncovered:
        return selected, {'status': 'PARTIAL', 'num_sets': len(selected), 'coverage': len(universe) - len(uncovered)}
    
    return selected, {'status': 'COMPLETE', 'num_sets': len(selected), 'coverage': len(universe)}
