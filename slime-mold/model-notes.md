# Slime Mold Pathfinding Model

## Agent Rules

### Exploration
- Agents (representing slime extensions) move outward from sources
- Movement is stochastic but biased toward unexplored areas
- Agents deposit pheromone trail as they move

### Trail Following
- Agents prefer paths with existing pheromone
- Higher pheromone = higher probability of following
- Creates positive feedback for good paths

### Path Pruning
- Trails with low traffic evaporate faster than they're reinforced
- Unused paths naturally disappear
- Network converges to efficient routes

## Environment Rules
- Graph or continuous space with obstacles
- Multiple food sources (destinations) to connect
- Pheromone field with deposition and evaporation

## Activation Logic
```
# Agent movement decision
if at_food_source:
    reinforcement_mode = True
    
if exploration_mode:
    # Random walk with pheromone bias
    directions = get_possible_directions()
    weights = [1 + pheromone[d] * bias_factor for d in directions]
    next_direction = weighted_random_choice(directions, weights)
    
if reinforcement_mode:
    # Backtrack to origin, reinforcing path
    deposit_pheromone(current_position, amount)
    move_toward_origin()

# Environment update
for each cell:
    pheromone[cell] *= (1 - evaporation_rate)
```

## Mathematical Model
- Pheromone update: `τ(t+1) = ρ * τ(t) + Δτ`
- Where `ρ` is retention rate, `Δτ` is new deposit
- Path probability: `P(path) ∝ τ^α` (α controls exploitation strength)
- Flow conservation at junctions

## Key Parameters
- `evaporation_rate`: How fast unused paths fade
- `deposition_amount`: Pheromone added per traversal
- `exploration_bias`: Random vs pheromone-guided movement
- `reinforcement_factor`: Bonus for successful paths
