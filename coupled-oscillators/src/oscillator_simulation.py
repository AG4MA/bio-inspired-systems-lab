# oscillator_simulation.py
# Purpose: Simulate coupled oscillator synchronization
# Demonstrates firefly-inspired distributed timing coordination

import random
import math
from agent import Oscillator, calculate_order_parameter


def create_all_to_all_network(num_oscillators, coupling_strength=0.1, freq_spread=0.0):
    """
    Create fully connected oscillator network.

    Inputs:
        num_oscillators (int): Number of oscillators
        coupling_strength (float): Coupling between oscillators
        freq_spread (float): Random variation in natural frequency

    Outputs:
        list: List of connected oscillators
    """
    oscillators = []

    for i in range(num_oscillators):
        freq = 1.0 + random.uniform(-freq_spread, freq_spread)
        osc = Oscillator(osc_id=i, frequency=freq, coupling_strength=coupling_strength)
        oscillators.append(osc)

    # Connect all to all
    for osc in oscillators:
        osc.set_neighbors([o for o in oscillators if o.id != osc.id])

    return oscillators


def create_ring_network(num_oscillators, coupling_strength=0.1, freq_spread=0.0):
    """
    Create ring topology oscillator network.

    Inputs:
        num_oscillators (int): Number of oscillators
        coupling_strength (float): Coupling between oscillators
        freq_spread (float): Random variation in natural frequency

    Outputs:
        list: List of connected oscillators
    """
    oscillators = []

    for i in range(num_oscillators):
        freq = 1.0 + random.uniform(-freq_spread, freq_spread)
        osc = Oscillator(osc_id=i, frequency=freq, coupling_strength=coupling_strength)
        oscillators.append(osc)

    # Connect in ring
    for i, osc in enumerate(oscillators):
        left = oscillators[(i - 1) % num_oscillators]
        right = oscillators[(i + 1) % num_oscillators]
        osc.set_neighbors([left, right])

    return oscillators


def run_simulation(num_oscillators=20, num_steps=1000, dt=0.02,
                   coupling_strength=0.15, topology='all-to-all'):
    """
    Run coupled oscillator simulation.

    Inputs:
        num_oscillators (int): Number of oscillators
        num_steps (int): Simulation duration in steps
        dt (float): Time step size
        coupling_strength (float): Coupling strength
        topology (str): 'all-to-all' or 'ring'

    Outputs:
        dict: Simulation results
    """
    # Create network
    if topology == 'all-to-all':
        oscillators = create_all_to_all_network(
            num_oscillators, coupling_strength, freq_spread=0.05
        )
    else:
        oscillators = create_ring_network(
            num_oscillators, coupling_strength, freq_spread=0.05
        )

    history = {
        'order_parameter': [],
        'fire_events': []
    }

    print(f"Coupled Oscillators: {num_oscillators} units, {topology} topology")
    print(f"Coupling strength: {coupling_strength}")
    print("-" * 60)

    # Initial state
    initial_r = calculate_order_parameter(oscillators)
    print(f"Initial order parameter: {initial_r:.4f}")

    for step in range(num_steps):
        # Update all oscillators
        fired_this_step = []
        for osc in oscillators:
            if osc.step(dt):
                fired_this_step.append(osc.id)

        # Broadcast pulses from fired oscillators
        for osc in oscillators:
            if osc.just_fired:
                osc.broadcast_pulse()

        # Record metrics
        r = calculate_order_parameter(oscillators)
        history['order_parameter'].append(r)

        if fired_this_step:
            history['fire_events'].append({
                'step': step,
                'time': step * dt,
                'fired': fired_this_step
            })

        # Progress output
        if step % 200 == 0 or step == num_steps - 1:
            num_firing = len(fired_this_step)
            print(f"Step {step:4d}: r={r:.4f}, firing={num_firing}")

    print("-" * 60)
    return {
        'oscillators': oscillators,
        'history': history
    }


def analyze_results(results):
    """
    Analyze simulation results.

    Inputs:
        results (dict): Results from run_simulation
    """
    history = results['history']
    oscillators = results['oscillators']

    r_values = history['order_parameter']

    # Final synchronization state
    final_r = r_values[-1]
    max_r = max(r_values)
    avg_r_last_quarter = sum(r_values[-len(r_values)//4:]) / (len(r_values)//4)

    print("\n=== Analysis ===")
    print(f"Final order parameter: {final_r:.4f}")
    print(f"Maximum order parameter: {max_r:.4f}")
    print(f"Average r (last quarter): {avg_r_last_quarter:.4f}")

    # Synchronization assessment
    if avg_r_last_quarter > 0.9:
        print("Result: Strong synchronization achieved")
    elif avg_r_last_quarter > 0.6:
        print("Result: Partial synchronization")
    else:
        print("Result: Weak or no synchronization")

    # Fire pattern analysis
    fire_events = history['fire_events']
    if fire_events:
        # Check if oscillators are firing together
        last_events = fire_events[-20:] if len(fire_events) > 20 else fire_events
        avg_group_size = sum(len(e['fired']) for e in last_events) / len(last_events)
        print(f"Average simultaneous firings (recent): {avg_group_size:.1f}")


def main():
    """Main entry point."""
    print("=== All-to-All Topology ===")
    results_all = run_simulation(
        num_oscillators=15,
        num_steps=800,
        dt=0.02,
        coupling_strength=0.12,
        topology='all-to-all'
    )
    analyze_results(results_all)

    print("\n" + "=" * 60)
    print("=== Ring Topology ===")
    results_ring = run_simulation(
        num_oscillators=15,
        num_steps=800,
        dt=0.02,
        coupling_strength=0.12,
        topology='ring'
    )
    analyze_results(results_ring)


if __name__ == "__main__":
    main()
