"""
Vertex Cover Problem Algorithms
Implements Bruteforce (Exact), Maximal Matching (2-approx), and LP Rounding (2-approx)
"""

import time
from typing import Set, Dict, List, Tuple
from itertools import combinations
import numpy as np
from scipy.optimize import linprog


def bruteforce_vertex_cover(graph: Dict[int, Set[int]], timeout: float = 60.0) -> Set[int]:
    """
    Bruteforce Vertex Cover - tries all subsets from size 0 to n
    Complexity: O(2^n × m)
    
    Args:
        graph: Adjacency list representation {vertex: set of neighbors}
        timeout: Maximum time in seconds
        
    Returns:
        Set of vertices in minimum cover
    """
    start_time = time.time()
    vertices = list(graph.keys())
    n = len(vertices)
    
    # Get all edges
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:  # Avoid duplicates
                edges.append((u, v))
    
    # Try subsets of increasing size
    for k in range(n + 1):
        if time.time() - start_time > timeout:
            # Timeout - return trivial cover
            return set(vertices)
            
        for subset in combinations(vertices, k):
            cover_set = set(subset)
            # Check if this is a valid vertex cover
            is_valid = True
            for u, v in edges:
                if u not in cover_set and v not in cover_set:
                    is_valid = False
                    break
            
            if is_valid:
                return cover_set
    
    return set(vertices)


def vertex_cover_maximal_matching(graph: Dict[int, Set[int]]) -> Set[int]:
    """
    Vertex Cover via Maximal Matching (2-approximation)
    Complexity: O(m)
    Approximation Ratio: 2
    
    Args:
        graph: Adjacency list
        
    Returns:
        Set of vertices (≤ 2 × OPT)
    """
    cover = set()
    remaining_edges = []
    
    # Get all edges
    for u in graph:
        for v in graph[u]:
            if u < v:
                remaining_edges.append((u, v))
    
    # Build maximal matching greedily
    covered_vertices = set()
    
    for u, v in remaining_edges:
        if u not in covered_vertices and v not in covered_vertices:
            # Add edge to matching
            cover.add(u)
            cover.add(v)
            covered_vertices.add(u)
            covered_vertices.add(v)
    
    return cover


def vertex_cover_lp_rounding(graph: Dict[int, Set[int]]) -> Set[int]:
    """
    Vertex Cover via LP Relaxation and Rounding (2-approximation)
    Complexity: O(n³) using scipy.linprog
    Approximation Ratio: 2
    
    Args:
        graph: Adjacency list
        
    Returns:
        Set of vertices (≤ 2 × OPT)
    """
    vertices = list(graph.keys())
    n = len(vertices)
    
    if n == 0:
        return set()
    
    # Create vertex index mapping
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    
    # Get all edges
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.append((u, v))
    
    if not edges:
        return set()
    
    # Formulate LP: minimize sum of x_v
    c = np.ones(n)  # Objective: minimize sum of all variables
    
    # Constraints: x_u + x_v >= 1 for each edge
    A_ub = []
    b_ub = []
    
    for u, v in edges:
        constraint = np.zeros(n)
        constraint[vertex_to_idx[u]] = -1
        constraint[vertex_to_idx[v]] = -1
        A_ub.append(constraint)
        b_ub.append(-1)  # -x_u - x_v <= -1  =>  x_u + x_v >= 1
    
    # Bounds: 0 <= x_v <= 1
    bounds = [(0, 1) for _ in range(n)]
    
    # Solve LP
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if not result.success:
        # Fallback to trivial cover
        return set(vertices)
    
    # Round: include vertex if x_v >= 0.5
    cover = set()
    for i, val in enumerate(result.x):
        if val >= 0.5:
            cover.add(vertices[i])
    
    return cover
