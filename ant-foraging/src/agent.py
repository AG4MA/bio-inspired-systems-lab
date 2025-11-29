# agent.py
# Purpose: Ant agent for ant colony optimization
# Builds paths, deposits pheromones, and enables collective optimization

import random
import math


class AntAgent:
    """
    Ant that explores graph, finds food, and deposits pheromone trails.
    Implements basic ACO behavior for pathfinding.
    """

    def __init__(self, ant_id, nest_node, alpha=1.0, beta=2.0):
        """
        Initialize an ant.

        Inputs:
            ant_id (int): Unique identifier
            nest_node: Starting node (nest)
            alpha (float): Pheromone influence weight
            beta (float): Distance influence weight
        """
        self.id = ant_id
        self.nest = nest_node
        self.alpha = alpha
        self.beta = beta

        # Current state
        self.current_node = nest_node
        self.path = [nest_node]
        self.path_length = 0.0
        self.visited = {nest_node}

        # Status
        self.found_food = False
        self.returning = False
        self.completed = False

    def reset(self):
        """Reset ant for a new foraging trip."""
        self.current_node = self.nest
        self.path = [self.nest]
        self.path_length = 0.0
        self.visited = {self.nest}
        self.found_food = False
        self.returning = False
        self.completed = False

    def get_transition_probabilities(self, neighbors, pheromone, distances):
        """
        Calculate probabilities for moving to each neighbor.

        Inputs:
            neighbors (list): Available next nodes
            pheromone (dict): Pheromone levels for edges
            distances (dict): Distances to neighbors

        Outputs:
            list: (node, probability) tuples
        """
        probabilities = []
        total = 0.0

        for neighbor in neighbors:
            if neighbor in self.visited:
                continue

            # Get edge pheromone and distance
            edge = (self.current_node, neighbor)
            tau = pheromone.get(edge, 0.1)  # Default pheromone
            dist = distances.get(edge, 1.0)
            eta = 1.0 / dist  # Inverse distance (desirability)

            # ACO probability formula
            weight = (tau ** self.alpha) * (eta ** self.beta)
            probabilities.append((neighbor, weight))
            total += weight

        # Normalize
        if total > 0:
            probabilities = [(n, w / total) for n, w in probabilities]

        return probabilities

    def select_next_node(self, probabilities):
        """
        Select next node using roulette wheel selection.

        Inputs:
            probabilities (list): (node, probability) tuples

        Outputs:
            node: Selected next node, or None if stuck
        """
        if not probabilities:
            return None

        r = random.random()
        cumulative = 0.0

        for node, prob in probabilities:
            cumulative += prob
            if cumulative >= r:
                return node

        return probabilities[-1][0]

    def move_to(self, node, distance):
        """
        Move to a node, updating path.

        Inputs:
            node: Destination node
            distance (float): Distance traveled
        """
        self.path.append(node)
        self.path_length += distance
        self.visited.add(node)
        self.current_node = node

    def step(self, graph, pheromone, food_nodes):
        """
        Perform one step of foraging.

        Inputs:
            graph (dict): Adjacency structure with distances
            pheromone (dict): Current pheromone levels
            food_nodes (set): Nodes containing food

        Outputs:
            str: Status ('moving', 'found_food', 'returning', 'completed', 'stuck')
        """
        if self.completed:
            return 'completed'

        # Returning to nest
        if self.returning:
            if self.current_node == self.nest:
                self.completed = True
                return 'completed'
            # Return via recorded path
            if len(self.path) > 1:
                self.path.pop()
                self.current_node = self.path[-1]
            return 'returning'

        # Exploring
        if self.current_node in food_nodes:
            self.found_food = True
            self.returning = True
            return 'found_food'

        # Get neighbors
        neighbors = graph.get(self.current_node, {})
        distances = {(self.current_node, n): d for n, d in neighbors.items()}

        # Calculate probabilities
        probs = self.get_transition_probabilities(
            list(neighbors.keys()), pheromone, distances
        )

        # Select and move
        next_node = self.select_next_node(probs)
        if next_node is None:
            return 'stuck'

        distance = neighbors[next_node]
        self.move_to(next_node, distance)

        return 'moving'

    def get_path_edges(self):
        """
        Get list of edges in the path.

        Outputs:
            list: List of (from, to) tuples
        """
        edges = []
        for i in range(len(self.path) - 1):
            edges.append((self.path[i], self.path[i + 1]))
        return edges

    def __repr__(self):
        status = 'completed' if self.completed else ('returning' if self.returning else 'exploring')
        return f"Ant({self.id}, at={self.current_node}, status={status}, length={self.path_length:.2f})"
