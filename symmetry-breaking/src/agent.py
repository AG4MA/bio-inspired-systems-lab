# agent.py
# Purpose: Agent for symmetry breaking / leaderless leader election
# Implements positive feedback amplification of small differences

import random


class SymmetryBreakingAgent:
    """
    Agent that participates in distributed symmetry breaking.
    Identical agents spontaneously differentiate into leaders/followers.
    """

    # Roles
    UNDECIDED = 'undecided'
    LEADER = 'leader'
    FOLLOWER = 'follower'

    def __init__(self, agent_id, initial_noise=0.01):
        """
        Initialize agent with nearly symmetric state.

        Inputs:
            agent_id (int): Unique identifier
            initial_noise (float): Small random initial difference
        """
        self.id = agent_id

        # Commitment level (0 = follower tendency, 1 = leader tendency)
        self.commitment = 0.5 + random.uniform(-initial_noise, initial_noise)

        self.role = SymmetryBreakingAgent.UNDECIDED
        self.neighbors = []

        # Parameters
        self.amplification_rate = 0.1
        self.noise_amplitude = 0.02
        self.decision_threshold = 0.15  # Distance from 0 or 1 to decide

    def set_neighbors(self, neighbors):
        """
        Set this agent's neighbors.

        Inputs:
            neighbors (list): List of neighbor agents
        """
        self.neighbors = neighbors

    def get_neighbor_average(self):
        """
        Calculate average commitment of neighbors.

        Outputs:
            float: Average neighbor commitment
        """
        if not self.neighbors:
            return 0.5

        return sum(n.commitment for n in self.neighbors) / len(self.neighbors)

    def update(self):
        """
        Perform one symmetry breaking step.
        Amplifies difference from neighbors.

        Outputs:
            str: Current role
        """
        # Already decided, no update needed
        if self.role != SymmetryBreakingAgent.UNDECIDED:
            return self.role

        # Compare to neighbors
        neighbor_avg = self.get_neighbor_average()

        # Positive feedback: amplify difference from neighbors
        difference = self.commitment - neighbor_avg
        delta = difference * self.amplification_rate

        # Add noise to break perfect symmetry
        delta += random.gauss(0, self.noise_amplitude)

        # Update commitment
        self.commitment += delta

        # Clamp to valid range
        self.commitment = max(0.0, min(1.0, self.commitment))

        # Check for decision
        if self.commitment > (1.0 - self.decision_threshold):
            self.role = SymmetryBreakingAgent.LEADER
        elif self.commitment < self.decision_threshold:
            self.role = SymmetryBreakingAgent.FOLLOWER

        return self.role

    def is_decided(self):
        """Check if agent has broken symmetry."""
        return self.role != SymmetryBreakingAgent.UNDECIDED

    def __repr__(self):
        return f"Agent({self.id}, c={self.commitment:.3f}, role={self.role})"
