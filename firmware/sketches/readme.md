# Sketches (Exploratory & Experimental Code)

This folder contains **early-stage sketches and experimental code** created during prototyping and exploration.

Sketches are used to:
- Test individual ideas quickly
- Validate assumptions in isolation
- Explore libraries, APIs, or hardware behavior
- Iterate without affecting production or MVP code paths

This folder is intentionally flexible and informal.

---

## What this is

- Temporary or exploratory code
- Small experiments and throwaway prototypes
- Isolated tests that may not follow final architecture
- A sandbox for learning and validation

Sketches are allowed to be messy.

---

## What this is NOT

- Not production code
- Not the final firmware or hub implementation
- Not guaranteed to be complete, stable, or maintained
- Not expected to run end-to-end with the rest of the system

If something graduates beyond exploration, it should move out of this folder.

---

## Typical contents

Examples of what might live here:
- BLE scanning experiments
- Sensor read tests
- Timing or power experiments
- Library proof-of-concepts
- One-off scripts used during debugging

Each sketch should focus on a single idea or question.

---

## Relationship to the rest of the system

- **Sketches** (this folder) → exploration and learning
- **BLE GATT MVP** → validated BLE patterns
- **Firmware** → stable probe implementation
- **Hub** → BLE reading and HTTP forwarding
- **Backend stub** → local ingest during development

Sketches often inform later implementation but are not directly depended on.

---

## How to use this folder

- Feel free to experiment freely here
- Keep sketches small and focused
- Do not rely on sketches for core system behavior
- When a sketch proves useful, refactor and move it into the appropriate folder

This keeps the main codebase clean while preserving learning.

---

## Future direction

As the project matures:
- Some sketches may be deleted
- Some may be archived for reference
- Successful experiments should be promoted into `firmware/` or `hub/`

This folder exists to encourage fast iteration without fear.
