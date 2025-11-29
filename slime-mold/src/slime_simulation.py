# slime_simulation.py
# Purpose: Simulate slime mold pathfinding behavior
# Demonstrates emergent optimal paths between food sources

import random
from agent import SlimeAgent
from environment import PheromoneEnvironment


def create_scenario(env):
    """
    Set up a typical pathfinding scenario.

    Inputs:
        env (PheromoneEnvironment): Environment to configure
    """
    # Add food sources at different locations
    env.add_food(env.width * 0.1, env.height * 0.5)  # Left
    env.add_food(env.width * 0.9, env.height * 0.5)  # Right
    env.add_food(env.width * 0.5, env.height * 0.9)  # Top

    # Add some obstacles
    env.add_obstacle(env.width * 0.5, env.height * 0.3, radius=2.0)
    env.add_obstacle(env.width * 0.3, env.height * 0.6, radius=1.5)
    env.add_obstacle(env.width * 0.7, env.height * 0.7, radius=1.5)


def spawn_agents(origin, num_agents, env):
    """
    Spawn agents from an origin point.

    Inputs:
        origin (tuple): (x, y) spawn point
        num_agents (int): Number of agents
        env (PheromoneEnvironment): Environment

    Outputs:
        list: List of SlimeAgent instances
    """
    agents = []
    for i in range(num_agents):
        # Slight randomization of spawn position
        x = origin[0] + random.uniform(-0.5, 0.5)
        y = origin[1] + random.uniform(-0.5, 0.5)
        agent = SlimeAgent(agent_id=i, x=x, y=y, origin=origin)
        agents.append(agent)
    return agents


def run_simulation(num_agents=50, num_steps=300, env_size=20.0):
    """
    Run slime mold pathfinding simulation.

    Inputs:
        num_agents (int): Number of explorer agents
        num_steps (int): Simulation duration
        env_size (float): Environment dimension

    Outputs:
        dict: Simulation results
    """
    # Setup
    env = PheromoneEnvironment(width=env_size, height=env_size, resolution=40)
    create_scenario(env)

    # Spawn agents from center
    origin = (env_size * 0.5, env_size * 0.1)
    agents = spawn_agents(origin, num_agents, env)

    history = {
        'alive_count': [],
        'food_found': [],
        'total_pheromone': [],
        'completed_paths': 0
    }

    print(f"Slime Mold Simulation: {num_agents} agents, {len(env.food_sources)} food sources")
    print("-" * 60)

    for step in range(num_steps):
        # Update all agents
        for agent in agents:
            result = agent.update(env)
            if result == 'completed':
                history['completed_paths'] += 1
            elif result == 'found_food':
                history['food_found'].append({'step': step, 'agent_id': agent.id})

        # Update environment
        env.update()

        # Spawn replacement agents periodically
        if step % 20 == 0 and step < num_steps * 0.7:
            new_agents = spawn_agents(origin, num_agents // 5, env)
            for i, a in enumerate(new_agents):
                a.id = len(agents) + i
            agents.extend(new_agents)

        # Record metrics
        alive = sum(1 for a in agents if a.is_alive())
        history['alive_count'].append(alive)
        history['total_pheromone'].append(env.get_total_pheromone())

        # Progress output
        if step % 50 == 0 or step == num_steps - 1:
            print(f"Step {step:3d}: alive={alive:3d}, completed={history['completed_paths']}, "
                  f"pheromone={env.get_total_pheromone():.1f}")

    print("-" * 60)
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
    env = results['environment']

    print("\n=== Analysis ===")
    print(f"Paths completed: {history['completed_paths']}")
    print(f"Food discoveries: {len(history['food_found'])}")
    print(f"Final pheromone: {history['total_pheromone'][-1]:.1f}")

    # Check path formation between food sources
    food = env.food_sources
    if len(food) >= 2:
        print("\nPath strengths between food sources:")
        for i in range(len(food)):
            for j in range(i + 1, len(food)):
                strength = env.get_path_strength(food[i], food[j])
                print(f"  Food {i} <-> Food {j}: {strength:.2f}")

    if history['completed_paths'] > 0:
        print("\nResult: Network paths successfully established")
    else:
        print("\nResult: No complete paths formed (may need more agents or steps)")


def main():
    """Main entry point."""
    results = run_simulation(
        num_agents=40,
        num_steps=250,
        env_size=15.0
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
