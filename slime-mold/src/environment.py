# environment.py
# Purpose: Environment with pheromone field, obstacles, and food sources
# Supports slime mold pathfinding simulation

import math


class PheromoneEnvironment:
    """
    Grid environment with pheromone diffusion, obstacles, and food sources.
    """

    def __init__(self, width, height, resolution=50):
        """
        Initialize environment.

        Inputs:
            width, height (float): Physical dimensions
            resolution (int): Grid cells per dimension
        """
        self.width = width
        self.height = height
        self.resolution = resolution

        # Pheromone grid
        self.pheromone = [[0.0 for _ in range(resolution)] for _ in range(resolution)]

        # Obstacles (set of (row, col) tuples)
        self.obstacles = set()

        # Food sources (list of (x, y) positions)
        self.food_sources = []

        # Parameters
        self.evaporation_rate = 0.02
        self.diffusion_rate = 0.1
        self.cell_size = width / resolution

    def pos_to_cell(self, x, y):
        """Convert world position to grid cell."""
        col = int(min(max(0, x / self.cell_size), self.resolution - 1))
        row = int(min(max(0, y / self.cell_size), self.resolution - 1))
        return (row, col)

    def cell_to_pos(self, row, col):
        """Convert grid cell to world position (center)."""
        x = (col + 0.5) * self.cell_size
        y = (row + 0.5) * self.cell_size
        return (x, y)

    def in_bounds(self, x, y):
        """Check if position is within environment."""
        return 0 <= x <= self.width and 0 <= y <= self.height

    def add_obstacle(self, x, y, radius=1.0):
        """
        Add circular obstacle.

        Inputs:
            x, y (float): Center position
            radius (float): Obstacle radius
        """
        for row in range(self.resolution):
            for col in range(self.resolution):
                cx, cy = self.cell_to_pos(row, col)
                if math.sqrt((cx - x)**2 + (cy - y)**2) < radius:
                    self.obstacles.add((row, col))

    def is_obstacle(self, x, y):
        """Check if position is blocked by obstacle."""
        row, col = self.pos_to_cell(x, y)
        return (row, col) in self.obstacles

    def add_food(self, x, y):
        """Add food source at position."""
        self.food_sources.append((x, y))

    def is_food(self, x, y, radius=0.5):
        """Check if position is at a food source."""
        for fx, fy in self.food_sources:
            if math.sqrt((x - fx)**2 + (y - fy)**2) < radius:
                return True
        return False

    def add_pheromone(self, x, y, amount):
        """Deposit pheromone at position."""
        row, col = self.pos_to_cell(x, y)
        if (row, col) not in self.obstacles:
            self.pheromone[row][col] += amount

    def get_pheromone(self, x, y):
        """Get pheromone concentration at position."""
        row, col = self.pos_to_cell(x, y)
        return self.pheromone[row][col]

    def evaporate(self):
        """Apply evaporation to all pheromone."""
        for row in range(self.resolution):
            for col in range(self.resolution):
                self.pheromone[row][col] *= (1.0 - self.evaporation_rate)

    def diffuse(self):
        """Diffuse pheromone to neighboring cells."""
        new_pheromone = [[0.0 for _ in range(self.resolution)] for _ in range(self.resolution)]

        for row in range(self.resolution):
            for col in range(self.resolution):
                if (row, col) in self.obstacles:
                    continue

                # Gather neighbor values
                neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.resolution and 0 <= nc < self.resolution:
                            if (nr, nc) not in self.obstacles:
                                neighbors.append(self.pheromone[nr][nc])

                # Blend with neighbors
                if neighbors:
                    avg = sum(neighbors) / len(neighbors)
                    current = self.pheromone[row][col]
                    new_pheromone[row][col] = current + self.diffusion_rate * (avg - current)

        self.pheromone = new_pheromone

    def update(self):
        """Perform environment update step."""
        self.evaporate()
        self.diffuse()

    def get_total_pheromone(self):
        """Calculate total pheromone in environment."""
        return sum(sum(row) for row in self.pheromone)

    def get_path_strength(self, start, end, sample_points=20):
        """
        Estimate path strength between two points.

        Inputs:
            start, end (tuple): (x, y) positions
            sample_points (int): Number of samples along path

        Outputs:
            float: Average pheromone along direct path
        """
        total = 0.0
        for i in range(sample_points):
            t = i / (sample_points - 1)
            x = start[0] + t * (end[0] - start[0])
            y = start[1] + t * (end[1] - start[1])
            total += self.get_pheromone(x, y)
        return total / sample_points

    def __repr__(self):
        return f"PheromoneEnvironment({self.width}x{self.height}, food={len(self.food_sources)})"
