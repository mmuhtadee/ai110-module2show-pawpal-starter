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
# Run the full test suite: python -m pytest
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0 -- /Users/munshatmuhtadee/ai110-module2show-pawpal-starter/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/munshatmuhtadee/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collecting ... collected 21 items

tests/test_pawpal.py::TestSortByTime::test_basic_reverse_order_becomes_ascending PASSED [  4%]
tests/test_pawpal.py::TestSortByTime::test_already_sorted_stays_the_same PASSED [  9%]
tests/test_pawpal.py::TestSortByTime::test_single_task_returns_one_element_list PASSED [ 14%]
tests/test_pawpal.py::TestSortByTime::test_no_tasks_returns_empty_list PASSED [ 19%]
tests/test_pawpal.py::TestSortByTime::test_tasks_interleaved_across_multiple_pets PASSED [ 23%]
tests/test_pawpal.py::TestSortByTime::test_midnight_boundary_sorts_correctly PASSED [ 28%]
tests/test_pawpal.py::TestSortByTime::test_all_tasks_at_same_time_all_present_in_result PASSED [ 33%]
tests/test_pawpal.py::TestRecurrenceLogic::test_daily_task_next_occurrence_is_tomorrow PASSED [ 38%]
tests/test_pawpal.py::TestRecurrenceLogic::test_daily_task_rolls_over_month_boundary PASSED [ 42%]
tests/test_pawpal.py::TestRecurrenceLogic::test_weekly_task_next_occurrence_is_seven_days_later PASSED [ 47%]
tests/test_pawpal.py::TestRecurrenceLogic::test_generate_next_occurrence_does_not_mutate_original PASSED [ 52%]
tests/test_pawpal.py::TestRecurrenceLogic::test_unsupported_frequency_raises_value_error PASSED [ 57%]
tests/test_pawpal.py::TestRecurrenceLogic::test_generate_next_occurrence_on_incomplete_task_still_works PASSED [ 61%]
tests/test_pawpal.py::TestDetectConflicts::test_no_conflicts_when_all_times_unique PASSED [ 66%]
tests/test_pawpal.py::TestDetectConflicts::test_single_task_no_conflict PASSED [ 71%]
tests/test_pawpal.py::TestDetectConflicts::test_no_tasks_returns_empty PASSED [ 76%]
tests/test_pawpal.py::TestDetectConflicts::test_two_tasks_same_time_flagged_as_one_conflict_group PASSED [ 80%]
tests/test_pawpal.py::TestDetectConflicts::test_three_tasks_same_time_one_group_of_three PASSED [ 85%]
tests/test_pawpal.py::TestDetectConflicts::test_two_separate_conflict_groups_both_returned PASSED [ 90%]
tests/test_pawpal.py::TestDetectConflicts::test_cross_pet_conflict_is_detected PASSED [ 95%]
tests/test_pawpal.py::TestDetectConflicts::test_completing_a_task_does_not_remove_it_from_conflict_detection PASSED [100%]

============================== 21 passed in 0.01s ==============================

Confidence level: 5/5
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

Follow these steps to explore every feature of PawPal+ from a fresh launch:

1. **Launch the app.** Run `streamlit run app.py` in your terminal. The browser opens to the PawPal+ home screen, which starts with a default owner ("Jordan") and one pet ("Mochi the Dog") already in session state so you have something to work with immediately.

2. **Add a second pet.** In the **Add a Pet** section, type a name (e.g. `Luna`) and select a species (`Cat`), then click **Add Pet**. A green success banner confirms the addition, and the "Current pets" line below updates to show both pets.

3. **Schedule tasks for your first pet.** In the **Add a Task** section, choose `Mochi` from the pet dropdown, enter a description (`Morning walk`), a time (`08:00`), and a frequency (`Daily`), then click **Add Task**. Repeat to add a second task — try `Lunch feeding` at `12:00`.

4. **Schedule tasks for your second pet.** Switch the pet dropdown to `Luna` and add a task at the same time as one of Mochi's tasks — for example, `Medication` at `12:00` with frequency `Weekly`. This deliberately creates a scheduling conflict you will see in the next step.

5. **Generate the schedule.** Scroll to the **Today's Schedule** section and click **Generate Schedule**. The table renders all tasks sorted chronologically by time across both pets, so `08:00` appears before `12:00` regardless of the order tasks were entered.

6. **Observe the conflict warning.** Because Mochi's `Lunch feeding` and Luna's `Medication` are both at `12:00`, a yellow `⚠️ Scheduling conflicts detected:` banner appears immediately below the table. It lists the conflicting time slot and the names of the clashing tasks so you know exactly what needs to be rescheduled.

7. **Resolve the conflict.** Add a replacement task for one of the conflicting pets at a different time (e.g. move `Medication` to `12:30`), then click **Generate Schedule** again. The warning disappears and a green `✅ No conflicts detected.` message confirms the schedule is clean.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
