# flocking_simulation.py
# Purpose: Main simulation for Reynolds flocking behavior
# Demonstrates emergent swarm coordination from local rules

import random
import math
from agent import FlockingAgent


def create_flock(num_agents, env_size, initial_speed=1.0):
    """
    Create a flock of agents with random positions and velocities.

    Inputs:
        num_agents (int): Number of agents
        env_size (float): Environment dimension
        initial_speed (float): Initial velocity magnitude

    Outputs:
        list: List of FlockingAgent instances
    """
    agents = []
    for i in range(num_agents):
        # Random position
        x = random.uniform(0, env_size)
        y = random.uniform(0, env_size)

        # Random initial velocity
        angle = random.uniform(0, 2 * math.pi)
        vx = initial_speed * math.cos(angle)
        vy = initial_speed * math.sin(angle)

        agent = FlockingAgent(agent_id=i, x=x, y=y, vx=vx, vy=vy)
        agents.append(agent)

    return agents


def calculate_metrics(agents):
    """
    Calculate flock metrics for analysis.

    Inputs:
        agents (list): List of agents

    Outputs:
        dict: Metrics including polarization, spread, avg_neighbors
    """
    n = len(agents)
    if n == 0:
        return {'polarization': 0, 'spread': 0, 'avg_neighbors': 0}

    # Polarization: how aligned are velocities (0-1, 1 = all same direction)
    total_vx = sum(a.vx for a in agents)
    total_vy = sum(a.vy for a in agents)
    avg_speed = sum(math.sqrt(a.vx**2 + a.vy**2) for a in agents) / n
    if avg_speed > 0:
        polarization = math.sqrt(total_vx**2 + total_vy**2) / (n * avg_speed)
    else:
        polarization = 0

    # Spread: average distance from center of mass
    center_x = sum(a.x for a in agents) / n
    center_y = sum(a.y for a in agents) / n
    spread = sum(math.sqrt((a.x - center_x)**2 + (a.y - center_y)**2) for a in agents) / n

    # Average neighbor count
    total_neighbors = 0
    for agent in agents:
        neighbors = agent.get_neighbors(agents)
        total_neighbors += len(neighbors)
    avg_neighbors = total_neighbors / n

    return {
        'polarization': polarization,
        'spread': spread,
        'avg_neighbors': avg_neighbors
    }


def run_simulation(num_agents=50, num_steps=200, env_size=50.0):
    """
    Run flocking simulation.

    Inputs:
        num_agents (int): Flock size
        num_steps (int): Simulation duration
        env_size (float): Environment dimension

    Outputs:
        dict: Simulation results
    """
    agents = create_flock(num_agents, env_size)
    bounds = (0, env_size)

    history = {
        'polarization': [],
        'spread': [],
        'avg_neighbors': []
    }

    print(f"Flocking Simulation: {num_agents} agents")
    print("-" * 50)

    for step in range(num_steps):
        # Update all agents
        for agent in agents:
            agent.update(agents, bounds)

        # Calculate metrics
        metrics = calculate_metrics(agents)
        history['polarization'].append(metrics['polarization'])
        history['spread'].append(metrics['spread'])
        history['avg_neighbors'].append(metrics['avg_neighbors'])

        # Progress output
        if step % 25 == 0 or step == num_steps - 1:
            print(f"Step {step:3d}: polarization={metrics['polarization']:.3f}, "
                  f"spread={metrics['spread']:.2f}, neighbors={metrics['avg_neighbors']:.1f}")

    print("-" * 50)
    return {
        'agents': agents,
        'history': history
    }


def analyze_results(results):
    """
    Analyze simulation results.

    Inputs:
        results (dict): Results from run_simulation
    """
    history = results['history']

    # Compare initial vs final metrics
    initial_pol = history['polarization'][0]
    final_pol = history['polarization'][-1]
    avg_pol = sum(history['polarization']) / len(history['polarization'])

    initial_spread = history['spread'][0]
    final_spread = history['spread'][-1]

    print("\n=== Analysis ===")
    print(f"Initial polarization: {initial_pol:.3f}")
    print(f"Final polarization: {final_pol:.3f}")
    print(f"Average polarization: {avg_pol:.3f}")
    print(f"Initial spread: {initial_spread:.2f}")
    print(f"Final spread: {final_spread:.2f}")

    if final_pol > 0.7:
        print("Result: Flock achieved high alignment (coherent motion)")
    elif final_pol > 0.4:
        print("Result: Flock achieved moderate alignment")
    else:
        print("Result: Flock remained dispersed")


def main():
    """Main entry point."""
    results = run_simulation(
        num_agents=60,
        num_steps=150,
        env_size=40.0
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
