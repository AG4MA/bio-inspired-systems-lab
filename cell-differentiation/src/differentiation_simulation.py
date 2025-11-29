# differentiation_simulation.py
# Purpose: Simulate cell differentiation with role emergence
# Demonstrates dynamic role assignment from homogeneous agents

import random
from agent import DifferentiatingAgent
from environment import DifferentiationEnvironment


def create_agents(num_agents, env_size):
    """
    Create undifferentiated agents at random positions.

    Inputs:
        num_agents (int): Number of agents
        env_size (float): Environment dimension

    Outputs:
        list: List of DifferentiatingAgent instances
    """
    agents = []
    for i in range(num_agents):
        x = random.uniform(1, env_size - 1)
        y = random.uniform(1, env_size - 1)
        agents.append(DifferentiatingAgent(agent_id=i, x=x, y=y))
    return agents


def count_roles(agents):
    """
    Count agents in each role.

    Inputs:
        agents (list): All agents

    Outputs:
        dict: Role -> count
    """
    counts = {role: 0 for role in DifferentiatingAgent.ALL_ROLES}
    for agent in agents:
        counts[agent.role] = counts.get(agent.role, 0) + 1
    return counts


def run_simulation(num_agents=30, num_steps=100, env_size=20.0):
    """
    Run differentiation simulation.

    Inputs:
        num_agents (int): Population size
        num_steps (int): Simulation duration
        env_size (float): Environment dimension

    Outputs:
        dict: Simulation results
    """
    # Setup
    env = DifferentiationEnvironment(width=env_size, height=env_size)
    env.setup_default_signals()
    agents = create_agents(num_agents, env_size)

    history = {
        'role_counts': [],
        'differentiation_events': []
    }

    print(f"Differentiation Simulation: {num_agents} agents")
    print("-" * 60)

    for step in range(num_steps):
        previous_roles = {a.id: a.role for a in agents}

        # Update all agents
        for agent in agents:
            agent.update(agents, env)

        # Track differentiation events
        for agent in agents:
            if agent.role != previous_roles[agent.id]:
                history['differentiation_events'].append({
                    'step': step,
                    'agent_id': agent.id,
                    'from': previous_roles[agent.id],
                    'to': agent.role
                })

        # Record role distribution
        role_counts = count_roles(agents)
        history['role_counts'].append(role_counts)

        # Progress output
        if step % 20 == 0 or step == num_steps - 1:
            counts_str = ', '.join(f"{r}={c}" for r, c in role_counts.items() if c > 0)
            print(f"Step {step:3d}: {counts_str}")

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
    agents = results['agents']

    # Final distribution
    final_counts = count_roles(agents)
    total_differentiated = sum(c for r, c in final_counts.items() if r != DifferentiatingAgent.STEM)

    # Differentiation statistics
    events = history['differentiation_events']
    unique_differentiators = len(set(e['agent_id'] for e in events))

    print("\n=== Analysis ===")
    print(f"Final role distribution:")
    for role, count in final_counts.items():
        pct = 100 * count / len(agents)
        print(f"  {role:10s}: {count:2d} ({pct:.1f}%)")

    print(f"\nTotal differentiation events: {len(events)}")
    print(f"Agents that differentiated: {unique_differentiators}/{len(agents)}")

    # Check for expected roles
    if final_counts.get(DifferentiatingAgent.LEADER, 0) >= 1:
        print("Leadership emerged")
    if final_counts.get(DifferentiatingAgent.WORKER, 0) >= 3:
        print("Worker pool formed")
    if final_counts.get(DifferentiatingAgent.STEM, 0) >= 2:
        print("Stem cell reserve maintained")


def main():
    """Main entry point."""
    results = run_simulation(
        num_agents=25,
        num_steps=80,
        env_size=15.0
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
