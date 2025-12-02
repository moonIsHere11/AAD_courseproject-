"""
Graph Coloring Problem Algorithms
Implements Backtracking (Exact), DSatur (Heuristic), and Greedy (Heuristic)
"""

import time
from typing import Dict, Set, Optional, List


def backtrack_coloring_optimized(graph: Dict[int, Set[int]], timeout: float = 60.0) -> Dict[int, int]:
    """
    Backtracking Graph Coloring - finds optimal coloring
    Complexity: O(k^n) where k is chromatic number
    
    Args:
        graph: Adjacency list
        timeout: Maximum time in seconds
        
    Returns:
        Dictionary {vertex: color}
    """
    start_time = time.time()
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    n = len(vertices)
    
    best_coloring = None
    best_num_colors = n + 1  # Upper bound
    
    coloring = {}
    
    def backtrack(idx: int, max_color_used: int):
        nonlocal best_coloring, best_num_colors
        
        if time.time() - start_time > timeout:
            return
        
        if idx == n:
            # All vertices colored
            num_colors = max_color_used + 1
            if num_colors < best_num_colors:
                best_num_colors = num_colors
                best_coloring = coloring.copy()
            return
        
        v = vertices[idx]
        neighbor_colors = {coloring.get(u) for u in graph[v] if u in coloring}
        
        # Try colors from 0 to max_color_used + 1
        for color in range(max_color_used + 2):
            if color >= best_num_colors:
                # Prune: can't improve
                break
                
            if color not in neighbor_colors:
                coloring[v] = color
                backtrack(idx + 1, max(max_color_used, color))
                del coloring[v]
    
    backtrack(0, -1)
    
    if best_coloring is None:
        # Timeout - return greedy
        return greedy_coloring(graph)
    
    return best_coloring


def dsatur_coloring(graph: Dict[int, Set[int]]) -> Dict[int, int]:
    """
    DSatur (Degree of Saturation) Heuristic
    Complexity: O(n²)
    Colors vertex with highest saturation degree
    
    Args:
        graph: Adjacency list
        
    Returns:
        Dictionary {vertex: color}
    """
    if not graph:
        return {}
    
    coloring = {}
    uncolored = set(graph.keys())
    
    # Color first vertex (highest degree) with color 0
    first_vertex = max(uncolored, key=lambda v: len(graph[v]))
    coloring[first_vertex] = 0
    uncolored.remove(first_vertex)
    
    while uncolored:
        # Calculate saturation degree for each uncolored vertex
        best_vertex = None
        best_saturation = -1
        best_degree = -1
        
        for v in uncolored:
            # Saturation degree: number of different colors used by neighbors
            neighbor_colors = {coloring[u] for u in graph[v] if u in coloring}
            saturation = len(neighbor_colors)
            degree = len(graph[v])
            
            # Pick vertex with max saturation (tie-break by degree)
            if saturation > best_saturation or (saturation == best_saturation and degree > best_degree):
                best_vertex = v
                best_saturation = saturation
                best_degree = degree
        
        # Color best_vertex with smallest available color
        neighbor_colors = {coloring[u] for u in graph[best_vertex] if u in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[best_vertex] = color
        uncolored.remove(best_vertex)
    
    return coloring


def greedy_coloring(graph: Dict[int, Set[int]], strategy: str = 'natural') -> Dict[int, int]:
    """
    Greedy Graph Coloring
    Complexity: O(n + m)
    Sequential greedy coloring
    
    Args:
        graph: Adjacency list
        strategy: Vertex ordering strategy ('natural' or 'degree')
        
    Returns:
        Dictionary {vertex: color}
    """
    if not graph:
        return {}
    
    coloring = {}
    
    if strategy == 'degree':
        vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    else:
        vertices = sorted(graph.keys())
    
    for v in vertices:
        # Find smallest color not used by neighbors
        neighbor_colors = {coloring[u] for u in graph[v] if u in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[v] = color
    
    return coloring
