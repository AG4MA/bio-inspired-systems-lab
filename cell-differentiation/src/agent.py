# agent.py
# Purpose: Agent capable of differentiation into specialized roles
# All agents share same code but assume different functions based on context

import random


class DifferentiatingAgent:
    """
    Agent that can differentiate into specialized roles based on local signals.
    Implements lateral inhibition and context-dependent specialization.
    """

    # Available roles
    STEM = 'stem'
    LEADER = 'leader'
    WORKER = 'worker'
    SCOUT = 'scout'
    GUARD = 'guard'

    ALL_ROLES = [STEM, LEADER, WORKER, SCOUT, GUARD]

    def __init__(self, agent_id, x, y):
        """
        Initialize an undifferentiated agent.

        Inputs:
            agent_id (int): Unique identifier
            x, y (float): Position
        """
        self.id = agent_id
        self.x = x
        self.y = y
        self.role = DifferentiatingAgent.STEM

        # Differentiation state
        self.differentiation_timer = 0
        self.commitment_level = 0.0  # 0 = plastic, 1 = fully committed

        # Role-specific output
        self.signal_output = {}
        self.task_output = 0

        # Sensing
        self.sensed_signals = {}
        self.nearby_roles = {}

    def distance_to(self, other):
        """Calculate distance to another agent."""
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def sense_neighbors(self, all_agents, radius=3.0):
        """
        Sense roles of nearby agents.

        Inputs:
            all_agents (list): All agents
            radius (float): Sensing radius
        """
        self.nearby_roles = {role: 0 for role in self.ALL_ROLES}

        for agent in all_agents:
            if agent.id != self.id and self.distance_to(agent) < radius:
                self.nearby_roles[agent.role] = self.nearby_roles.get(agent.role, 0) + 1

    def sense_signals(self, environment):
        """
        Sense local signal concentrations.

        Inputs:
            environment: Environment with signal fields
        """
        self.sensed_signals = environment.get_signals_at(self.x, self.y)

    def can_differentiate(self):
        """Check if agent can change role."""
        # Stem cells can always differentiate
        if self.role == DifferentiatingAgent.STEM:
            return True
        # Committed cells cannot
        if self.commitment_level > 0.8:
            return False
        return True

    def differentiate_to(self, new_role):
        """
        Change to a new role.

        Inputs:
            new_role (str): Target role
        """
        if new_role in self.ALL_ROLES and self.can_differentiate():
            self.role = new_role
            self.differentiation_timer = 0
            self.commitment_level = 0.3

    def evaluate_differentiation(self):
        """
        Decide whether to differentiate based on local context.
        Implements lateral inhibition and signal response.

        Outputs:
            str or None: New role if differentiating, None otherwise
        """
        if not self.can_differentiate():
            return None

        # Need for each role based on local conditions
        need_scores = {}

        # LEADER: needed if no leader nearby
        if self.nearby_roles.get(DifferentiatingAgent.LEADER, 0) == 0:
            need_scores[DifferentiatingAgent.LEADER] = 0.8
        else:
            need_scores[DifferentiatingAgent.LEADER] = 0.0

        # WORKER: needed if few workers and tasks present
        worker_count = self.nearby_roles.get(DifferentiatingAgent.WORKER, 0)
        task_signal = self.sensed_signals.get('task', 0)
        need_scores[DifferentiatingAgent.WORKER] = min(1.0, task_signal) * (1.0 - worker_count / 5.0)

        # SCOUT: needed at edges, if no scouts nearby
        scout_count = self.nearby_roles.get(DifferentiatingAgent.SCOUT, 0)
        edge_signal = self.sensed_signals.get('edge', 0)
        need_scores[DifferentiatingAgent.SCOUT] = edge_signal * (1.0 if scout_count == 0 else 0.2)

        # GUARD: needed if threat signal present
        threat_signal = self.sensed_signals.get('threat', 0)
        guard_count = self.nearby_roles.get(DifferentiatingAgent.GUARD, 0)
        need_scores[DifferentiatingAgent.GUARD] = threat_signal * (1.0 - guard_count / 3.0)

        # Find highest need
        best_role = max(need_scores, key=need_scores.get)
        best_score = need_scores[best_role]

        # Differentiate if need is high enough
        if best_score > 0.5 and self.role == DifferentiatingAgent.STEM:
            return best_role

        # Possible redifferentiation if current role not needed
        if self.role != DifferentiatingAgent.STEM and self.commitment_level < 0.5:
            current_need = need_scores.get(self.role, 0)
            if current_need < 0.2 and best_score > 0.6:
                return best_role

        return None

    def execute_role_behavior(self):
        """
        Execute behavior specific to current role.

        Outputs:
            dict: Role-specific output
        """
        output = {'role': self.role, 'agent_id': self.id}

        if self.role == DifferentiatingAgent.LEADER:
            # Leader produces coordination signal
            self.signal_output = {'coordination': 1.0}
            output['action'] = 'coordinating'

        elif self.role == DifferentiatingAgent.WORKER:
            # Worker produces task output
            self.task_output += 1
            self.signal_output = {'busy': 0.5}
            output['action'] = 'working'

        elif self.role == DifferentiatingAgent.SCOUT:
            # Scout explores and reports
            self.signal_output = {'explored': 0.3}
            output['action'] = 'scouting'

        elif self.role == DifferentiatingAgent.GUARD:
            # Guard produces security
            self.signal_output = {'secure': 0.8}
            output['action'] = 'guarding'

        else:  # STEM
            # Stem waits and observes
            self.signal_output = {}
            output['action'] = 'waiting'

        # Increase commitment over time
        if self.role != DifferentiatingAgent.STEM:
            self.commitment_level = min(1.0, self.commitment_level + 0.05)

        return output

    def update(self, all_agents, environment):
        """
        Full update cycle: sense, differentiate, act.

        Inputs:
            all_agents (list): All agents
            environment: Environment object
        """
        self.sense_neighbors(all_agents)
        self.sense_signals(environment)

        new_role = self.evaluate_differentiation()
        if new_role:
            self.differentiate_to(new_role)

        return self.execute_role_behavior()

    def __repr__(self):
        return f"DifferentiatingAgent({self.id}, role={self.role}, commitment={self.commitment_level:.2f})"
