# NP-Complete Problems Benchmarking Suite

Comprehensive empirical analysis of 13 algorithms across 5 classical NP-complete problems, demonstrating practical trade-offs between exact, approximation, and heuristic approaches.

## 🎯 Overview

This project implements and benchmarks:
- **5 Exact Algorithms** - Guarantee optimal solutions (exponential time)
- **5 Approximation Algorithms** - Provable worst-case guarantees (polynomial time)  
- **3 Heuristic Algorithms** - Fast practical solutions (no theoretical guarantees)

### Problems & Algorithms

| Problem | Exact | Approximation | Heuristic |
|---------|-------|---------------|-----------|
| **3-SAT** | Bruteforce O(2ⁿ×m) | Randomization (7/8-approx), Flipping Literals | - |
| **Vertex Cover** | Bruteforce O(2ⁿ×m) | Maximal Matching (2-approx), LP Rounding (2-approx) | - |
| **Max Clique** | Bruteforce O(C(n,k)×k²) | - | Greedy O(n²) |
| **Graph Coloring** | Backtracking O(kⁿ) | - | DSatur O(n²), Greedy O(n+m) |
| **Set Cover** | Bruteforce O(2ᵐ×n) | Greedy (ln(n)-approx) | - |

## 📁 Project Structure

```
aad_project/
├── src/
│   ├── sat/sat_algos.py              # 3-SAT algorithms
│   ├── graph/
│   │   ├── vertex_cover.py           # Vertex Cover algorithms
│   │   ├── clique.py                 # Max Clique algorithms
│   │   └── graph_coloring.py         # Graph Coloring algorithms
│   └── set_cover/set_cover_algos.py  # Set Cover algorithms
├── generate_datasets.py              # Dataset generation (Erdős-Rényi graphs)
├── run_benchmarks.py                 # Benchmark execution with timing/accuracy
├── generate_plots.py                 # Matplotlib visualizations
├── generate_report.py                # LaTeX report generator
├── latex_upload/                     # Ready for Overleaf (report + plots)
└── README.md
```

## 🚀 Quick Start

### Prerequisites

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install numpy scipy matplotlib
```

### Run Complete Pipeline

```bash
# 1. Generate datasets (8 size categories × 2 instances × 5 problems = 80 instances)
python generate_datasets.py

# 2. Run all benchmarks (may take 5-10 minutes for complete run)
python run_benchmarks.py

# 3. Generate visualizations (10 plots: time + accuracy for each problem)
python generate_plots.py

# 4. Generate LaTeX report (comprehensive 500+ line document)
python generate_report.py

# 5. Results ready in latex_upload/ for Overleaf
```

## 📊 Key Results

From our benchmarking (complete data with 8 problem sizes):

### Speed-up Over Exact Algorithms (at largest instances)

| Problem | Instance Size | Exact Time | Approx/Heuristic Time | Speed-up |
|---------|---------------|------------|----------------------|----------|
| 3-SAT | 20 vars | 3.14s | 0.02s | **155×** |
| Vertex Cover | 22 vertices | 1.36s | 0.0001s | **10,000×** |
| Max Clique | 22 vertices | 0.74s | 0.00005s | **15,000×** |
| Graph Coloring | 22 vertices | 0.015s | 0.0001s | **150×** |
| Set Cover | 22 sets | 0.32s | 0.00006s | **5,300×** |

### Accuracy vs Optimal Solutions

| Algorithm | Accuracy Range | Notes |
|-----------|----------------|-------|
| **3-SAT Randomization** | 96-100% | Matches 7/8 theoretical guarantee |
| **3-SAT Flipping Literals** | 95-100% | 50-100× faster than randomization |
| **Vertex Cover (both)** | 50-100% | Average 1.5-1.8× optimal (better than 2-approx guarantee) |
| **Max Clique Greedy** | 75-100% | Optimal in 81% of instances |
| **Graph Coloring DSatur** | Optimal 87.5% | Usually within +1 color |
| **Set Cover Greedy** | 85-100% | Average 1.13× optimal (far better than ln(n) guarantee) |

## 📈 Output Files

After running the pipeline:

```
datasets/          # Pickle files with test instances (regenerable)
results/           # JSON benchmark results (regenerable)
plots/             # PNG/SVG visualizations (regenerable)
report/            # LaTeX source + compiled PDF (regenerable)
latex_upload/      # Self-contained folder for Overleaf
  ├── benchmark_report.tex
  └── plots/       # All 20 plot files (PNG + SVG)
