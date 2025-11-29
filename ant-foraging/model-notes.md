# Ant Foraging Model

## Agent (Ant) Rules

### Exploration Phase
- Ant starts at nest
- At each node, choose next node probabilistically based on pheromone and distance
- Probability: `P(edge) ∝ τ^α * η^β` where τ is pheromone, η is 1/distance
- Build path until food source reached or max steps exceeded

### Return Phase
- Once food found, ant returns to nest via same path
- Deposit pheromone on each edge traversed
- Amount deposited inversely proportional to path length
- Shorter paths = more pheromone per edge

### Memory
- Ant remembers visited nodes (tabu list)
- Avoids revisiting nodes in current trip
- Memory cleared when reaching food or nest

## Environment Rules
- Graph with nodes (nest, food, waypoints) and weighted edges
- Each edge has pheromone level and distance
- Pheromone evaporates each iteration: `τ(t+1) = ρ * τ(t)`
- All edges start with small initial pheromone

## Activation Logic
```
# Edge selection probability
def select_next_node(current, unvisited):
    weights = []
    for node in unvisited:
        tau = pheromone[current][node]
        eta = 1.0 / distance[current][node]
        weights.append((tau ** alpha) * (eta ** beta))
    return weighted_random_choice(unvisited, weights)

# Pheromone update after ant completes tour
def update_pheromone(path, path_length):
    deposit = Q / path_length
    for edge in path:
        pheromone[edge] += deposit
```

## Mathematical Model
- Selection: `P(i,j) = (τ_ij^α * η_ij^β) / Σ(τ_ik^α * η_ik^β)`
- Evaporation: `τ_ij(t+1) = (1-ρ) * τ_ij(t) + Δτ_ij`
- Deposit: `Δτ_ij = Q / L` if edge in best path, else 0

## Key Parameters
- `alpha`: Pheromone influence weight
- `beta`: Distance influence weight
- `rho`: Evaporation rate (0 < ρ < 1)
- `Q`: Pheromone deposit constant
- `num_ants`: Population size per iteration
