# Cell Differentiation Model

## Agent Rules

### Role Plasticity
- All agents start undifferentiated (stem state)
- Agents can differentiate into one of several roles
- Some roles allow de-differentiation back to stem
- Differentiation is triggered by local signals

### Signal Response
- Agents sense local concentrations of multiple signals
- Signal combinations determine differentiation path
- Threshold logic determines when to differentiate

### Role Behaviors
- Each role has specific behaviors and signal production
- Roles create feedback: role A produces signal that inhibits role A nearby
- This creates spacing and distribution of roles

## Environment Rules
- Multiple signal types diffuse through space
- Initial signal gradients may bias differentiation
- Signals decay and diffuse similar to morphogens

## Activation Logic
```
# Sense local signals
signal_a = environment.get_signal('A', position)
signal_b = environment.get_signal('B', position)
neighbor_roles = get_neighbor_roles()

# Differentiation decision tree
if self.role == STEM:
    if signal_a > threshold_a and count(neighbor_roles, LEADER) == 0:
        differentiate_to(LEADER)
    elif signal_b > threshold_b and count(neighbor_roles, WORKER) < 3:
        differentiate_to(WORKER)
    elif no_neighbors_of_role(SCOUT):
        differentiate_to(SCOUT)

# Role-specific behavior
execute_role_behavior()
```

## Mathematical Model
- Differentiation probability: `P(role) = f(signals, neighbor_roles)`
- Lateral inhibition: `P(role_A | neighbor_has_role_A) < P(role_A | no_neighbor_has_role_A)`
- Signal production: Each role produces specific signals that influence nearby cells

## Key Parameters
- `differentiation_thresholds`: Signal levels triggering each role
- `role_inhibition_radius`: Distance for lateral inhibition
- `plasticity_window`: Time during which differentiation is reversible
