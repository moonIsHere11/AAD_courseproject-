"""
Dataset Generator for All Problems
Generates synthetic test instances with varying sizes
"""

import random
import pickle
import os
from typing import List, Set, Dict, Tuple


def generate_3sat_instance(n_vars: int, n_clauses: int, seed: int = None) -> List[List[int]]:
    """Generate random 3-SAT instance"""
    if seed is not None:
        random.seed(seed)
    
    clauses = []
    for _ in range(n_clauses):
        # Pick 3 distinct variables
        vars_in_clause = random.sample(range(1, n_vars + 1), 3)
        # Randomly negate each variable
        clause = [v if random.random() < 0.5 else -v for v in vars_in_clause]
        clauses.append(clause)
    
    return clauses


def generate_graph(n_vertices: int, edge_probability: float, seed: int = None) -> Dict[int, Set[int]]:
    """Generate random graph using Erdős-Rényi model"""
    if seed is not None:
        random.seed(seed)
    
    graph = {i: set() for i in range(n_vertices)}
    
    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if random.random() < edge_probability:
                graph[i].add(j)
                graph[j].add(i)
    
    return graph


def generate_set_cover_instance(universe_size: int, num_sets: int, avg_set_size: int, seed: int = None) -> Tuple[Set[int], List[Set[int]]]:
    """Generate random set cover instance"""
    if seed is not None:
        random.seed(seed)
    
    universe = set(range(universe_size))
    sets = []
    
    for _ in range(num_sets):
        # Vary set size around average
        set_size = max(1, int(random.gauss(avg_set_size, avg_set_size / 3)))
        set_size = min(set_size, universe_size)
        s = set(random.sample(list(universe), set_size))
        sets.append(s)
    
    return universe, sets


def generate_all_datasets(output_dir: str = 'datasets'):
    """Generate all benchmark datasets"""
    os.makedirs(output_dir, exist_ok=True)
    
    datasets = {
        '3sat': [],
        'vertex_cover': [],
        'max_clique': [],
        'graph_coloring': [],
        'set_cover': []
    }
    
    # 3-SAT instances
    print("Generating 3-SAT instances...")
    sat_configs = [
        (5, 10, 'tiny'),
        (7, 18, 'small'),
        (9, 27, 'medium'),
        (11, 35, 'medium_large'),
        (13, 42, 'large'),
        (15, 50, 'xlarge'),
        (17, 60, 'xxlarge'),
        (20, 80, 'huge'),
    ]
    for n_vars, n_clauses, size in sat_configs:
        for i in range(2):  # 2 instances per size for faster generation
            clauses = generate_3sat_instance(n_vars, n_clauses, seed=1000 + i)
            datasets['3sat'].append({
                'name': f'{size}_{i+1}',
                'n_vars': n_vars,
                'n_clauses': n_clauses,
                'clauses': clauses
            })
    
    # Vertex Cover / Max Clique / Graph Coloring (same graphs)
    print("Generating graph instances...")
    graph_configs = [
        (6, 0.5, 'tiny'),
        (8, 0.5, 'small'),
        (10, 0.5, 'medium'),
        (12, 0.45, 'medium_large'),
        (14, 0.45, 'large'),
        (16, 0.4, 'xlarge'),
        (18, 0.4, 'xxlarge'),
        (22, 0.35, 'huge'),
    ]
    for n_vertices, edge_prob, size in graph_configs:
        for i in range(2):
            graph = generate_graph(n_vertices, edge_prob, seed=2000 + i)
            graph_data = {
                'name': f'{size}_{i+1}',
                'n_vertices': n_vertices,
                'edge_prob': edge_prob,
                'graph': graph
            }
            datasets['vertex_cover'].append(graph_data.copy())
            datasets['max_clique'].append(graph_data.copy())
            datasets['graph_coloring'].append(graph_data.copy())
    
    # Set Cover instances
    print("Generating set cover instances...")
    setcover_configs = [
        (10, 6, 4, 'tiny'),
        (15, 8, 5, 'small'),
        (20, 10, 6, 'medium'),
        (25, 12, 7, 'medium_large'),
        (30, 14, 8, 'large'),
        (35, 16, 9, 'xlarge'),
        (40, 18, 10, 'xxlarge'),
        (50, 22, 12, 'huge'),
    ]
    for univ_size, num_sets, avg_size, size in setcover_configs:
        for i in range(2):
            universe, sets = generate_set_cover_instance(univ_size, num_sets, avg_size, seed=3000 + i)
            datasets['set_cover'].append({
                'name': f'{size}_{i+1}',
                'universe_size': univ_size,
                'num_sets': num_sets,
                'universe': universe,
                'sets': sets
            })
    
    # Save datasets
    for problem, data in datasets.items():
        filepath = os.path.join(output_dir, f'{problem}_datasets.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"Saved {len(data)} instances for {problem}")
    
    print(f"\nAll datasets saved to {output_dir}/")
    return datasets


if __name__ == '__main__':
    datasets = generate_all_datasets()
    print("\n✓ Dataset generation complete!")
