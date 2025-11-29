# environment.py
# Purpose: Defines the Environment class for quorum sensing simulation
# Manages signal diffusion, decay, and spatial concentration grid

import math


class Environment:
    """
    2D environment with signal diffusion dynamics.
    Tracks concentration of autoinducer molecules across a grid.
    """

    def __init__(self, width, height, resolution=20, diffusion_rate=0.1, decay_rate=0.05):
        """
        Initialize the environment grid.

        Inputs:
            width, height (float): Physical dimensions of the environment
            resolution (int): Grid cells per dimension
            diffusion_rate (float): Rate of signal spread to neighbors
            decay_rate (float): Rate of signal decay per step
        """
        self.width = width
        self.height = height
        self.resolution = resolution
        self.diffusion_rate = diffusion_rate
        self.decay_rate = decay_rate

        # Initialize concentration grid
        self.grid = [[0.0 for _ in range(resolution)] for _ in range(resolution)]
        self.cell_width = width / resolution
        self.cell_height = height / resolution

    def position_to_cell(self, x, y):
        """
        Convert world coordinates to grid cell indices.

        Inputs:
            x, y (float): World coordinates

        Outputs:
            tuple: (row, col) grid indices
        """
        col = int(min(x / self.cell_width, self.resolution - 1))
        row = int(min(y / self.cell_height, self.resolution - 1))
        return max(0, row), max(0, col)

    def add_signal(self, x, y, amount):
        """
        Add signal molecules at a specific position.

        Inputs:
            x, y (float): World coordinates
            amount (float): Amount of signal to add
        """
        row, col = self.position_to_cell(x, y)
        self.grid[row][col] += amount

    def get_concentration(self, x, y):
        """
        Get signal concentration at a position.

        Inputs:
            x, y (float): World coordinates

        Outputs:
            float: Local signal concentration
        """
        row, col = self.position_to_cell(x, y)
        return self.grid[row][col]

    def diffuse(self):
        """
        Apply diffusion: spread signals to neighboring cells.
        Uses simple averaging with neighbors.
        """
        new_grid = [[0.0 for _ in range(self.resolution)] for _ in range(self.resolution)]

        for row in range(self.resolution):
            for col in range(self.resolution):
                # Collect neighbor concentrations
                neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.resolution and 0 <= nc < self.resolution:
                            neighbors.append(self.grid[nr][nc])

                # Diffusion: blend with neighbor average
                avg_neighbor = sum(neighbors) / len(neighbors)
                current = self.grid[row][col]
                new_grid[row][col] = current + self.diffusion_rate * (avg_neighbor - current)

        self.grid = new_grid

    def decay(self):
        """Apply exponential decay to all signal concentrations."""
        for row in range(self.resolution):
            for col in range(self.resolution):
                self.grid[row][col] *= (1.0 - self.decay_rate)

    def update(self):
        """Perform one environment update step: diffuse then decay."""
        self.diffuse()
        self.decay()

    def get_total_signal(self):
        """Calculate total signal in environment."""
        return sum(sum(row) for row in self.grid)

    def get_max_concentration(self):
        """Find maximum concentration in environment."""
        return max(max(row) for row in self.grid)

    def reset(self):
        """Clear all signals from environment."""
        self.grid = [[0.0 for _ in range(self.resolution)] for _ in range(self.resolution)]

    def __repr__(self):
        return f"Environment({self.width}x{self.height}, resolution={self.resolution})"