"""
Comprehensive Benchmarking Script
Runs all algorithms on generated datasets and collects metrics
"""

import sys
import os
import time
import pickle
import json
from typing import Dict, List, Any

# Add src to path
_script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.insert(0, os.path.join(_script_dir, 'src'))

from sat.sat_algos import bruteforce_sat, randomization_maxsat, flipping_literals_maxsat
from graph.vertex_cover import bruteforce_vertex_cover, vertex_cover_maximal_matching, vertex_cover_lp_rounding
from graph.clique import bruteforce_clique, greedy_clique
from graph.graph_coloring import backtrack_coloring_optimized, dsatur_coloring, greedy_coloring
from set_cover.set_cover_algos import bruteforce_set_cover, greedy_set_cover


def benchmark_3sat(datasets: List[Dict]) -> List[Dict]:
    """Benchmark 3-SAT algorithms"""
    results = []
    
    print("\n" + "="*60)
    print("BENCHMARKING 3-SAT ALGORITHMS")
    print("="*60)
    
    for instance in datasets:
        print(f"\nInstance: {instance['name']} (vars={instance['n_vars']}, clauses={instance['n_clauses']})")
        instance_results = {
            'name': instance['name'],
            'n_vars': instance['n_vars'],
            'n_clauses': instance['n_clauses'],
            'algorithms': {}
        }
        
        clauses = instance['clauses']
        n_vars = instance['n_vars']
        
        # 1. Bruteforce (Exact)
        print("  Running Bruteforce...", end=" ")
        start = time.time()
        assignment, status = bruteforce_sat(clauses, n_vars, timeout=60.0)  # Increased timeout
        elapsed = time.time() - start
        
        if status == 'SAT':
            num_satisfied = len(clauses)  # All satisfied
        elif status == 'TIMEOUT':
            num_satisfied = None
        else:
            num_satisfied = 0
        
        instance_results['algorithms']['Bruteforce'] = {
            'time': elapsed,
            'status': status,
            'num_satisfied': num_satisfied,
            'total_clauses': len(clauses),
            'accuracy': 100.0 if status != 'TIMEOUT' else None
        }
        print(f"✓ {elapsed:.4f}s ({status})")
        
        # 2. Randomization (MAX-3SAT)
        print("  Running Randomization...", end=" ")
        start = time.time()
        assignment, num_satisfied = randomization_maxsat(clauses, n_vars, max_tries=1000, seed=42)
        elapsed = time.time() - start
        
        # Calculate accuracy vs bruteforce (if available)
        accuracy = None
        if instance_results['algorithms']['Bruteforce']['num_satisfied'] is not None:
            optimal = instance_results['algorithms']['Bruteforce']['num_satisfied']
            accuracy = (num_satisfied / optimal * 100) if optimal > 0 else 100.0
        
        instance_results['algorithms']['Randomization'] = {
            'time': elapsed,
            'status': 'COMPLETE',
            'num_satisfied': num_satisfied,
            'total_clauses': len(clauses),
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s ({num_satisfied}/{len(clauses)} satisfied)")
        
        # 3. Flipping Literals (Local Search)
        print("  Running Flipping Literals...", end=" ")
        start = time.time()
        assignment, num_satisfied = flipping_literals_maxsat(clauses, n_vars, max_steps=10000, seed=42)
        elapsed = time.time() - start
        
        accuracy = None
        if instance_results['algorithms']['Bruteforce']['num_satisfied'] is not None:
            optimal = instance_results['algorithms']['Bruteforce']['num_satisfied']
            accuracy = (num_satisfied / optimal * 100) if optimal > 0 else 100.0
        
        instance_results['algorithms']['Flipping Literals'] = {
            'time': elapsed,
            'status': 'COMPLETE',
            'num_satisfied': num_satisfied,
            'total_clauses': len(clauses),
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s ({num_satisfied}/{len(clauses)} satisfied)")
        
        results.append(instance_results)
    
    return results


def benchmark_vertex_cover(datasets: List[Dict]) -> List[Dict]:
    """Benchmark Vertex Cover algorithms"""
    results = []
    
    print("\n" + "="*60)
    print("BENCHMARKING VERTEX COVER ALGORITHMS")
    print("="*60)
    
    for instance in datasets:
        print(f"\nInstance: {instance['name']} (vertices={instance['n_vertices']})")
        instance_results = {
            'name': instance['name'],
            'n_vertices': instance['n_vertices'],
            'algorithms': {}
        }
        
        graph = instance['graph']
        
        # 1. Bruteforce (Exact)
        print("  Running Bruteforce...", end=" ")
        start = time.time()
        cover = bruteforce_vertex_cover(graph, timeout=60.0)  # Increased timeout
        elapsed = time.time() - start
        
        instance_results['algorithms']['Bruteforce'] = {
            'time': elapsed,
            'cover_size': len(cover),
            'accuracy': 100.0
        }
        print(f"✓ {elapsed:.4f}s (size={len(cover)})")
        
        # 2. Maximal Matching (2-approx)
        print("  Running Maximal Matching...", end=" ")
        start = time.time()
        cover = vertex_cover_maximal_matching(graph)
        elapsed = time.time() - start
        
        accuracy = None
        if instance_results['algorithms']['Bruteforce']['cover_size'] is not None:
            optimal = instance_results['algorithms']['Bruteforce']['cover_size']
            accuracy = (optimal / len(cover) * 100) if len(cover) > 0 else 100.0
        
        instance_results['algorithms']['Maximal Matching'] = {
            'time': elapsed,
            'cover_size': len(cover),
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s (size={len(cover)})")
        
        # 3. LP Rounding (2-approx)
        print("  Running LP Rounding...", end=" ")
        start = time.time()
        cover = vertex_cover_lp_rounding(graph)
        elapsed = time.time() - start
        
        accuracy = None
        if instance_results['algorithms']['Bruteforce']['cover_size'] is not None:
            optimal = instance_results['algorithms']['Bruteforce']['cover_size']
            accuracy = (optimal / len(cover) * 100) if len(cover) > 0 else 100.0
        
        instance_results['algorithms']['LP Rounding'] = {
            'time': elapsed,
            'cover_size': len(cover),
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s (size={len(cover)})")
        
        results.append(instance_results)
    
    return results


def benchmark_max_clique(datasets: List[Dict]) -> List[Dict]:
    """Benchmark Max Clique algorithms"""
    results = []
    
    print("\n" + "="*60)
    print("BENCHMARKING MAX CLIQUE ALGORITHMS")
    print("="*60)
    
    for instance in datasets:
        print(f"\nInstance: {instance['name']} (vertices={instance['n_vertices']})")
        instance_results = {
            'name': instance['name'],
            'n_vertices': instance['n_vertices'],
            'algorithms': {}
        }
        
        graph = instance['graph']
        
        # 1. Bruteforce (Exact)
        print("  Running Bruteforce...", end=" ")
        start = time.time()
        clique = bruteforce_clique(graph, timeout=60.0)  # Increased timeout
        elapsed = time.time() - start
        
        instance_results['algorithms']['Bruteforce'] = {
            'time': elapsed,
            'clique_size': len(clique),
            'accuracy': 100.0
        }
        print(f"✓ {elapsed:.4f}s (size={len(clique)})")
        
        # 2. Greedy (Heuristic)
        print("  Running Greedy...", end=" ")
        start = time.time()
        clique = greedy_clique(graph)
        elapsed = time.time() - start
        
        accuracy = None
        if instance_results['algorithms']['Bruteforce']['clique_size'] is not None:
            optimal = instance_results['algorithms']['Bruteforce']['clique_size']
            accuracy = (len(clique) / optimal * 100) if optimal > 0 else 100.0
        
        instance_results['algorithms']['Greedy'] = {
            'time': elapsed,
            'clique_size': len(clique),
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s (size={len(clique)})")
        
        results.append(instance_results)
    
    return results


def benchmark_graph_coloring(datasets: List[Dict]) -> List[Dict]:
    """Benchmark Graph Coloring algorithms"""
    results = []
    
    print("\n" + "="*60)
    print("BENCHMARKING GRAPH COLORING ALGORITHMS")
    print("="*60)
    
    for instance in datasets:
        print(f"\nInstance: {instance['name']} (vertices={instance['n_vertices']})")
        instance_results = {
            'name': instance['name'],
            'n_vertices': instance['n_vertices'],
            'algorithms': {}
        }
        
        graph = instance['graph']
        
        # 1. Backtracking (Exact)
        print("  Running Backtracking...", end=" ")
        start = time.time()
        coloring = backtrack_coloring_optimized(graph, timeout=60.0)  # Increased timeout
        elapsed = time.time() - start
        num_colors = max(coloring.values()) + 1 if coloring else 0
        
        instance_results['algorithms']['Backtracking'] = {
            'time': elapsed,
            'num_colors': num_colors,
            'accuracy': 100.0
        }
        print(f"✓ {elapsed:.4f}s (colors={num_colors})")
        
        # 2. DSatur (Heuristic)
        print("  Running DSatur...", end=" ")
        start = time.time()
        coloring = dsatur_coloring(graph)
        elapsed = time.time() - start
        num_colors = max(coloring.values()) + 1 if coloring else 0
        
        accuracy = None
        if instance_results['algorithms']['Backtracking']['num_colors'] is not None:
            optimal = instance_results['algorithms']['Backtracking']['num_colors']
            accuracy = (optimal / num_colors * 100) if num_colors > 0 else 100.0
        
        instance_results['algorithms']['DSatur'] = {
            'time': elapsed,
            'num_colors': num_colors,
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s (colors={num_colors})")
        
        # 3. Greedy (Heuristic)
        print("  Running Greedy...", end=" ")
        start = time.time()
        coloring = greedy_coloring(graph)
        elapsed = time.time() - start
        num_colors = max(coloring.values()) + 1 if coloring else 0
        
        accuracy = None
        if instance_results['algorithms']['Backtracking']['num_colors'] is not None:
            optimal = instance_results['algorithms']['Backtracking']['num_colors']
            accuracy = (optimal / num_colors * 100) if num_colors > 0 else 100.0
        
        instance_results['algorithms']['Greedy'] = {
            'time': elapsed,
            'num_colors': num_colors,
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s (colors={num_colors})")
        
        results.append(instance_results)
    
    return results


def benchmark_set_cover(datasets: List[Dict]) -> List[Dict]:
    """Benchmark Set Cover algorithms"""
    results = []
    
    print("\n" + "="*60)
    print("BENCHMARKING SET COVER ALGORITHMS")
    print("="*60)
    
    for instance in datasets:
        print(f"\nInstance: {instance['name']} (universe={instance['universe_size']}, sets={instance['num_sets']})")
        instance_results = {
            'name': instance['name'],
            'universe_size': instance['universe_size'],
            'num_sets': instance['num_sets'],
            'algorithms': {}
        }
        
        universe = instance['universe']
        sets = instance['sets']
        
        # 1. Bruteforce (Exact)
        print("  Running Bruteforce...", end=" ")
        start = time.time()
        cover, meta = bruteforce_set_cover(universe, sets, timeout=60.0)  # Increased timeout
        elapsed = time.time() - start
        
        instance_results['algorithms']['Bruteforce'] = {
            'time': elapsed,
            'cover_size': len(cover) if cover else None,
            'status': meta['status'],
            'accuracy': 100.0 if cover else None
        }
        print(f"✓ {elapsed:.4f}s (size={len(cover) if cover else 'N/A'})")
        
        # 2. Greedy (ln(n)-approx)
        print("  Running Greedy...", end=" ")
        start = time.time()
        cover, meta = greedy_set_cover(universe, sets, timeout=30.0)
        elapsed = time.time() - start
        
        accuracy = None
        if instance_results['algorithms']['Bruteforce']['cover_size'] is not None:
            optimal = instance_results['algorithms']['Bruteforce']['cover_size']
            accuracy = (optimal / len(cover) * 100) if len(cover) > 0 else 100.0
        
        instance_results['algorithms']['Greedy'] = {
            'time': elapsed,
            'cover_size': len(cover),
            'status': meta['status'],
            'accuracy': accuracy
        }
        print(f"✓ {elapsed:.4f}s (size={len(cover)})")
        
        results.append(instance_results)
    
    return results


def run_all_benchmarks(datasets_dir: str = 'datasets', output_dir: str = 'results'):
    """Run all benchmarks and save results"""
    os.makedirs(output_dir, exist_ok=True)
    
    all_results = {}
    
    # Load and benchmark each problem
    problems = ['3sat', 'vertex_cover', 'max_clique', 'graph_coloring', 'set_cover']
    
    for problem in problems:
        dataset_file = os.path.join(datasets_dir, f'{problem}_datasets.pkl')
        
        if not os.path.exists(dataset_file):
            print(f"Warning: {dataset_file} not found, skipping...")
            continue
        
        with open(dataset_file, 'rb') as f:
            datasets = pickle.load(f)
        
        if problem == '3sat':
            results = benchmark_3sat(datasets)
        elif problem == 'vertex_cover':
            results = benchmark_vertex_cover(datasets)
        elif problem == 'max_clique':
            results = benchmark_max_clique(datasets)
        elif problem == 'graph_coloring':
            results = benchmark_graph_coloring(datasets)
        elif problem == 'set_cover':
            results = benchmark_set_cover(datasets)
        
        all_results[problem] = results
        
        # Save individual problem results
        output_file = os.path.join(output_dir, f'{problem}_results.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to {output_file}")
    
    # Save combined results
    combined_file = os.path.join(output_dir, 'all_results.json')
    with open(combined_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✓ All results saved to {combined_file}")
    
    return all_results


if __name__ == '__main__':
    print("Starting comprehensive benchmark...")
    results = run_all_benchmarks()
    print("\n" + "="*60)
    print("BENCHMARK COMPLETE!")
    print("="*60)
