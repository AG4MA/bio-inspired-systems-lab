# morphogenesis_simulation.py
# Purpose: Simulate Turing pattern formation via reaction-diffusion
# Demonstrates emergent spatial patterns from local chemical interactions

import random


class ReactionDiffusionGrid:
    """
    Grid implementing Gray-Scott reaction-diffusion model.
    Simpler and more numerically stable than Gierer-Meinhardt.
    """

    def __init__(self, width, height):
        """
        Initialize the grid.

        Inputs:
            width, height (int): Grid dimensions
        """
        self.width = width
        self.height = height

        # Chemical concentrations (A = activator/U, B = inhibitor/V)
        self.A = [[1.0 for _ in range(width)] for _ in range(height)]
        self.B = [[0.0 for _ in range(width)] for _ in range(height)]

        # Gray-Scott parameters
        self.D_a = 1.0      # Diffusion rate of A
        self.D_b = 0.5      # Diffusion rate of B (typically D_b < D_a for Gray-Scott)
        self.feed = 0.055   # Feed rate of A
        self.kill = 0.062   # Kill rate of B

        self.dt = 1.0       # Time step

    def add_seed(self, x, y, radius=3):
        """
        Add a seed region of B chemical.

        Inputs:
            x, y (int): Center of seed
            radius (int): Seed radius
        """
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    nx = (x + dx) % self.width
                    ny = (y + dy) % self.height
                    self.B[ny][nx] = 1.0
                    self.A[ny][nx] = 0.5

    def add_noise(self, amount=0.05):
        """
        Add random perturbation to initial conditions.

        Inputs:
            amount (float): Noise amplitude
        """
        for y in range(self.height):
            for x in range(self.width):
                self.A[y][x] += random.uniform(-amount, amount)
                self.B[y][x] += random.uniform(-amount, amount)
                # Clamp to valid range
                self.A[y][x] = max(0, min(1, self.A[y][x]))
                self.B[y][x] = max(0, min(1, self.B[y][x]))

    def laplacian(self, grid, x, y):
        """
        Compute discrete Laplacian at a point (5-point stencil).

        Inputs:
            grid (2D list): Concentration grid
            x, y (int): Position

        Outputs:
            float: Laplacian value
        """
        # Periodic boundary conditions
        xp = (x + 1) % self.width
        xm = (x - 1) % self.width
        yp = (y + 1) % self.height
        ym = (y - 1) % self.height

        center = grid[y][x]
        neighbors = grid[y][xp] + grid[y][xm] + grid[yp][x] + grid[ym][x]

        return neighbors - 4 * center

    def step(self):
        """
        Perform one reaction-diffusion step.
        Uses Gray-Scott model equations.
        """
        new_A = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        new_B = [[0.0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                a = self.A[y][x]
                b = self.B[y][x]

                # Reaction term
                reaction = a * b * b

                # Diffusion (Laplacian)
                lap_a = self.laplacian(self.A, x, y)
                lap_b = self.laplacian(self.B, x, y)

                # Gray-Scott equations
                da = self.D_a * lap_a - reaction + self.feed * (1.0 - a)
                db = self.D_b * lap_b + reaction - (self.kill + self.feed) * b

                # Update
                new_A[y][x] = max(0, min(1, a + da * self.dt))
                new_B[y][x] = max(0, min(1, b + db * self.dt))

        self.A = new_A
        self.B = new_B

    def get_pattern_stats(self):
        """
        Calculate pattern statistics.

        Outputs:
            dict: Statistics about current pattern
        """
        total_a = sum(sum(row) for row in self.A)
        total_b = sum(sum(row) for row in self.B)
        cells = self.width * self.height

        # Count "active" cells (where B is significant)
        active = sum(1 for y in range(self.height)
                     for x in range(self.width) if self.B[y][x] > 0.2)

        return {
            'mean_A': total_a / cells,
            'mean_B': total_b / cells,
            'active_fraction': active / cells
        }

    def print_pattern(self, threshold=0.2):
        """
        Print ASCII representation of pattern.

        Inputs:
            threshold (float): B concentration for "active" display
        """
        chars = " .:-=+*#@"
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                b = self.B[y][x]
                idx = int(b * (len(chars) - 1))
                row += chars[min(idx, len(chars) - 1)]
            print(row)


def run_simulation(width=60, height=30, num_steps=1000, num_seeds=5):
    """
    Run morphogenesis simulation.

    Inputs:
        width, height (int): Grid dimensions
        num_steps (int): Simulation duration
        num_seeds (int): Number of initial B seeds

    Outputs:
        dict: Simulation results
    """
    grid = ReactionDiffusionGrid(width, height)

    # Add seed regions
    for _ in range(num_seeds):
        x = random.randint(5, width - 5)
        y = random.randint(5, height - 5)
        grid.add_seed(x, y, radius=2)

    # Add small noise
    grid.add_noise(0.02)

    history = {
        'stats': []
    }

    print(f"Morphogenesis Simulation: {width}x{height} grid")
    print("-" * 60)

    for step in range(num_steps):
        grid.step()

        # Record stats periodically
        if step % 100 == 0 or step == num_steps - 1:
            stats = grid.get_pattern_stats()
            history['stats'].append({'step': step, **stats})

            print(f"Step {step:4d}: mean_B={stats['mean_B']:.4f}, "
                  f"active={stats['active_fraction']:.2%}")

    print("-" * 60)
    print("\nFinal pattern:")
    grid.print_pattern()

    return {
        'grid': grid,
        'history': history
    }


def analyze_results(results):
    """
    Analyze simulation results.

    Inputs:
        results (dict): Results from run_simulation
    """
    history = results['history']
    grid = results['grid']

    final_stats = history['stats'][-1]

    print("\n=== Analysis ===")
    print(f"Final mean B: {final_stats['mean_B']:.4f}")
    print(f"Active fraction: {final_stats['active_fraction']:.2%}")

    if final_stats['active_fraction'] > 0.1:
        print("Result: Pattern successfully formed")
    else:
        print("Result: Pattern formation minimal")


def main():
    """Main entry point."""
    results = run_simulation(
        width=50,
        height=25,
        num_steps=2000,
        num_seeds=3
    )
    analyze_results(results)


if __name__ == "__main__":
    main()
