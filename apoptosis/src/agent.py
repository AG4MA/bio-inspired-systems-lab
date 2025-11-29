# agent.py
# Purpose: Agent with self-monitoring and apoptosis (self-termination) capability
# Implements health tracking and peer voting for fault tolerance

import random


class ApoptosisAgent:
    """
    Agent capable of programmed self-destruction when faulty.
    Monitors own health and responds to neighbor marks.
    """

    # Agent states
    ALIVE = 'alive'
    APOPTOTIC = 'apoptotic'
    DEAD = 'dead'

    def __init__(self, agent_id, survival_threshold=0.3, mark_quorum=3):
        """
        Initialize an apoptosis-capable agent.

        Inputs:
            agent_id (int): Unique identifier
            survival_threshold (float): Minimum health to stay alive
            mark_quorum (int): Number of marks needed for forced death
        """
        self.id = agent_id
        self.survival_threshold = survival_threshold
        self.mark_quorum = mark_quorum

        # State
        self.state = ApoptosisAgent.ALIVE
        self.health = 1.0

        # Health components
        self.error_rate = 0.0
        self.latency = 0.0
        self.anomaly_score = 0.0

        # Marks from neighbors
        self.marks = 0
        self.mark_decay = 0.9

        # Death reason (for logging)
        self.death_reason = None

        # History for anomaly detection
        self.recent_errors = []
        self.window_size = 10

    def compute_health(self):
        """
        Calculate overall health score from components.

        Outputs:
            float: Health score between 0 and 1
        """
        # Weighted combination of factors
        w_error = 0.4
        w_latency = 0.3
        w_anomaly = 0.3

        health = (
            w_error * (1.0 - min(1.0, self.error_rate)) +
            w_latency * (1.0 - min(1.0, self.latency)) +
            w_anomaly * (1.0 - min(1.0, self.anomaly_score))
        )

        self.health = max(0.0, min(1.0, health))
        return self.health

    def simulate_operation(self, failure_probability=0.1):
        """
        Simulate agent performing a task with possible failures.

        Inputs:
            failure_probability (float): Chance of error per operation

        Outputs:
            bool: True if operation succeeded
        """
        if self.state != ApoptosisAgent.ALIVE:
            return False

        # Simulate potential failure
        error_occurred = random.random() < failure_probability
        self.recent_errors.append(1 if error_occurred else 0)

        # Keep only recent history
        if len(self.recent_errors) > self.window_size:
            self.recent_errors.pop(0)

        # Update error rate from recent history
        if self.recent_errors:
            self.error_rate = sum(self.recent_errors) / len(self.recent_errors)

        # Simulate latency (random with occasional spikes)
        self.latency = random.uniform(0, 0.3)
        if random.random() < 0.05:
            self.latency = random.uniform(0.5, 1.0)

        # Update anomaly score (increases if behaving erratically)
        if error_occurred or self.latency > 0.5:
            self.anomaly_score = min(1.0, self.anomaly_score + 0.1)
        else:
            self.anomaly_score = max(0.0, self.anomaly_score - 0.05)

        return not error_occurred

    def receive_mark(self):
        """Receive a suspicious mark from a neighbor."""
        self.marks += 1

    def decay_marks(self):
        """Apply decay to accumulated marks."""
        self.marks = int(self.marks * self.mark_decay)

    def check_apoptosis(self):
        """
        Check if apoptosis should be triggered.

        Outputs:
            bool: True if agent should die
        """
        if self.state != ApoptosisAgent.ALIVE:
            return False

        # Compute current health
        self.compute_health()

        # Check self-triggered death
        if self.health < self.survival_threshold:
            self.initiate_apoptosis("self-detected low health")
            return True

        # Check neighbor consensus death
        if self.marks >= self.mark_quorum:
            self.initiate_apoptosis("neighbor consensus")
            return True

        return False

    def initiate_apoptosis(self, reason):
        """
        Begin controlled self-destruction.

        Inputs:
            reason (str): Why apoptosis was triggered
        """
        self.state = ApoptosisAgent.APOPTOTIC
        self.death_reason = reason
        # In real system: drain connections, flush data, notify neighbors

    def complete_death(self):
        """Finalize death after apoptotic cleanup."""
        self.state = ApoptosisAgent.DEAD

    def is_alive(self):
        """Check if agent is still alive."""
        return self.state == ApoptosisAgent.ALIVE

    def observe_neighbor(self, neighbor):
        """
        Observe a neighbor and potentially mark them as suspicious.

        Inputs:
            neighbor (ApoptosisAgent): Neighbor to observe

        Outputs:
            bool: True if neighbor was marked
        """
        if not neighbor.is_alive() or not self.is_alive():
            return False

        # Mark if neighbor appears unhealthy
        if neighbor.health < 0.4 or neighbor.error_rate > 0.5:
            neighbor.receive_mark()
            return True

        return False

    def __repr__(self):
        return f"ApoptosisAgent({self.id}, state={self.state}, health={self.health:.2f})"
