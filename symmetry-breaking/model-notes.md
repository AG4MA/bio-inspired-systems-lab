# Symmetry Breaking Model

## Agent Rules

### Initial State
- All agents start with identical state (symmetric)
- Each agent has a "commitment" value, initially small random noise
- Agents observe neighbors' commitment levels

### Amplification
- Agents adjust their commitment based on local environment
- If own commitment > neighbors' average → increase commitment
- If own commitment < neighbors' average → decrease commitment
- Small initial differences get amplified

### Saturation
- Commitment has maximum value (1.0)
- Once near saturation, agent is "committed" to role/direction
- Creates bistable system: most agents end up at 0 or 1

## Environment Rules
- Agents connected in network (ring, grid, or random)
- Communication is local (neighbors only)
- No global broadcast or central coordinator

## Activation Logic
```
# Each timestep
neighbor_avg = mean(neighbor.commitment for neighbor in neighbors)

# Positive feedback: difference from neighbors amplified
delta = (self.commitment - neighbor_avg) * amplification_rate

# Small random perturbation
delta += random_noise * noise_amplitude

# Update with bounds
self.commitment = clamp(self.commitment + delta, 0, 1)

# Check for symmetry break
if self.commitment > 0.9:
    self.role = LEADER
elif self.commitment < 0.1:
    self.role = FOLLOWER
```

## Mathematical Model
- Dynamics: `dc/dt = α * (c - c_avg) + σ * ξ(t)`
- Where α is amplification rate, σ is noise, ξ is random
- Bistable potential: `V(c) = -c²/2 + c⁴/4` (double well)
- Time to break symmetry: `τ ∝ 1/σ * exp(ΔV/σ²)`

## Key Parameters
- `amplification_rate`: How fast differences grow
- `noise_amplitude`: Random perturbation strength
- `neighbor_count`: Number of neighbors to compare with
- `commitment_threshold`: Level considered "decided"
