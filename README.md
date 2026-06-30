# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
========================================
       TODAY'S SCHEDULE - PawPal+
========================================
Owner : Alex

  [Dog] Buddy
  ------------------------------
    08:00  |  Morning walk              |  Daily     |  [DONE]
    12:00  |  Lunch feeding             |  Daily     |  [PENDING]
    18:00  |  Evening walk              |  Daily     |  [PENDING]

  [Cat] Luna
  ------------------------------
    08:30  |  Breakfast                 |  Daily     |  [PENDING]
    12:00  |  Medication                |  Weekly    |  [PENDING]
    19:00  |  Dinner                    |  Daily     |  [PENDING]

========================================
Tasks sorted by time:
  08:00  Morning walk
  08:30  Breakfast
  12:00  Lunch feeding
  12:00  Medication
  18:00  Evening walk
  19:00  Dinner

Pending tasks : 5
Completed tasks: 1

Scheduling conflicts detected:
  12:00  ->  Lunch feeding, Medication
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns all tasks across all pets sorted chronologically by `"HH:MM"` string. Works correctly because lexicographic order matches time order for zero-padded 24-hour strings. |
| Filtering | `Scheduler.filter_by_status(status: bool)` | Pass `True` for completed tasks, `False` for pending. Returns a flat list across all pets. |
| Filtering | `Scheduler.filter_by_pet(pet_name: str)` | Returns only the tasks belonging to the named pet. Returns `[]` if the pet is not found. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups all tasks by their `"HH:MM"` time slot and returns a list of groups where two or more tasks share the exact same time. Returns `[]` if no conflicts exist. |
| Recurring tasks | `Task.frequency` (`"Daily"` / `"Weekly"`) | Frequency is stored on each `Task`. The next step is `Scheduler.complete_and_reschedule(pet, task)` to auto-generate the next occurrence when a recurring task is marked done. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
