# agent.py
# Purpose: Slime mold agent for decentralized pathfinding
# Explores, deposits pheromones, and reinforces successful paths

import random
import math


class SlimeAgent:
    """
    Agent representing a slime mold extension.
    Explores environment, deposits pheromone, reinforces paths to food.
    """

    # Agent modes
    EXPLORING = 'exploring'
    RETURNING = 'returning'
    DEAD = 'dead'

    def __init__(self, agent_id, x, y, origin):
        """
        Initialize a slime agent.

        Inputs:
            agent_id (int): Unique identifier
            x, y (float): Starting position
            origin (tuple): (x, y) of origin point (home base)
        """
        self.id = agent_id
        self.x = x
        self.y = y
        self.origin = origin
        self.mode = SlimeAgent.EXPLORING

        # Path memory for backtracking
        self.path_history = [(x, y)]

        # Movement parameters
        self.speed = 0.5
        self.exploration_bias = 0.3  # How much to favor pheromone vs random

        # Pheromone parameters
        self.deposition_amount = 0.5
        self.reinforcement_bonus = 2.0

        # State
        self.found_food = False
        self.steps_alive = 0
        self.max_steps = 200

    def distance_to(self, x, y):
        """Calculate distance to a point."""
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

    def get_possible_moves(self, environment, num_directions=8):
        """
        Get possible movement directions weighted by pheromone.

        Inputs:
            environment: PheromoneEnvironment
            num_directions (int): Number of directions to consider

        Outputs:
            list: (dx, dy, weight) tuples
        """
        moves = []
        for i in range(num_directions):
            angle = 2 * math.pi * i / num_directions
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed

            new_x = self.x + dx
            new_y = self.y + dy

            # Check bounds
            if not environment.in_bounds(new_x, new_y):
                continue

            # Check obstacles
            if environment.is_obstacle(new_x, new_y):
                continue

            # Weight by pheromone (with exploration factor)
            pheromone = environment.get_pheromone(new_x, new_y)
            weight = 1.0 + pheromone * self.exploration_bias

            moves.append((dx, dy, weight))

        return moves

    def choose_direction(self, environment):
        """
        Choose movement direction using weighted random selection.

        Inputs:
            environment: PheromoneEnvironment

        Outputs:
            tuple: (dx, dy) movement vector, or None if stuck
        """
        moves = self.get_possible_moves(environment)

        if not moves:
            return None

        # Weighted random selection
        total_weight = sum(m[2] for m in moves)
        r = random.uniform(0, total_weight)
        cumulative = 0

        for dx, dy, weight in moves:
            cumulative += weight
            if cumulative >= r:
                return (dx, dy)

        return moves[-1][:2]

    def move(self, dx, dy):
        """
        Move agent by displacement.

        Inputs:
            dx, dy (float): Movement vector
        """
        self.x += dx
        self.y += dy
        self.path_history.append((self.x, self.y))

    def backtrack_step(self):
        """
        Move one step back toward origin.

        Outputs:
            bool: True if still backtracking, False if reached origin
        """
        if len(self.path_history) <= 1:
            return False

        # Pop current position, move to previous
        self.path_history.pop()
        if self.path_history:
            prev = self.path_history[-1]
            self.x, self.y = prev

        # Check if back at origin
        if self.distance_to(self.origin[0], self.origin[1]) < self.speed:
            return False

        return True

    def update(self, environment):
        """
        Perform one simulation step.

        Inputs:
            environment: PheromoneEnvironment

        Outputs:
            str: Action taken
        """
        if self.mode == SlimeAgent.DEAD:
            return 'dead'

        self.steps_alive += 1

        # Check for timeout
        if self.steps_alive > self.max_steps and not self.found_food:
            self.mode = SlimeAgent.DEAD
            return 'timeout'

        if self.mode == SlimeAgent.EXPLORING:
            # Check for food
            if environment.is_food(self.x, self.y):
                self.found_food = True
                self.mode = SlimeAgent.RETURNING
                return 'found_food'

            # Explore: move and deposit light pheromone
            direction = self.choose_direction(environment)
            if direction is None:
                self.mode = SlimeAgent.DEAD
                return 'stuck'

            self.move(direction[0], direction[1])
            environment.add_pheromone(self.x, self.y, self.deposition_amount)
            return 'exploring'

        elif self.mode == SlimeAgent.RETURNING:
            # Backtrack and reinforce path
            environment.add_pheromone(
                self.x, self.y,
                self.deposition_amount * self.reinforcement_bonus
            )

            if not self.backtrack_step():
                self.mode = SlimeAgent.DEAD  # Reached origin, done
                return 'completed'

            return 'returning'

        return 'unknown'

    def is_alive(self):
        """Check if agent is still active."""
        return self.mode != SlimeAgent.DEAD

    def __repr__(self):
        return f"SlimeAgent({self.id}, mode={self.mode}, pos=({self.x:.2f},{self.y:.2f}))"
