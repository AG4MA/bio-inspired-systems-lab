# agent.py
# Purpose: Coupled oscillator (firefly) for distributed synchronization
# Implements pulse-coupled phase dynamics

import math
import random


class Oscillator:
    """
    Phase oscillator that synchronizes through pulse coupling.
    Inspired by firefly synchronization behavior.
    """

    def __init__(self, osc_id, frequency=1.0, coupling_strength=0.1):
        """
        Initialize an oscillator.

        Inputs:
            osc_id (int): Unique identifier
            frequency (float): Natural oscillation frequency
            coupling_strength (float): How strongly pulses affect phase
        """
        self.id = osc_id
        self.frequency = frequency
        self.coupling_strength = coupling_strength

        # Phase in [0, 1), represents position in cycle
        self.phase = random.random()

        # Neighbors for pulse coupling
        self.neighbors = []

        # Firing state
        self.just_fired = False
        self.fire_count = 0

    def set_neighbors(self, neighbors):
        """
        Set oscillator's neighbors.

        Inputs:
            neighbors (list): List of neighboring oscillators
        """
        self.neighbors = neighbors

    def phase_response(self, current_phase):
        """
        Calculate phase adjustment when receiving pulse.
        Uses sine curve: positive adjustment near end of cycle (speeds up).

        Inputs:
            current_phase (float): Current phase value

        Outputs:
            float: Phase adjustment
        """
        # Kuramoto-style phase response
        return self.coupling_strength * math.sin(2 * math.pi * current_phase)

    def receive_pulse(self):
        """
        Respond to pulse from a neighbor.
        Adjusts phase based on phase response curve.
        """
        adjustment = self.phase_response(self.phase)
        self.phase += adjustment

        # Keep phase in valid range
        self.phase = self.phase % 1.0

    def step(self, dt=0.01):
        """
        Advance oscillator by one timestep.

        Inputs:
            dt (float): Time step size

        Outputs:
            bool: True if oscillator fired this step
        """
        # Advance phase
        self.phase += self.frequency * dt

        # Check for firing
        self.just_fired = False
        if self.phase >= 1.0:
            self.phase = self.phase % 1.0
            self.just_fired = True
            self.fire_count += 1

        return self.just_fired

    def broadcast_pulse(self):
        """
        Send pulse to all neighbors.
        Called after firing.
        """
        for neighbor in self.neighbors:
            neighbor.receive_pulse()

    def get_phase_radians(self):
        """Get phase in radians for order parameter calculation."""
        return 2 * math.pi * self.phase

    def __repr__(self):
        return f"Oscillator({self.id}, phase={self.phase:.3f}, freq={self.frequency:.3f})"


def calculate_order_parameter(oscillators):
    """
    Calculate Kuramoto order parameter (sync measure).

    Inputs:
        oscillators (list): List of oscillators

    Outputs:
        float: Order parameter r in [0, 1], 1 = perfect sync
    """
    if not oscillators:
        return 0.0

    n = len(oscillators)

    # Sum of unit vectors at each phase
    sum_cos = sum(math.cos(osc.get_phase_radians()) for osc in oscillators)
    sum_sin = sum(math.sin(osc.get_phase_radians()) for osc in oscillators)

    # Magnitude of average vector
    r = math.sqrt(sum_cos**2 + sum_sin**2) / n

    return r
