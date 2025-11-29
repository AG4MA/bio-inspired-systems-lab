# agent.py
# Purpose: Chemotactic agent that follows gradients using run-and-tumble behavior
# Implements temporal gradient sensing without global knowledge

import random
import math


class ChemotaxisAgent:
    """
    Agent that navigates toward higher concentrations using
    the run-and-tumble strategy inspired by bacterial chemotaxis.
    """

    def __init__(self, agent_id, x, y, speed=0.5, sensitivity=2.0):
        """
        Initialize a chemotactic agent.

        Inputs:
            agent_id (int): Unique identifier
            x, y (float): Initial position
            speed (float): Movement speed per step
            sensitivity (float): How strongly improvements affect run duration
        """
        self.id = agent_id
        self.x = x
        self.y = y
        self.speed = speed
        self.sensitivity = sensitivity

        # Movement state
        self.direction = random.uniform(0, 2 * math.pi)
        self.run_timer = 0
        self.base_run_duration = 5

        # Sensing state
        self.previous_concentration = 0.0
        self.current_concentration = 0.0

        # Statistics
        self.tumble_count = 0
        self.total_improvement = 0.0

    def sense(self, concentration):
        """
        Sense local concentration and store for comparison.

        Inputs:
            concentration (float): Local concentration value
        """
        self.previous_concentration = self.current_concentration
        self.current_concentration = concentration

    def get_improvement(self):
        """
        Calculate improvement since last sensing.

        Outputs:
            float: Change in concentration (positive = improving)
        """
        return self.current_concentration - self.previous_concentration

    def tumble(self):
        """
        Perform a tumble: choose a new random direction.
        In real bacteria, tumbles are biased but we simplify to uniform random.
        """
        # Random new direction
        self.direction = random.uniform(0, 2 * math.pi)
        self.tumble_count += 1

    def run(self, bounds=(0, 10)):
        """
        Move in current direction for one step.

        Inputs:
            bounds (tuple): (min, max) coordinate boundaries
        """
        # Calculate displacement
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)

        # Apply movement with boundary reflection
        new_x = self.x + dx
        new_y = self.y + dy

        # Reflect off boundaries
        if new_x < bounds[0] or new_x > bounds[1]:
            self.direction = math.pi - self.direction
            new_x = max(bounds[0], min(bounds[1], new_x))
        if new_y < bounds[0] or new_y > bounds[1]:
            self.direction = -self.direction
            new_y = max(bounds[0], min(bounds[1], new_y))

        self.x = new_x
        self.y = new_y

    def update(self, concentration, bounds=(0, 10)):
        """
        Perform one step of chemotactic behavior.

        Inputs:
            concentration (float): Local concentration at current position
            bounds (tuple): Environment boundaries

        Outputs:
            str: Action taken ('run' or 'tumble')
        """
        self.sense(concentration)
        improvement = self.get_improvement()
        self.total_improvement += improvement

        # Decide action based on improvement
        if self.run_timer > 0:
            # Continue current run
            self.run(bounds)
            self.run_timer -= 1
            return 'run'
        else:
            # Time to decide: tumble or extend run
            if improvement > 0:
                # Good direction: longer run
                run_length = self.base_run_duration * (1 + improvement * self.sensitivity)
                self.run_timer = int(max(1, run_length))
            else:
                # Bad direction: tumble and short run
                self.tumble()
                self.run_timer = self.base_run_duration

            self.run(bounds)
            self.run_timer -= 1
            return 'tumble' if improvement <= 0 else 'run'

    def get_position(self):
        """Return current position as tuple."""
        return (self.x, self.y)

    def __repr__(self):
        return f"ChemotaxisAgent({self.id}, pos=({self.x:.2f},{self.y:.2f}), tumbles={self.tumble_count})"
