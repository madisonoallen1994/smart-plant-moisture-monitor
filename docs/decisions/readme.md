# Architecture & Design Decisions

This folder contains **records of important technical and product decisions** made during the development of the Smart Plant Soil Moisture Monitoring System.

These documents exist to explain:
- Why certain approaches were chosen
- What alternatives were considered
- What tradeoffs were accepted

This helps preserve context over time and makes future changes easier and safer.

---

## What belongs in this folder

Decision documents should capture choices that:
- Affect system architecture
- Impact hardware or BLE design
- Influence data flow or interfaces
- Would be confusing without historical context

Examples include:
- Why BLE was chosen over other wireless options
- Why raw sensor values are forwarded instead of calibrated values
- Why a local hub is used instead of direct probe → backend communication

---

## What does NOT belong here

- Step-by-step instructions (those live in `runbooks/`)
- Product goals or requirements (those live in specs)
- Temporary experiments or sketches
- Code-level implementation details

This folder is about **reasoning**, not execution.

---

## How decisions should be written

Each decision document should ideally include:
- The problem or question being addressed
- Constraints and assumptions at the time
- Options that were considered
- The final decision
- Tradeoffs or known drawbacks
- Any follow-up or revisit criteria

The goal is clarity, not perfection.

---

## When to add a decision record

Add a decision document when:
- You are choosing between multiple viable options
- The decision may be questioned later
- The choice impacts more than one part of the system

If you find yourself explaining “why we did it this way” more than once, it probably belongs here.

---

## Relationship to the rest of the docs

- **Decisions** → explain *why* choices were made
- **Specs** → define *what* we are building
- **Runbooks** → explain *how* to run or debug the system
- **Execution plans** → explain *when* things happen

Together, these documents provide full project context.

---

## Future direction

As the project evolves:
- Some decisions may be revisited or superseded
- New decisions should be added rather than overwriting old ones
- Historical context should be preserved whenever possible

This folder acts as the project’s long-term memory.
