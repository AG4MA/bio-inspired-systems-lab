# symmetry_simulation.py
# Purpose: Simulate symmetry breaking for leader election
# Shows how identical agents spontaneously differentiate

import random
from agent import SymmetryBreakingAgent


def create_ring_network(num_agents):
    """
    Create agents connected in a ring topology.

    Inputs:
        num_agents (int): Number of agents

    Outputs:
        list: List of connected agents
    """
    agents = [SymmetryBreakingAgent(agent_id=i) for i in range(num_agents)]

    # Connect in ring (each agent connected to neighbors)
    for i, agent in enumerate(agents):
        left = agents[(i - 1) % num_agents]
        right = agents[(i + 1) % num_agents]
        agent.set_neighbors([left, right])

    return agents


def create_full_network(num_agents):
    """
    Create fully connected network.

    Inputs:
        num_agents (int): Number of agents

    Outputs:
        list: List of connected agents
    """
    agents = [SymmetryBreakingAgent(agent_id=i) for i in range(num_agents)]

    # Fully connected (each agent sees all others)
    for agent in agents:
        agent.set_neighbors([a for a in agents if a.id != agent.id])

    return agents


def count_roles(agents):
    """
    Count agents in each role.

    Inputs:
        agents (list): All agents

    Outputs:
        dict: Role counts
    """
    counts = {
        SymmetryBreakingAgent.UNDECIDED: 0,
        SymmetryBreakingAgent.LEADER: 0,
        SymmetryBreakingAgent.FOLLOWER: 0
    }
    for agent in agents:
        counts[agent.role] += 1
    return counts


def run_simulation(num_agents=10, num_steps=200, topology='ring'):
    """
    Run symmetry breaking simulation.

    Inputs:
        num_agents (int): Number of agents
        num_steps (int): Maximum steps
        topology (str): 'ring' or 'full'

    Outputs:
        dict: Simulation results
    """
    # Create network
    if topology == 'ring':
        agents = create_ring_network(num_agents)
    else:
        agents = create_full_network(num_agents)

    history = {
        'commitment_std': [],
        'decided_count': [],
        'leaders': [],
        'steps_to_break': None
    }

    print(f"Symmetry Breaking Simulation: {num_agents} agents, {topology} topology")
    print("-" * 60)

    # Print initial state
    commitments = [a.commitment for a in agents]
    print(f"Initial commitments: mean={sum(commitments)/len(commitments):.4f}, "
          f"std={compute_std(commitments):.4f}")

    for step in range(num_steps):
        # Update all agents (in random order to avoid bias)
        order = list(range(num_agents))
        random.shuffle(order)
        for i in order:
            agents[i].update()

        # Calculate metrics
        commitments = [a.commitment for a in agents]
        std = compute_std(commitments)
        decided = sum(1 for a in agents if a.is_decided())

        history['commitment_std'].append(std)
        history['decided_count'].append(decided)

        # Check if symmetry is broken (all decided)
        if decided == num_agents and history['steps_to_break'] is None:
            history['steps_to_break'] = step
            counts = count_roles(agents)
            history['leaders'] = [a.id for a in agents if a.role == SymmetryBreakingAgent.LEADER]
            print(f"Step {step}: Symmetry broken! {counts[SymmetryBreakingAgent.LEADER]} leader(s)")
            break

        # Progress output
        if step % 25 == 0:
            print(f"Step {step:3d}: std={std:.4f}, decided={decided}/{num_agents}")

    print("-" * 60)

    # Final state
    print("\nFinal agent states:")
    for agent in agents:
        print(f"  {agent}")

    return {
        'agents': agents,
        'history': history
    }


def compute_std(values):
    """Compute standard deviation."""
    mean = sum(values) / len(values)
    variance = sum((v - mean)**2 for v in values) / len(values)
    return variance ** 0.5


def analyze_results(results):
    """
    Analyze simulation results.

    Inputs:
        results (dict): Results from run_simulation
    """
    history = results['history']
    agents = results['agents']

    counts = count_roles(agents)

    print("\n=== Analysis ===")
    print(f"Final roles: {counts}")

    if history['steps_to_break']:
        print(f"Symmetry broke at step: {history['steps_to_break']}")
        print(f"Leaders: agents {history['leaders']}")
    else:
        print("Symmetry did not fully break within time limit")

    # Check commitment distribution
    commitments = [a.commitment for a in agents]
    print(f"Final commitment range: [{min(commitments):.3f}, {max(commitments):.3f}]")


def main():
    """Main entry point."""
    print("=== Ring Topology ===")
    results_ring = run_simulation(
        num_agents=8,
        num_steps=150,
        topology='ring'
    )
    analyze_results(results_ring)

    print("\n" + "=" * 60)
    print("=== Full Topology ===")
    results_full = run_simulation(
        num_agents=8,
        num_steps=150,
        topology='full'
    )
    analyze_results(results_full)


if __name__ == "__main__":
    main()
