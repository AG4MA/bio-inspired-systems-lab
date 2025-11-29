# environment.py
# Purpose: Environment with concentration gradient field for chemotaxis simulation
# Supports single or multiple attractant sources

import math


class GradientEnvironment:
    """
    Environment containing a concentration field with one or more sources.
    Agents can query local concentration at any position.
    """

    def __init__(self, width, height, noise_level=0.0):
        """
        Initialize the gradient environment.

        Inputs:
            width, height (float): Environment dimensions
            noise_level (float): Standard deviation of sensing noise
        """
        self.width = width
        self.height = height
        self.noise_level = noise_level
        self.sources = []  # List of (x, y, strength) tuples

    def add_source(self, x, y, strength=10.0):
        """
        Add an attractant source to the environment.

        Inputs:
            x, y (float): Source position
            strength (float): Source intensity
        """
        self.sources.append((x, y, strength))

    def get_concentration(self, x, y):
        """
        Calculate concentration at a given position.
        Uses inverse-square falloff from sources.

        Inputs:
            x, y (float): Query position

        Outputs:
            float: Concentration value (with optional noise)
        """
        if not self.sources:
            return 0.0

        total = 0.0
        for sx, sy, strength in self.sources:
            # Distance to source
            dist = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
            # Inverse distance falloff (avoid division by zero)
            total += strength / (1.0 + dist)

        # Add sensing noise if configured
        if self.noise_level > 0:
            import random
            total += random.gauss(0, self.noise_level)
            total = max(0, total)  # Concentration cannot be negative

        return total

    def get_gradient(self, x, y, epsilon=0.1):
        """
        Estimate gradient at a position using finite differences.

        Inputs:
            x, y (float): Query position
            epsilon (float): Step size for numerical gradient

        Outputs:
            tuple: (dx, dy) gradient vector pointing uphill
        """
        c_center = self.get_concentration(x, y)
        c_right = self.get_concentration(x + epsilon, y)
        c_up = self.get_concentration(x, y + epsilon)

        grad_x = (c_right - c_center) / epsilon
        grad_y = (c_up - c_center) / epsilon

        return (grad_x, grad_y)

    def get_max_concentration_position(self):
        """
        Find position of highest concentration (for analysis).

        Outputs:
            tuple: (x, y) of maximum concentration
        """
        if not self.sources:
            return (self.width / 2, self.height / 2)

        # For single source, it's at the source
        # For multiple, find weighted center
        if len(self.sources) == 1:
            return (self.sources[0][0], self.sources[0][1])

        # Return strongest source position
        strongest = max(self.sources, key=lambda s: s[2])
        return (strongest[0], strongest[1])

    def __repr__(self):
        return f"GradientEnvironment({self.width}x{self.height}, sources={len(self.sources)})"
