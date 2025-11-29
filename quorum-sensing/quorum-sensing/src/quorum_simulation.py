# quorum_simulation.py
# Purpose: Main simulation loop for quorum sensing behavior
# Demonstrates emergent collective activation based on population density

import random
from agent import Agent
from environment import Environment


def create_agents(num_agents, env_size, threshold):
    """
    Create a population of agents with random positions.

    Inputs:
        num_agents (int): Number of agents to create
        env_size (float): Size of the environment
        threshold (float): Activation threshold for all agents

    Outputs:
        list: List of Agent instances
    """
    agents = []
    for i in range(num_agents):
        x = random.uniform(0, env_size)
        y = random.uniform(0, env_size)
        agent = Agent(agent_id=i, x=x, y=y, threshold=threshold)
        agents.append(agent)
    return agents


def run_simulation(num_agents=50, num_steps=100, env_size=10.0, threshold=1.0):
    """
    Run the quorum sensing simulation.

    Inputs:
        num_agents (int): Population size
        num_steps (int): Number of simulation steps
        env_size (float): Environment dimension
        threshold (float): Activation threshold

    Outputs:
        dict: Simulation results with history
    """
    # Initialize environment and agents
    env = Environment(width=env_size, height=env_size)
    agents = create_agents(num_agents, env_size, threshold)

    # Track simulation history
    history = {
        'active_count': [],
        'total_signal': [],
        'max_concentration': []
    }

    print(f"Starting simulation: {num_agents} agents, threshold={threshold}")
    print("-" * 50)

    for step in range(num_steps):
        # Phase 1: Agents produce signals
        for agent in agents:
            signal = agent.produce_signal()
            env.add_signal(agent.x, agent.y, signal)

        # Phase 2: Environment dynamics (diffusion + decay)
        env.update()

        # Phase 3: Agents sense and update state
        state_changes = 0
        for agent in agents:
            concentration = env.get_concentration(agent.x, agent.y)
            agent.sense(concentration)
            if agent.update_state():
                state_changes += 1

        # Phase 4: Agents move (optional random walk)
        for agent in agents:
            agent.move_random(step_size=0.2, bounds=(0, env_size))

        # Record metrics
        active_count = sum(1 for a in agents if a.is_active())
        history['active_count'].append(active_count)
        history['total_signal'].append(env.get_total_signal())
        history['max_concentration'].append(env.get_max_concentration())

        # Print progress every 10 steps
        if step % 10 == 0 or step == num_steps - 1:
            pct_active = 100 * active_count / num_agents
            print(f"Step {step:3d}: {active_count:3d}/{num_agents} active ({pct_active:.1f}%)")

    print("-" * 50)
    print("Simulation complete.")

    return {
        'agents': agents,
        'environment': env,
        'history': history
    }


def analyze_results(results):
    """
    Analyze and display simulation results.

    Inputs:
        results (dict): Results from run_simulation
    """
    history = results['history']
    active = history['active_count']

    # Detect quorum activation
    final_active = active[-1]
    max_active = max(active)
    activation_step = next((i for i, a in enumerate(active) if a > len(results['agents']) * 0.5), None)

    print("\n=== Analysis ===")
    print(f"Final active agents: {final_active}")
    print(f"Peak active agents: {max_active}")
    if activation_step:
        print(f"Quorum reached at step: {activation_step}")
    else:
        print("Quorum threshold (50%) never reached")


def main():
    """Main entry point for quorum sensing simulation."""
    # Run with default parameters
    results = run_simulation(
        num_agents=80,
        num_steps=100,
        env_size=10.0,
        threshold=0.8
    )
    analyze_results(results)


if __name__ == "__main__":
    main()