# Swarm Flocking Model

## Agent Rules

### Separation
- Repel from neighbors within minimum distance
- Force inversely proportional to distance
- Prevents collisions

### Alignment
- Match velocity with neighbors within perception radius
- Steer toward average heading
- Creates coherent group motion

### Cohesion
- Steer toward center of mass of nearby neighbors
- Keeps flock together
- Prevents fragmentation

## Environment Rules
- Open 2D or 3D space with optional boundaries
- Boundaries can be reflective, wrapping, or repulsive
- No central coordination or communication infrastructure

## Activation Logic
```
neighbors = get_neighbors_within_radius(perception_radius)

# Separation: avoid crowding
separation_force = sum(
    (self.pos - neighbor.pos) / distance^2
    for neighbor in neighbors if distance < separation_radius
)

# Alignment: match heading
avg_velocity = mean(neighbor.velocity for neighbor in neighbors)
alignment_force = (avg_velocity - self.velocity) * alignment_weight

# Cohesion: move toward center
center_of_mass = mean(neighbor.pos for neighbor in neighbors)
cohesion_force = (center_of_mass - self.pos) * cohesion_weight

# Combine forces
acceleration = separation_force * w_sep + alignment_force * w_ali + cohesion_force * w_coh
velocity += acceleration
position += velocity
```

## Mathematical Model
- Velocity update: `v(t+1) = v(t) + Σ(w_i * F_i)`
- Position update: `p(t+1) = p(t) + v(t+1)`
- Speed clamped: `|v| ≤ v_max`
- Forces weighted by parameters: `w_sep, w_ali, w_coh`

## Key Parameters
- `perception_radius`: How far agent can see neighbors
- `separation_radius`: Minimum comfortable distance
- `w_sep, w_ali, w_coh`: Relative weights of three behaviors
- `max_speed`: Maximum velocity magnitude
- `max_force`: Maximum acceleration magnitude
