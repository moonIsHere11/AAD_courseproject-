"""
Maximum Clique Problem Algorithms
Implements Bruteforce (Exact) and Greedy (Heuristic)
"""

import time
from typing import Set, Dict, List
from itertools import combinations


def bruteforce_clique(graph: Dict[int, Set[int]], timeout: float = 60.0) -> Set[int]:
    """
    Bruteforce Maximum Clique - tries all subsets from largest to smallest
    Complexity: O(C(n,k) × k²) where k is clique size
    
    Args:
        graph: Adjacency list representation
        timeout: Maximum time in seconds
        
    Returns:
        Set of vertices in maximum clique
    """
    start_time = time.time()
    vertices = list(graph.keys())
    n = len(vertices)
    
    # Try subsets from largest to smallest
    for k in range(n, 0, -1):
        if time.time() - start_time > timeout:
            # Timeout - return empty
            return set()
            
        for subset in combinations(vertices, k):
            # Check if subset forms a clique (all pairs connected)
            is_clique = True
            for i in range(len(subset)):
                for j in range(i + 1, len(subset)):
                    u, v = subset[i], subset[j]
                    if v not in graph.get(u, set()):
                        is_clique = False
                        break
                if not is_clique:
                    break
            
            if is_clique:
                return set(subset)
    
    return set()


def greedy_clique(graph: Dict[int, Set[int]]) -> Set[int]:
    """
    Greedy Maximum Clique Heuristic
    Complexity: O(n²)
    Orders vertices by degree, greedily extends clique
    
    Args:
        graph: Adjacency list
        
    Returns:
        Set of vertices (maximal clique, not necessarily maximum)
    """
    if not graph:
        return set()
    
    # Order vertices by degree (descending)
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    
    current_clique = set()
    
    for v in vertices:
        # Check if v is connected to all vertices in current clique
        if all(u in graph.get(v, set()) for u in current_clique):
            current_clique.add(v)
            
            # Try to extend with remaining candidates
            candidates = set(graph[v]) - current_clique
            
            while candidates:
                # Pick candidate with max degree
                best = max(candidates, key=lambda x: len(graph.get(x, set()) & candidates))
                
                # Check if best is connected to all in clique
                if all(u in graph.get(best, set()) for u in current_clique):
                    current_clique.add(best)
                    # Update candidates
                    candidates = candidates & graph.get(best, set())
                else:
                    candidates.remove(best)
    
    return current_clique
