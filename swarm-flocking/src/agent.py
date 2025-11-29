# agent.py
# Purpose: Flocking agent implementing Reynolds' rules (separation, alignment, cohesion)
# Produces emergent swarm behavior from simple local rules

import math


class FlockingAgent:
    """
    Agent that follows Reynolds' flocking rules.
    Combines separation, alignment, and cohesion behaviors.
    """

    def __init__(self, agent_id, x, y, vx=0, vy=0):
        """
        Initialize a flocking agent.

        Inputs:
            agent_id (int): Unique identifier
            x, y (float): Initial position
            vx, vy (float): Initial velocity
        """
        self.id = agent_id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        # Flocking parameters
        self.perception_radius = 5.0
        self.separation_radius = 1.5
        self.max_speed = 2.0
        self.max_force = 0.3

        # Behavior weights
        self.w_separation = 1.5
        self.w_alignment = 1.0
        self.w_cohesion = 1.0

    def distance_to(self, other):
        """Calculate Euclidean distance to another agent."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def get_neighbors(self, all_agents):
        """
        Find all agents within perception radius.

        Inputs:
            all_agents (list): All agents in simulation

        Outputs:
            list: Neighbors within perception radius
        """
        neighbors = []
        for agent in all_agents:
            if agent.id != self.id:
                if self.distance_to(agent) < self.perception_radius:
                    neighbors.append(agent)
        return neighbors

    def separation(self, neighbors):
        """
        Calculate separation force: steer away from nearby neighbors.

        Inputs:
            neighbors (list): Nearby agents

        Outputs:
            tuple: (fx, fy) separation force
        """
        fx, fy = 0.0, 0.0
        count = 0

        for neighbor in neighbors:
            dist = self.distance_to(neighbor)
            if dist < self.separation_radius and dist > 0:
                # Vector pointing away from neighbor
                dx = self.x - neighbor.x
                dy = self.y - neighbor.y
                # Weight by inverse distance (closer = stronger repulsion)
                fx += dx / (dist * dist)
                fy += dy / (dist * dist)
                count += 1

        if count > 0:
            fx /= count
            fy /= count

        return (fx, fy)

    def alignment(self, neighbors):
        """
        Calculate alignment force: steer toward average heading of neighbors.

        Inputs:
            neighbors (list): Nearby agents

        Outputs:
            tuple: (fx, fy) alignment force
        """
        if not neighbors:
            return (0.0, 0.0)

        # Average velocity of neighbors
        avg_vx = sum(n.vx for n in neighbors) / len(neighbors)
        avg_vy = sum(n.vy for n in neighbors) / len(neighbors)

        # Desired change in velocity
        fx = avg_vx - self.vx
        fy = avg_vy - self.vy

        return (fx, fy)

    def cohesion(self, neighbors):
        """
        Calculate cohesion force: steer toward center of mass of neighbors.

        Inputs:
            neighbors (list): Nearby agents

        Outputs:
            tuple: (fx, fy) cohesion force
        """
        if not neighbors:
            return (0.0, 0.0)

        # Center of mass of neighbors
        center_x = sum(n.x for n in neighbors) / len(neighbors)
        center_y = sum(n.y for n in neighbors) / len(neighbors)

        # Direction toward center
        fx = center_x - self.x
        fy = center_y - self.y

        return (fx, fy)

    def limit_magnitude(self, vx, vy, max_mag):
        """
        Limit vector magnitude while preserving direction.

        Inputs:
            vx, vy (float): Vector components
            max_mag (float): Maximum magnitude

        Outputs:
            tuple: (vx, vy) limited vector
        """
        mag = math.sqrt(vx * vx + vy * vy)
        if mag > max_mag and mag > 0:
            vx = vx / mag * max_mag
            vy = vy / mag * max_mag
        return (vx, vy)

    def update(self, all_agents, bounds=None):
        """
        Update agent position and velocity based on flocking rules.

        Inputs:
            all_agents (list): All agents for neighbor detection
            bounds (tuple): Optional (min, max) boundary
        """
        neighbors = self.get_neighbors(all_agents)

        # Calculate forces
        sep = self.separation(neighbors)
        ali = self.alignment(neighbors)
        coh = self.cohesion(neighbors)

        # Combine forces with weights
        ax = sep[0] * self.w_separation + ali[0] * self.w_alignment + coh[0] * self.w_cohesion
        ay = sep[1] * self.w_separation + ali[1] * self.w_alignment + coh[1] * self.w_cohesion

        # Limit acceleration
        ax, ay = self.limit_magnitude(ax, ay, self.max_force)

        # Update velocity
        self.vx += ax
        self.vy += ay

        # Limit speed
        self.vx, self.vy = self.limit_magnitude(self.vx, self.vy, self.max_speed)

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Handle boundaries (wrap around)
        if bounds:
            min_b, max_b = bounds
            if self.x < min_b: self.x = max_b
            if self.x > max_b: self.x = min_b
            if self.y < min_b: self.y = max_b
            if self.y > max_b: self.y = min_b

    def get_position(self):
        """Return current position."""
        return (self.x, self.y)

    def get_velocity(self):
        """Return current velocity."""
        return (self.vx, self.vy)

    def __repr__(self):
        return f"FlockingAgent({self.id}, pos=({self.x:.2f},{self.y:.2f}))"
