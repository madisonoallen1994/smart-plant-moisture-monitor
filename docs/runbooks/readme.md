# Runbooks

This folder contains **runbooks** — practical, step-by-step guides for running, testing, and troubleshooting the Smart Plant Soil Moisture Monitoring System.

Runbooks are intended to be used:
- During hands-on development
- On hardware day
- When something breaks and needs to be fixed quickly

They prioritize clarity and action over background or theory.

---

## What belongs in this folder

Runbooks should include:
- Setup commands
- Environment configuration steps
- Validation checklists
- Troubleshooting flows
- Known failure modes and recovery steps

They should be safe to follow even under time pressure.

---

## What does NOT belong here

- Product goals or requirements
- Design rationale or architectural decisions
- High-level system descriptions
- Exploratory notes or experiments

Those belong in specs, decisions, or sketches.

---

## How to use runbooks

- Follow runbooks **top to bottom**
- Execute commands exactly as written
- Use troubleshooting sections when a step fails
- Do not skip steps unless explicitly instructed

Runbooks assume minimal context and should be self-contained.

---

## Key runbooks

The most important runbook during early development is:

`hardware_day_quick_start.md`

This runbook covers:
- Local environment setup
- Running the hub and backend stub
- BLE discovery and validation
- macOS-specific BLE troubleshooting
- End-to-end flow verification

If you are setting up hardware or debugging BLE issues, start there.

---

## Writing and updating runbooks

When adding or updating runbooks:
- Use clear, imperative language
- Prefer numbered steps where order matters
- Keep sections short and scannable
- Update runbooks as soon as behavior changes

Runbooks should reflect the **current state of the system**, not an idealized future.

---

## Relationship to the rest of the docs

- **Runbooks** → how to run and debug
- **Specs** → what we are building
- **Decisions** → why choices were made
- **Diagrams** → visual explanations

Together, these form a complete documentation set.

---

## Future direction

As the project evolves, this folder may include:
- Additional hardware setup guides
- Calibration runbooks
- Deployment or migration guides

Runbooks should always remain practical and up to date.
