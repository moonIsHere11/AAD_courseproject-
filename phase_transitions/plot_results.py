"""
Plots all results from the 3-SAT Phase Transition experiment.
Generates 3 plots:
1. P(SAT) for n=25, 50, 75
2. Difficulty for n=25, 50, 75
3. Combined P(SAT) and Difficulty for n=75
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_data(n_val: int) -> pd.DataFrame:
    """Loads the results JSON file for a specific n."""
    results_file = f'data/full_experiment_results_n{n_val}.json'
    
    if not os.path.exists(results_file):
        print(f"Warning: Results file not found at {results_file}")
        print("Please run 'python run_experiment.py' first.")
        return None
    
    # Load the main data into a DataFrame
    df = pd.read_json(results_file)
    return df

def plot_task1_comparison(data_dict: dict):
    """
    Plots the P(SAT) 'cliff' for all n values on one graph.
    """
    plt.figure(figsize=(12, 7))
    
    for n, df in data_dict.items():
        # Show datapoints and connect them with a line
        plt.plot(df['alpha_values'], df['satisfiability_probability'], 
                 label=f'n = {n}', marker='o', linestyle='-', markersize=6, lw=1.5)
    
    plt.axvline(x=4.26, color='k', linestyle='--', label='Theoretical Threshold (α ≈ 4.26)')
    
    plt.title('Task 1: Satisfiability vs. Alpha (n=25, 50, 75)', fontsize=16)
    plt.xlabel('Clause-to-Variable Ratio (α = m/n)', fontsize=12)
    plt.ylabel('Probability of Satisfiability', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.ylim(-0.05, 1.05)
    
    filename = 'task1_comparison.png'
    plt.savefig(filename)
    print(f"Task 1 comparison plot saved as '{filename}'")
    plt.show()

def plot_task2_comparison(data_dict: dict):
    """
    Plots the Difficulty 'spike' for all n values on one graph.
    """
    plt.figure(figsize=(12, 7))
    
    for n, df in data_dict.items():
        # Show datapoints and connect them with a line
        plt.plot(df['alpha_values'], df['average_conflicts'], 
                 label=f'n = {n}', marker='s', linestyle='-', markersize=6, lw=1.5)
    
    plt.axvline(x=4.26, color='k', linestyle='--', label='Theoretical Threshold (α ≈ 4.26)')
    
    plt.title('Task 2: Computational Difficulty vs. Alpha (n=25, 50, 75)', fontsize=16)
    plt.xlabel('Clause-to-Variable Ratio (α = m/n)', fontsize=12)
    plt.ylabel('Average Conflicts ("Deadends")', fontsize=12)
    
    # Use a log scale on Y-axis to see all spikes
    plt.yscale('log')
    
    plt.legend(fontsize=11)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    filename = 'task2_comparison.png'
    plt.savefig(filename)
    print(f"Task 2 comparison plot saved as '{filename}'")
    plt.show()

def plot_n75_combined(df_75: pd.DataFrame):
    """
    Plots P(SAT) and Difficulty for n=75 on the same graph
    using a secondary Y-axis.
    """
    
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # --- Plot 1: P(SAT) (Left Y-axis) ---
    color = 'tab:blue'
    ax1.set_xlabel('Clause-to-Variable Ratio (α = m/n)', fontsize=12)
    ax1.set_ylabel('Probability of Satisfiability', color=color, fontsize=12)
    # Show datapoints and connect them for P(SAT)
    ax1.plot(df_75['alpha_values'], df_75['satisfiability_probability'], 
             color=color, label='P(SAT)', marker='o', linestyle='-', markersize=6, lw=1.5)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')

    # --- Plot 2: Difficulty (Right Y-axis) ---
    ax2 = ax1.twinx()  # Create a second Y-axis sharing the same X-axis
    color = 'tab:red'
    ax2.set_ylabel('Average Conflicts', color=color, fontsize=12)
    # Show datapoints and connect them for Avg. Conflicts (log-scaled axis)
    ax2.plot(df_75['alpha_values'], df_75['average_conflicts'], 
             color=color, label='Avg. Conflicts', marker='s', linestyle='-', markersize=6, lw=1.5)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yscale('log') # Use log scale for spike

    # --- Highlighting Phase Transition ---
    ax1.axvspan(4.0, 4.5, color='gray', alpha=0.3, label='Phase Transition')

    # --- Combined Legend ---
    # We ask both axes for their labels and combine them
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper center')

    plt.title('Combined P(SAT) and Difficulty for n=75', fontsize=16)
    fig.tight_layout()  # Adjust plot to prevent label overlap
    
    filename = 'n75_combined.png'
    plt.savefig(filename)
    print(f"n=75 combined plot saved as '{filename}'")
    plt.show()

if __name__ == "__main__":
    n_values_to_plot = [25, 50, 75]
    
    # Load all data into a dictionary
    all_data = {}
    for n in n_values_to_plot:
        df = load_data(n)
        if df is not None:
            all_data[n] = df
            
    if not all_data:
        print("No data was loaded. Exiting.")
    else:
        # Generate the 3 plots
        print("\nGenerating Plot 1: P(SAT) Comparison")
        plot_task1_comparison(all_data)
        
        print("\nGenerating Plot 2: Difficulty Comparison")
        plot_task2_comparison(all_data)
        
        # Check if n=75 data exists before plotting
        if 75 in all_data:
            print("\nGenerating Plot 3: n=75 Combined")
            plot_n75_combined(all_data[75])
        else:
            print("\nSkipping n=75 combined plot (data not found).")