# environment.py
# Purpose: Graph environment with pheromone management for ACO
# Tracks pheromone levels, handles evaporation and deposition

import math


class AntColonyEnvironment:
    """
    Graph environment for ant colony optimization.
    Manages pheromone trails and provides graph structure.
    """

    def __init__(self, evaporation_rate=0.1, initial_pheromone=0.1):
        """
        Initialize environment.

        Inputs:
            evaporation_rate (float): Pheromone decay rate per iteration
            initial_pheromone (float): Starting pheromone on all edges
        """
        self.evaporation_rate = evaporation_rate
        self.initial_pheromone = initial_pheromone

        # Graph structure: node -> {neighbor: distance}
        self.graph = {}

        # Pheromone levels: (from, to) -> level
        self.pheromone = {}

        # Special nodes
        self.nest = None
        self.food_nodes = set()

    def add_node(self, node):
        """Add a node to the graph."""
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, from_node, to_node, distance):
        """
        Add bidirectional edge.

        Inputs:
            from_node, to_node: Node identifiers
            distance (float): Edge weight
        """
        self.add_node(from_node)
        self.add_node(to_node)

        self.graph[from_node][to_node] = distance
        self.graph[to_node][from_node] = distance

        # Initialize pheromone
        self.pheromone[(from_node, to_node)] = self.initial_pheromone
        self.pheromone[(to_node, from_node)] = self.initial_pheromone

    def set_nest(self, node):
        """Set the nest node."""
        self.nest = node
        self.add_node(node)

    def add_food(self, node):
        """Add a food source node."""
        self.food_nodes.add(node)
        self.add_node(node)

    def create_random_graph(self, num_nodes, connectivity=0.4, max_distance=10.0):
        """
        Create a random connected graph.

        Inputs:
            num_nodes (int): Number of nodes
            connectivity (float): Probability of edge between any two nodes
            max_distance (float): Maximum edge distance
        """
        import random

        nodes = list(range(num_nodes))

        # Ensure connectivity: create spanning tree first
        for i in range(1, num_nodes):
            target = random.randint(0, i - 1)
            dist = random.uniform(1.0, max_distance)
            self.add_edge(i, target, dist)

        # Add random additional edges
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if (i, j) not in self.pheromone and random.random() < connectivity:
                    dist = random.uniform(1.0, max_distance)
                    self.add_edge(i, j, dist)

        # Set nest and food
        self.set_nest(0)
        self.add_food(num_nodes - 1)

    def evaporate(self):
        """Apply evaporation to all pheromone trails."""
        for edge in self.pheromone:
            self.pheromone[edge] *= (1.0 - self.evaporation_rate)
            # Keep minimum level
            self.pheromone[edge] = max(self.pheromone[edge], 0.01)

    def deposit_pheromone(self, edges, amount):
        """
        Deposit pheromone on edges.

        Inputs:
            edges (list): List of (from, to) tuples
            amount (float): Amount to deposit per edge
        """
        for edge in edges:
            if edge in self.pheromone:
                self.pheromone[edge] += amount
            # Also deposit on reverse edge
            reverse = (edge[1], edge[0])
            if reverse in self.pheromone:
                self.pheromone[reverse] += amount

    def get_best_path(self, from_node, to_node):
        """
        Find current best path based on pheromone (greedy).

        Inputs:
            from_node, to_node: Start and end nodes

        Outputs:
            tuple: (path list, total distance)
        """
        path = [from_node]
        visited = {from_node}
        current = from_node
        total_dist = 0.0

        while current != to_node:
            neighbors = self.graph.get(current, {})
            best_next = None
            best_pheromone = -1

            for neighbor, dist in neighbors.items():
                if neighbor not in visited:
                    edge_pheromone = self.pheromone.get((current, neighbor), 0)
                    if edge_pheromone > best_pheromone:
                        best_pheromone = edge_pheromone
                        best_next = (neighbor, dist)

            if best_next is None:
                return None, float('inf')  # No path found

            path.append(best_next[0])
            visited.add(best_next[0])
            total_dist += best_next[1]
            current = best_next[0]

        return path, total_dist

    def __repr__(self):
        return f"AntColonyEnvironment(nodes={len(self.graph)}, edges={len(self.pheromone)//2})"