```

**For Overleaf**: Upload entire `latex_upload/` folder (or zip it first)

## 🔬 Benchmark Metrics

For each algorithm × instance combination:
- **Execution time** (seconds, averaged if multiple runs)
- **Solution quality** (cover size, clique size, colors, satisfied clauses, sets)
- **Accuracy vs optimal** (percentage, computed from exact algorithm baseline)
- **Status** (COMPLETE, TIMEOUT after 60s, INFEASIBLE for set cover)

## 🎨 Visualizations

10 plots generated (5 problems × 2 metrics):

1. **Time Comparison** - Bar charts showing execution time across instances
   - Demonstrates exponential growth of exact algorithms
   - Shows constant/polynomial time of approximations
   
2. **Accuracy Comparison** - Bar charts showing approximation quality
   - Compares approximation/heuristic solutions vs optimal baseline
   - Highlights practical performance exceeding theoretical guarantees

## 📝 LaTeX Report

Comprehensive 500+ line report includes:

- **Algorithm descriptions** with complexity analysis
- **Benchmark results tables** (partial, showing 6 representative instances)
- **Analysis sections** for each problem (exponential growth, crossover points, recommendations)
- **Comparative analysis** (speed-ups, accuracy, theoretical vs empirical)
- **Practical recommendations** (when to use exact vs approximation)
- **10 embedded plots** (time + accuracy for all 5 problems)

## ⚙️ Customization

### Modify Problem Sizes

Edit `generate_datasets.py`:

```python
sat_configs = [
    (5, 10, 'tiny'),      # (n_vars, n_clauses, label)
    (10, 30, 'medium'),   # Add/remove configurations
    (15, 50, 'large'),
]
```

### Adjust Timeouts

Edit `run_benchmarks.py`:

```python
# Line ~50: Change timeout for exact algorithms
assignment, status = bruteforce_sat(clauses, n_vars, timeout=30.0)  # Default: 60s
```

## 🔍 Key Insights from Benchmarks

1. **Exponential Wall**: Exact algorithms hit practical limit at n≈15-22 depending on problem
2. **Approximation Quality**: Real performance far exceeds worst-case theoretical bounds
3. **Local Search Power**: Flipping Literals outperforms pure randomization for 3-SAT
4. **Heuristic Success**: DSatur (Graph Coloring) finds optimal 87.5% of time with no guarantee
5. **Crossover Points**: Approximations become superior around n=15-18 for most problems

## 📚 Algorithms Implemented

### Exact Algorithms
- **Bruteforce SAT**: Enumerate all 2ⁿ assignments
- **Bruteforce Vertex Cover**: Try all 2ⁿ subsets
- **Bruteforce Max Clique**: Check all C(n,k) combinations
- **Backtracking Coloring**: Branch-and-bound with pruning
- **Bruteforce Set Cover**: Try all 2ᵐ set combinations

### Approximation Algorithms  
- **Randomization (3-SAT)**: Random assignment, 7/8 expected ratio
- **Maximal Matching (VC)**: 2-approximation, O(m) time
- **LP Rounding (VC)**: 2-approximation via LP relaxation
- **Greedy Set Cover**: ln(n)-approximation (best possible)

### Heuristics
- **Flipping Literals (3-SAT)**: Local search with greedy flips
- **Greedy Clique**: Degree-based greedy construction
- **DSatur (Coloring)**: Degree of saturation heuristic
- **Greedy Coloring**: Sequential assignment

## 📄 License

MIT License - Free for academic and commercial use.

## 🙏 Acknowledgments

Algorithms based on classic results from:
- Vazirani (2001) - *Approximation Algorithms*
- Cormen et al. (2009) - *Introduction to Algorithms*
- Williamson & Shmoys (2011) - *The Design of Approximation Algorithms*

---

**Total Lines of Code**: ~2,500 (Python implementations + LaTeX generation)  
**Total Benchmark Instances**: 80 (16 per problem)  
**Estimated Full Run Time**: 5-10 minutes (with all instances, 60s timeout)
