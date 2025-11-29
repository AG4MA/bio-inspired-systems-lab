# ant_foraging_simulation.py
# Purpose: Simulate ant colony optimization for pathfinding
# Demonstrates emergent optimal path discovery

import random
from agent import AntAgent
from environment import AntColonyEnvironment


def run_simulation(num_nodes=15, num_ants=20, num_iterations=50, q_constant=100.0):
    """
    Run ant colony optimization simulation.

    Inputs:
        num_nodes (int): Number of graph nodes
        num_ants (int): Ants per iteration
        num_iterations (int): Number of iterations
        q_constant (float): Pheromone deposit constant

    Outputs:
        dict: Simulation results
    """
    # Setup environment
    env = AntColonyEnvironment(evaporation_rate=0.2)
    env.create_random_graph(num_nodes, connectivity=0.35)

    history = {
        'best_path_length': [],
        'avg_path_length': [],
        'best_path': None,
        'overall_best_length': float('inf')
    }

    print(f"Ant Colony Optimization: {num_nodes} nodes, {num_ants} ants/iteration")
    print(f"Nest: {env.nest}, Food: {env.food_nodes}")
    print("-" * 60)

    for iteration in range(num_iterations):
        # Create ants
        ants = [AntAgent(ant_id=i, nest_node=env.nest) for i in range(num_ants)]

        # Let ants explore (max steps to prevent infinite loops)
        max_steps = num_nodes * 3
        for step in range(max_steps):
            all_done = True
            for ant in ants:
                if not ant.completed:
                    ant.step(env.graph, env.pheromone, env.food_nodes)
                    all_done = False
            if all_done:
                break

        # Collect results from successful ants
        successful_ants = [a for a in ants if a.found_food and a.completed]

        if successful_ants:
            # Find best ant this iteration
            best_ant = min(successful_ants, key=lambda a: a.path_length)
            avg_length = sum(a.path_length for a in successful_ants) / len(successful_ants)

            history['best_path_length'].append(best_ant.path_length)
            history['avg_path_length'].append(avg_length)

            # Update global best
            if best_ant.path_length < history['overall_best_length']:
                history['overall_best_length'] = best_ant.path_length
                history['best_path'] = best_ant.path.copy()

            # Deposit pheromone (only successful ants)
            for ant in successful_ants:
                deposit_amount = q_constant / ant.path_length
                env.deposit_pheromone(ant.get_path_edges(), deposit_amount)
        else:
            history['best_path_length'].append(float('inf'))
            history['avg_path_length'].append(float('inf'))

        # Evaporate pheromone
        env.evaporate()

        # Progress output
        if iteration % 10 == 0 or iteration == num_iterations - 1:
            if successful_ants:
                print(f"Iter {iteration:3d}: success={len(successful_ants)}/{num_ants}, "
                      f"best={history['best_path_length'][-1]:.2f}, "
                      f"overall_best={history['overall_best_length']:.2f}")
            else:
                print(f"Iter {iteration:3d}: no successful ants")

    print("-" * 60)
    return {
        'environment': env,
        'history': history
    }


def analyze_results(results):
    """
    Analyze simulation results.

    Inputs:
        results (dict): Results from run_simulation
    """
    history = results['history']
    env = results['environment']

    print("\n=== Analysis ===")
    print(f"Best path found: {history['best_path']}")
    print(f"Best path length: {history['overall_best_length']:.2f}")

    # Improvement over time
    valid_lengths = [l for l in history['best_path_length'] if l < float('inf')]
    if len(valid_lengths) > 1:
        improvement = (valid_lengths[0] - valid_lengths[-1]) / valid_lengths[0] * 100
        print(f"Improvement from first to last: {improvement:.1f}%")

    # Compare with greedy pheromone path
    greedy_path, greedy_length = env.get_best_path(env.nest, list(env.food_nodes)[0])
    print(f"\nGreedy pheromone path: {greedy_path}")
    print(f"Greedy path length: {greedy_length:.2f}")


def main():
    """Main entry point."""
    results = run_simulation(
        num_nodes=12,
        num_ants=15,
        num_iterations=40,
        q_constant=50.0
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
