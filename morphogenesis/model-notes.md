# Morphogenesis Model

## Agent/Cell Rules

### Chemical Production
- Each cell produces two morphogens: activator (A) and inhibitor (B)
- Production rates depend on local concentrations
- A activates production of both A and B
- B inhibits production of A

### Diffusion
- Both chemicals diffuse to neighboring cells
- Inhibitor diffuses faster than activator
- This difference in diffusion rates is key to pattern formation

### Concentration Update
- Cells update their concentrations each timestep
- Reaction + diffusion dynamics create instabilities
- Instabilities grow into stable patterns

## Environment Rules
- 2D grid of cells
- Each cell has (A, B) concentration values
- Boundary conditions (periodic, fixed, or reflective)

## Activation Logic (Turing's Reaction-Diffusion)
```
# For each cell, at each timestep:
dA = D_a * laplacian(A) + f(A, B)
dB = D_b * laplacian(B) + g(A, B)

A_new = A + dA * dt
B_new = B + dB * dt

# Common reaction functions (Gierer-Meinhardt model):
f(A, B) = a - b*A + (A^2 / B)  # Activator dynamics
g(A, B) = A^2 - B               # Inhibitor dynamics
```

## Mathematical Model
- Activator: `∂A/∂t = D_a ∇²A + ρ_a * A²/B - μ_a * A + σ_a`
- Inhibitor: `∂B/∂t = D_b ∇²B + ρ_b * A² - μ_b * B`
- Key condition: `D_b >> D_a` (inhibitor diffuses faster)

## Key Parameters
- `D_a, D_b`: Diffusion rates (D_b > D_a)
- `ρ_a, ρ_b`: Production rates
- `μ_a, μ_b`: Decay rates
- `dt`: Time step size
- `noise`: Initial perturbation amplitude
