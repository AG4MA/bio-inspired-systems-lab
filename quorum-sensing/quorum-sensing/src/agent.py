# agent.py
# Purpose: Defines the Agent class for quorum sensing simulation
# Each agent produces signals, senses local concentration, and activates when threshold is reached

import random


class Agent:
    """
    Represents a bacterium-like agent in quorum sensing simulation.
    Agents produce autoinducers and respond to local signal concentration.
    """

    # Agent states
    INACTIVE = 0
    ACTIVE = 1

    def __init__(self, agent_id, x, y, threshold=0.5, production_rate=0.1):
        """
        Initialize an agent with position and sensing parameters.

        Inputs:
            agent_id (int): Unique identifier
            x, y (float): Position in 2D space
            threshold (float): Activation threshold for signal concentration
            production_rate (float): Base rate of signal molecule production
        """
        self.id = agent_id
        self.x = x
        self.y = y
        self.threshold = threshold
        self.production_rate = production_rate
        self.state = Agent.INACTIVE
        self.sensed_concentration = 0.0

    def produce_signal(self):
        """
        Produce signaling molecules based on current state.
        
        Outputs:
            float: Amount of signal produced this step
        """
        # Active agents produce more signal (positive feedback)
        if self.state == Agent.ACTIVE:
            return self.production_rate * 2.0
        return self.production_rate

    def sense(self, local_concentration):
        """
        Sense the local concentration of signaling molecules.

        Inputs:
            local_concentration (float): Signal concentration at agent's position
        """
        self.sensed_concentration = local_concentration

    def update_state(self):
        """
        Update agent state based on sensed concentration.
        Implements threshold-based activation logic.

        Outputs:
            bool: True if state changed, False otherwise
        """
        previous_state = self.state

        # Activation logic: switch state based on threshold
        if self.sensed_concentration >= self.threshold:
            self.state = Agent.ACTIVE
        else:
            # Hysteresis: active agents have lower deactivation threshold
            deactivation_threshold = self.threshold * 0.7
            if self.sensed_concentration < deactivation_threshold:
                self.state = Agent.INACTIVE

        return self.state != previous_state

    def move_random(self, step_size=0.1, bounds=(0, 10)):
        """
        Random walk movement within bounds.

        Inputs:
            step_size (float): Maximum displacement per step
            bounds (tuple): (min, max) coordinate values
        """
        # Random displacement
        dx = random.uniform(-step_size, step_size)
        dy = random.uniform(-step_size, step_size)

        # Apply movement with boundary constraints
        self.x = max(bounds[0], min(bounds[1], self.x + dx))
        self.y = max(bounds[0], min(bounds[1], self.y + dy))

    def is_active(self):
        """Check if agent is in active state."""
        return self.state == Agent.ACTIVE

    def get_position(self):
        """Return agent position as tuple."""
        return (self.x, self.y)

    def __repr__(self):
        state_str = "ACTIVE" if self.is_active() else "INACTIVE"
        return f"Agent({self.id}, pos=({self.x:.2f},{self.y:.2f}), {state_str})"