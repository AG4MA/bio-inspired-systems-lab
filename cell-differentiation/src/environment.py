# environment.py
# Purpose: Environment with multiple signal types for differentiation cues
# Simulates morphogen gradients and local condition signals

import math


class DifferentiationEnvironment:
    """
    Environment providing signals that guide cell differentiation.
    Multiple signal types create complex differentiation landscapes.
    """

    def __init__(self, width, height):
        """
        Initialize the environment.

        Inputs:
            width, height (float): Environment dimensions
        """
        self.width = width
        self.height = height
        self.signal_sources = []  # List of (type, x, y, strength)

    def add_signal_source(self, signal_type, x, y, strength=1.0):
        """
        Add a signal source.

        Inputs:
            signal_type (str): Type of signal
            x, y (float): Source position
            strength (float): Signal intensity
        """
        self.signal_sources.append((signal_type, x, y, strength))

    def setup_default_signals(self):
        """Create a typical differentiation environment."""
        # Task signal in center
        self.add_signal_source('task', self.width / 2, self.height / 2, 2.0)

        # Edge signal (high at boundaries)
        # Simulated by distance from center

        # Threat signal in one corner
        self.add_signal_source('threat', self.width * 0.9, self.height * 0.9, 1.5)

    def get_signals_at(self, x, y):
        """
        Get all signal concentrations at a position.

        Inputs:
            x, y (float): Query position

        Outputs:
            dict: Signal type -> concentration
        """
        signals = {
            'task': 0.0,
            'threat': 0.0,
            'edge': 0.0
        }

        # Calculate signal from sources
        for signal_type, sx, sy, strength in self.signal_sources:
            dist = math.sqrt((x - sx)**2 + (y - sy)**2)
            concentration = strength / (1.0 + dist)
            signals[signal_type] = signals.get(signal_type, 0) + concentration

        # Edge signal based on distance from center
        center_dist = math.sqrt((x - self.width/2)**2 + (y - self.height/2)**2)
        max_dist = math.sqrt((self.width/2)**2 + (self.height/2)**2)
        signals['edge'] = center_dist / max_dist

        return signals

    def __repr__(self):
        return f"DifferentiationEnvironment({self.width}x{self.height}, sources={len(self.signal_sources)})"
