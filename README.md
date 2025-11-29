# Bio-Inspired Systems Lab — Global Agent Context

## Purpose of the Repository
This repository is a conceptual and experimental lab where each folder contains:
- a biological phenomenon
- an abstraction into system rules (agents, interactions, thresholds)
- a minimal technical implementation (Python / C# / TS)
- insights for software architecture, distributed systems, AI, robotics, or
  complex adaptive systems.

The repo is not meant to build real biology or hardware.  
Its purpose is to **inspire software design** through models derived from nature.

## Structure Overview
Each module must contain:
- `README.md` → biological description + high-level analogy
- `model-notes.md` → abstract rules and simplified mathematical model
- `insights.md` → reflections for system design
- `src/` → minimal code implementation (simulation or prototype)

## Design Principles
Agents must:
- generate concise, high-quality technical files
- keep all documentation in English
- avoid long boilerplate unless required
- ensure code readability and clear comments
- maintain modularity (each biological phenomenon is independent)

## Coding Rules
- All code must be written in English.
- Variable names must be meaningful.
- Each function requires:
  - a top-level header comment (purpose, inputs, outputs)
  - inline comments for key steps
- Follow good software engineering practices:
  - single responsibility
  - small units
  - unit tests when meaningful

## Scope of the Project
Agents should focus on:
- translating biological concepts into system abstractions
- designing small, elegant simulations
- highlighting emergent behavior
- keeping modules lightweight and educational
- enabling cross-pollination between biology-inspired logic and engineering

## Non-Goals
Agents must **not**:
- write actual drone control firmware
- simulate biology with high fidelity
- produce unnecessary complexity
- introduce long scientific essays
- diverge into non-technical or non-conceptual biological commentary

## Module Template (Agents Must Reproduce It)
Each new module created by an agent must follow:

phenomenon-name/
README.md
model-notes.md
insights.md
src/
<demo_code_file>


README must include:
- biological summary (max 8–12 lines)
- why the phenomenon matters in complex systems
- its relevance to distributed software or AI

model-notes.md must include:
- agent rules
- environment rules
- activation logic
- simplified math when relevant

insights.md must include:
- emergent patterns
- architectural parallels
- what this phenomenon teaches about designing robust systems

## Tone Requirements
Agents must:
- be concise
- avoid emojis or informal slang
- produce high-value conceptual clarity
- maintain professional, minimal style
- use examples only when necessary

## Output Requirements for Agents
Whenever an agent generates files:
- output **clean Markdown only**
- generate **runnable code**
- keep directories exactly as defined
- avoid mixing languages in the same module

## Current Modules
- `quorum-sensing/` — Density-dependent collective behavior
- `chemotaxis/` — Gradient-following exploration
- `swarm-flocking/` — Reynolds rules for coordinated motion
- `apoptosis/` — Self-elimination of faulty agents
- `cell-differentiation/` — Dynamic role assignment from identical agents
- `slime-mold/` — Decentralized pathfinding networks
- `morphogenesis/` — Turing patterns and emergent structures
- `symmetry-breaking/` — Spontaneous leader election
- `ant-foraging/` — Pheromone-based optimization
- `coupled-oscillators/` — Firefly synchronization

## Overall Vision
This repository is an exploration of how biological systems:
- coordinate
- adapt
- maintain stability
- self-organize
- generate emergent complexity

And how these patterns can inspire software architecture, agent systems,
distributed intelligence, and next-generation computational frameworks.

Agents must preserve and reinforce this direction with every contribution.
