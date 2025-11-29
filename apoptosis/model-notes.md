# Apoptosis Model

## Agent Rules

### Self-Monitoring
- Agent tracks its own health metrics (error rate, response time, anomaly score)
- Agent maintains history of recent behavior
- Agent computes deviation from normal operation

### Self-Triggered Death
- If health drops below survival threshold → initiate apoptosis
- If anomaly score exceeds danger threshold → initiate apoptosis
- If marked by multiple neighbors → initiate apoptosis

### Neighbor Voting
- Agents can mark suspicious neighbors
- Marked agents have limited time to prove health
- Unanimous marking triggers forced apoptosis

## Environment Rules
- System maintains registry of active agents
- Dead agents are removed and can be replaced
- Environment tracks overall system health

## Activation Logic
```
# Self-monitoring
health_score = compute_health(error_rate, latency, anomaly_indicators)

# Check self-termination conditions
if health_score < survival_threshold:
    initiate_apoptosis("self-detected fault")
    return

# Check neighbor votes
marks_received = count_marks_from_neighbors()
if marks_received >= quorum_for_death:
    initiate_apoptosis("neighbor consensus")
    return

# Continue normal operation
perform_task()
```

## Mathematical Model
- Health score: `H = w1*(1-error_rate) + w2*(1-normalized_latency) + w3*conformity`
- Apoptosis trigger: `H < T_survival` OR `marks >= M_quorum`
- Mark decay: `marks(t+1) = marks(t) * decay_rate` (allows recovery)

## Key Parameters
- `survival_threshold`: Minimum health to continue operation
- `mark_quorum`: Number of marks needed for forced termination
- `mark_decay`: How quickly marks expire
- `observation_window`: Time period for health calculation
