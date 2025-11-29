# chemotaxis_simulation.py
# Purpose: Main simulation demonstrating bacterial chemotaxis behavior
# Shows how agents converge toward attractant sources using run-and-tumble

import random
import math
from agent import ChemotaxisAgent
from environment import GradientEnvironment


def create_agents(num_agents, env_size):
    """
    Create agents with random initial positions.

    Inputs:
        num_agents (int): Number of agents
        env_size (float): Environment dimension

    Outputs:
        list: List of ChemotaxisAgent instances
    """
    agents = []
    for i in range(num_agents):
        x = random.uniform(0, env_size)
        y = random.uniform(0, env_size)
        agent = ChemotaxisAgent(agent_id=i, x=x, y=y)
        agents.append(agent)
    return agents


def calculate_distance_to_source(agent, source_pos):
    """
    Calculate distance from agent to source.

    Inputs:
        agent: ChemotaxisAgent instance
        source_pos (tuple): (x, y) of source

    Outputs:
        float: Euclidean distance
    """
    dx = agent.x - source_pos[0]
    dy = agent.y - source_pos[1]
    return math.sqrt(dx * dx + dy * dy)


def run_simulation(num_agents=30, num_steps=200, env_size=20.0):
    """
    Run chemotaxis simulation.

    Inputs:
        num_agents (int): Population size
        num_steps (int): Simulation duration
        env_size (float): Environment dimension

    Outputs:
        dict: Simulation results
    """
    # Setup environment with a single attractant source
    env = GradientEnvironment(width=env_size, height=env_size, noise_level=0.1)
    source_x, source_y = env_size * 0.75, env_size * 0.75
    env.add_source(source_x, source_y, strength=15.0)

    # Create agents
    agents = create_agents(num_agents, env_size)

    # Initialize agents with first concentration reading
    for agent in agents:
        c = env.get_concentration(agent.x, agent.y)
        agent.sense(c)

    # Track history
    history = {
        'mean_distance': [],
        'min_distance': [],
        'mean_concentration': []
    }

    source_pos = (source_x, source_y)
    print(f"Chemotaxis Simulation: {num_agents} agents, source at ({source_x:.1f}, {source_y:.1f})")
    print("-" * 50)

    for step in range(num_steps):
        # Update all agents
        for agent in agents:
            concentration = env.get_concentration(agent.x, agent.y)
            agent.update(concentration, bounds=(0, env_size))

        # Calculate metrics
        distances = [calculate_distance_to_source(a, source_pos) for a in agents]
        concentrations = [env.get_concentration(a.x, a.y) for a in agents]

        mean_dist = sum(distances) / len(distances)
        min_dist = min(distances)
        mean_conc = sum(concentrations) / len(concentrations)

        history['mean_distance'].append(mean_dist)
        history['min_distance'].append(min_dist)
        history['mean_concentration'].append(mean_conc)

        # Progress output
        if step % 25 == 0 or step == num_steps - 1:
            print(f"Step {step:3d}: mean_dist={mean_dist:.2f}, min_dist={min_dist:.2f}, mean_conc={mean_conc:.2f}")

    print("-" * 50)
    return {
        'agents': agents,
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
    agents = results['agents']

    initial_distance = history['mean_distance'][0]
    final_distance = history['mean_distance'][-1]
    improvement = (initial_distance - final_distance) / initial_distance * 100

    total_tumbles = sum(a.tumble_count for a in agents)
    avg_tumbles = total_tumbles / len(agents)

    print("\n=== Analysis ===")
    print(f"Initial mean distance: {initial_distance:.2f}")
    print(f"Final mean distance: {final_distance:.2f}")
    print(f"Improvement: {improvement:.1f}%")
    print(f"Average tumbles per agent: {avg_tumbles:.1f}")


def main():
    """Main entry point."""
    results = run_simulation(
        num_agents=40,
        num_steps=150,
        env_size=20.0
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
