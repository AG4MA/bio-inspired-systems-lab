# model-notes.md

## Agent Rules
- Each agent communicates its state (e.g., presence of a signal) to its neighbors.
- Agents change their behavior based on the density of the signaling molecules in their environment.
- An agent will switch from a non-activated state to an activated state when the concentration of signaling molecules exceeds a defined threshold.

## Environment Rules
- The environment is a discrete grid where agents can occupy cells.
- Each cell can contain one or more agents and has a local concentration of signaling molecules.
- Signaling molecules diffuse through the environment, affecting neighboring agents.

## Activation Logic
- An agent checks the local concentration of signaling molecules during each time step.
- If the concentration exceeds the activation threshold, the agent activates and performs its designated behavior (e.g., aggregation, movement).
- Activated agents can also produce more signaling molecules, influencing nearby agents.

## Simplified Mathematical Model
- Let \( C \) be the concentration of signaling molecules in a cell.
- An agent activates if \( C > T \), where \( T \) is the activation threshold.
- The change in concentration over time can be modeled as:
  - \( C(t+1) = C(t) + D \cdot (C_{neighbors} - C(t)) \)
  - Where \( D \) is the diffusion rate and \( C_{neighbors} \) is the average concentration of neighboring cells.