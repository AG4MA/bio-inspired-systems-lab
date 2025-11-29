# apoptosis_simulation.py
# Purpose: Simulate self-healing system with apoptosis mechanism
# Demonstrates how faulty agents self-eliminate to maintain system health

import random
from agent import ApoptosisAgent


def create_agents(num_agents):
    """
    Create a population of agents.

    Inputs:
        num_agents (int): Number of agents

    Outputs:
        list: List of ApoptosisAgent instances
    """
    return [ApoptosisAgent(agent_id=i) for i in range(num_agents)]


def introduce_fault(agent, severity='moderate'):
    """
    Introduce a fault into an agent.

    Inputs:
        agent (ApoptosisAgent): Agent to corrupt
        severity (str): 'mild', 'moderate', or 'severe'
    """
    if severity == 'mild':
        agent.error_rate = 0.3
        agent.anomaly_score = 0.2
    elif severity == 'moderate':
        agent.error_rate = 0.5
        agent.anomaly_score = 0.4
    elif severity == 'severe':
        agent.error_rate = 0.8
        agent.anomaly_score = 0.7


def run_simulation(num_agents=20, num_steps=100, fault_rate=0.05):
    """
    Run apoptosis simulation.

    Inputs:
        num_agents (int): Initial population
        num_steps (int): Simulation duration
        fault_rate (float): Probability of introducing fault per step

    Outputs:
        dict: Simulation results
    """
    agents = create_agents(num_agents)

    history = {
        'alive_count': [],
        'avg_health': [],
        'deaths': [],
        'faults_introduced': 0
    }

    print(f"Apoptosis Simulation: {num_agents} agents, fault_rate={fault_rate}")
    print("-" * 60)

    for step in range(num_steps):
        alive_agents = [a for a in agents if a.is_alive()]

        # Random fault injection
        for agent in alive_agents:
            if random.random() < fault_rate:
                severity = random.choice(['mild', 'moderate', 'severe'])
                introduce_fault(agent, severity)
                history['faults_introduced'] += 1

        # Agents operate and update health
        for agent in alive_agents:
            # Agents with faults have higher failure probability
            fail_prob = 0.1 + agent.anomaly_score * 0.5
            agent.simulate_operation(failure_probability=fail_prob)

        # Neighbor observation and marking
        for i, agent in enumerate(alive_agents):
            # Each agent observes a few random neighbors
            neighbors = random.sample(
                [a for a in alive_agents if a.id != agent.id],
                min(3, len(alive_agents) - 1)
            ) if len(alive_agents) > 1 else []

            for neighbor in neighbors:
                agent.observe_neighbor(neighbor)

        # Check for apoptosis
        deaths_this_step = []
        for agent in alive_agents:
            agent.decay_marks()
            if agent.check_apoptosis():
                agent.complete_death()
                deaths_this_step.append({
                    'step': step,
                    'agent_id': agent.id,
                    'reason': agent.death_reason,
                    'health': agent.health
                })

        history['deaths'].extend(deaths_this_step)

        # Spawn replacements (optional: maintain population)
        while len([a for a in agents if a.is_alive()]) < num_agents * 0.8:
            new_id = max(a.id for a in agents) + 1
            agents.append(ApoptosisAgent(agent_id=new_id))

        # Record metrics
        alive_agents = [a for a in agents if a.is_alive()]
        history['alive_count'].append(len(alive_agents))
        avg_health = sum(a.health for a in alive_agents) / len(alive_agents) if alive_agents else 0
        history['avg_health'].append(avg_health)

        # Progress output
        if step % 20 == 0 or step == num_steps - 1:
            deaths_count = len([d for d in history['deaths'] if d['step'] <= step])
            print(f"Step {step:3d}: alive={len(alive_agents):2d}, "
                  f"avg_health={avg_health:.2f}, total_deaths={deaths_count}")

    print("-" * 60)
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
    deaths = history['deaths']

    print("\n=== Analysis ===")
    print(f"Total faults introduced: {history['faults_introduced']}")
    print(f"Total deaths: {len(deaths)}")

    # Categorize death reasons
    self_deaths = len([d for d in deaths if 'self' in d['reason']])
    peer_deaths = len([d for d in deaths if 'neighbor' in d['reason']])

    print(f"  - Self-triggered: {self_deaths}")
    print(f"  - Peer consensus: {peer_deaths}")

    # Health trends
    initial_health = history['avg_health'][0]
    final_health = history['avg_health'][-1]
    print(f"Initial avg health: {initial_health:.2f}")
    print(f"Final avg health: {final_health:.2f}")

    if final_health > 0.7:
        print("Result: System maintained high health through apoptosis")
    else:
        print("Result: System health degraded despite apoptosis")


def main():
    """Main entry point."""
    results = run_simulation(
        num_agents=25,
        num_steps=100,
        fault_rate=0.08
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
