# Chemotaxis Model

## Agent Rules
- Agent moves in current direction for a "run" period
- After each run, agent samples local concentration
- If concentration increased: continue direction (longer run)
- If concentration decreased: tumble (pick new random direction)
- Run duration is proportional to improvement rate

## Environment Rules
- Environment contains a scalar concentration field
- Concentration typically follows gradient toward source(s)
- Field may be static or dynamic
- Noise can be added to simulate real-world uncertainty

## Activation Logic
```
current_concentration = sense()
improvement = current_concentration - previous_concentration

if improvement > 0:
    # Good direction: extend run duration
    run_duration = base_duration * (1 + improvement * sensitivity)
    continue_direction()
else:
    # Bad direction: tumble to new random direction
    tumble()
    run_duration = base_duration

previous_concentration = current_concentration
```

## Mathematical Model
- Position update: `x(t+1) = x(t) + v * direction`
- Tumble probability: `P_tumble = 1 / (1 + exp(k * improvement))`
- Run length: `L = L_base * exp(α * dC/dt)`
- Where dC/dt is the temporal derivative of concentration

## Key Parameters
- `run_duration`: Base time between direction changes
- `tumble_angle`: Range of random angle change during tumble
- `sensitivity`: How strongly improvement affects run duration
- `speed`: Agent movement speed
