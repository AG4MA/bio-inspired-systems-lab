# Coupled Oscillators Model

## Agent (Oscillator) Rules

### Internal Phase
- Each oscillator has a phase φ ∈ [0, 1)
- Phase increases linearly: φ(t+dt) = φ(t) + ω*dt
- When φ reaches 1: fire (flash), reset to 0

### Pulse Coupling
- When oscillator fires, it sends a pulse to neighbors
- When oscillator receives a pulse, it adjusts its phase
- Phase response: φ_new = φ + Δφ(φ)
- Δφ typically positive near phase 1 (speed up when about to fire)

### Natural Frequency
- Each oscillator has natural frequency ω
- Frequencies can be identical or slightly varied
- Variation tests robustness of synchronization

## Environment Rules
- Oscillators connected in network
- Pulses propagate with optional delay
- No central coordinator or reference clock

## Activation Logic
```
# Each timestep
self.phase += self.frequency * dt

# Check for firing
if self.phase >= 1.0:
    self.fire()  # Send pulse to neighbors
    self.phase = 0.0

# When receiving pulse from neighbor
def receive_pulse():
    # Phase response curve (Kuramoto-style)
    adjustment = coupling_strength * sin(2 * pi * self.phase)
    self.phase += adjustment
    self.phase = self.phase % 1.0  # Keep in [0, 1)
```

## Mathematical Model (Kuramoto Model)
- Phase dynamics: `dφ_i/dt = ω_i + (K/N) * Σ sin(φ_j - φ_i)`
- Where K is coupling strength, N is number of neighbors
- Order parameter: `r = |1/N * Σ exp(i*φ_j)|` (r=1 is perfect sync)
- Critical coupling: `K_c ∝ spread(ω)` (minimum K for sync)

## Key Parameters
- `natural_frequency`: Base oscillation rate
- `coupling_strength`: How strongly pulses affect phase
- `frequency_spread`: Variation in natural frequencies
- `network_topology`: All-to-all, ring, random, etc.
