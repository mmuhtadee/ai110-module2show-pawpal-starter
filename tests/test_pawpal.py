"""
Phase 5 – Step 1: Automated test suite for the PawPal scheduler.

Covers three pillars:
  1. Sorting correctness  – tasks come back in exact HH:MM chronological order
  2. Recurrence logic     – marking a Daily task complete produces the next instance
  3. Conflict detection   – Scheduler.detect_conflicts() flags duplicate time slots
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def make_scheduler(*time_strings: str) -> Scheduler:
    """Build a Scheduler with one pet whose tasks have the given times."""
    owner = Owner(name="TestOwner")
    pet = Pet(name="TestPet", species="Dog")
    for i, t in enumerate(time_strings):
        pet.add_task(Task(description=f"Task{i}", time=t, frequency="Daily"))
    owner.add_pet(pet)
    return Scheduler(owner)


# ===========================================================================
# 1. SORTING CORRECTNESS
# ===========================================================================

class TestSortByTime:

    def test_basic_reverse_order_becomes_ascending(self):
        """Tasks added latest-first must come out earliest-first."""
        scheduler = make_scheduler("18:00", "08:00", "12:00")
        times = [t.time for t in scheduler.sort_by_time()]
        assert times == ["08:00", "12:00", "18:00"]

    def test_already_sorted_stays_the_same(self):
        """An already-ascending list must not be re-ordered."""
        scheduler = make_scheduler("07:00", "09:30", "14:00", "21:00")
        times = [t.time for t in scheduler.sort_by_time()]
        assert times == ["07:00", "09:30", "14:00", "21:00"]

    def test_single_task_returns_one_element_list(self):
        scheduler = make_scheduler("10:00")
        result = scheduler.sort_by_time()
        assert len(result) == 1
        assert result[0].time == "10:00"

    def test_no_tasks_returns_empty_list(self):
        owner = Owner(name="EmptyOwner")
        scheduler = Scheduler(owner)
        assert scheduler.sort_by_time() == []

    def test_tasks_interleaved_across_multiple_pets(self):
        """Tasks from different pets must be merged and sorted together."""
        owner = Owner(name="Alex")
        dog = Pet(name="Buddy", species="Dog")
        cat = Pet(name="Luna", species="Cat")

        dog.add_task(Task(description="Evening walk", time="18:00", frequency="Daily"))
        dog.add_task(Task(description="Morning walk", time="08:00", frequency="Daily"))
        cat.add_task(Task(description="Breakfast",    time="08:30", frequency="Daily"))
        cat.add_task(Task(description="Dinner",       time="19:00", frequency="Daily"))

        owner.add_pet(dog)
        owner.add_pet(cat)
        times = [t.time for t in Scheduler(owner).sort_by_time()]
        assert times == ["08:00", "08:30", "18:00", "19:00"]

    def test_midnight_boundary_sorts_correctly(self):
        """'00:00' must sort before '01:00' and after '23:59'."""
        scheduler = make_scheduler("23:59", "00:00", "01:00")
        times = [t.time for t in scheduler.sort_by_time()]
        assert times == ["00:00", "01:00", "23:59"]

    def test_all_tasks_at_same_time_all_present_in_result(self):
        """Ties are allowed; all tied tasks must still appear in the output."""
        scheduler = make_scheduler("09:00", "09:00", "09:00")
        result = scheduler.sort_by_time()
        assert len(result) == 3
        assert all(t.time == "09:00" for t in result)


# ===========================================================================
# 2. RECURRENCE LOGIC
#
# NOTE: Task.generate_next_occurrence() does not exist yet.
# These tests are written TDD-style — they will FAIL until you implement
# the method in pawpal_system.py.
#
# Expected contract:
#   task.generate_next_occurrence(current_date: str) -> Task
#     current_date format: "YYYY-MM-DD"
#     Returns a NEW Task with is_completed=False and a date one period later.
#     Raises ValueError for an unsupported frequency string.
# ===========================================================================

class TestRecurrenceLogic:

    def test_daily_task_next_occurrence_is_tomorrow(self):
        """Marking a Daily task done and calling generate_next_occurrence
        must produce a new incomplete task dated one day later."""
        task = Task(description="Morning walk", time="08:00", frequency="Daily")
        task.mark_complete()

        next_task = task.generate_next_occurrence(current_date="2026-06-29")

        assert next_task.is_completed is False
        assert next_task.description == "Morning walk"
        assert next_task.time == "08:00"
        assert next_task.frequency == "Daily"
        # The next occurrence must be exactly one calendar day later.
        assert next_task.date == "2026-06-30"

    def test_daily_task_rolls_over_month_boundary(self):
        """A Daily task on the last day of the month must roll into the next month."""
        task = Task(description="Evening feed", time="18:00", frequency="Daily")
        task.mark_complete()

        next_task = task.generate_next_occurrence(current_date="2026-06-30")
        assert next_task.date == "2026-07-01"

    def test_weekly_task_next_occurrence_is_seven_days_later(self):
        """A Weekly task must schedule exactly 7 days out."""
        task = Task(description="Bath time", time="11:00", frequency="Weekly")
        task.mark_complete()

        next_task = task.generate_next_occurrence(current_date="2026-06-29")
        assert next_task.date == "2026-07-06"

    def test_generate_next_occurrence_does_not_mutate_original(self):
        """The original task must remain completed and unchanged after generating next."""
        task = Task(description="Feeding", time="07:00", frequency="Daily")
        task.mark_complete()

        task.generate_next_occurrence(current_date="2026-06-29")

        assert task.is_completed is True
        assert task.description == "Feeding"

    def test_unsupported_frequency_raises_value_error(self):
        """An unrecognised frequency string must raise ValueError, not silently fail."""
        task = Task(description="Odd task", time="10:00", frequency="Hourly")
        task.mark_complete()

        with pytest.raises(ValueError):
            task.generate_next_occurrence(current_date="2026-06-29")

    def test_generate_next_occurrence_on_incomplete_task_still_works(self):
        """generate_next_occurrence should work even if the task is not yet marked done,
        because the scheduler may call it proactively."""
        task = Task(description="Medication", time="09:00", frequency="Daily")
        # do NOT call mark_complete()
        next_task = task.generate_next_occurrence(current_date="2026-06-29")
        assert next_task.date == "2026-06-30"


# ===========================================================================
# 3. CONFLICT DETECTION
# ===========================================================================

class TestDetectConflicts:

    def test_no_conflicts_when_all_times_unique(self):
        scheduler = make_scheduler("08:00", "12:00", "18:00")
        assert scheduler.detect_conflicts() == []

    def test_single_task_no_conflict(self):
        scheduler = make_scheduler("10:00")
        assert scheduler.detect_conflicts() == []

    def test_no_tasks_returns_empty(self):
        owner = Owner(name="EmptyOwner")
        assert Scheduler(owner).detect_conflicts() == []

    def test_two_tasks_same_time_flagged_as_one_conflict_group(self):
        owner = Owner(name="Alex")
        pet = Pet(name="Buddy", species="Dog")
        pet.add_task(Task(description="Feeding",  time="12:00", frequency="Daily"))
        pet.add_task(Task(description="Medicine", time="12:00", frequency="Weekly"))
        owner.add_pet(pet)

        conflicts = Scheduler(owner).detect_conflicts()

        assert len(conflicts) == 1
        assert len(conflicts[0]) == 2
        assert all(t.time == "12:00" for t in conflicts[0])

    def test_three_tasks_same_time_one_group_of_three(self):
        owner = Owner(name="Alex")
        pet = Pet(name="Buddy", species="Dog")
        for desc in ("Feed", "Walk", "Groom"):
            pet.add_task(Task(description=desc, time="10:00", frequency="Daily"))
        owner.add_pet(pet)

        conflicts = Scheduler(owner).detect_conflicts()

        assert len(conflicts) == 1
        assert len(conflicts[0]) == 3

    def test_two_separate_conflict_groups_both_returned(self):
        owner = Owner(name="Alex")
        pet = Pet(name="Buddy", species="Dog")
        pet.add_task(Task(description="A", time="08:00", frequency="Daily"))
        pet.add_task(Task(description="B", time="08:00", frequency="Daily"))
        pet.add_task(Task(description="C", time="14:00", frequency="Daily"))
        pet.add_task(Task(description="D", time="14:00", frequency="Daily"))
        pet.add_task(Task(description="E", time="18:00", frequency="Daily"))  # no conflict
        owner.add_pet(pet)

        conflicts = Scheduler(owner).detect_conflicts()
        conflict_times = sorted({t.time for group in conflicts for t in group})

        assert len(conflicts) == 2
        assert conflict_times == ["08:00", "14:00"]

    def test_cross_pet_conflict_is_detected(self):
        """The most critical real-world case: two different pets scheduled at the same time."""
        owner = Owner(name="Alex")
        dog = Pet(name="Buddy", species="Dog")
        cat = Pet(name="Luna",  species="Cat")
        dog.add_task(Task(description="Walk",       time="09:00", frequency="Daily"))
        cat.add_task(Task(description="Medication", time="09:00", frequency="Weekly"))
        owner.add_pet(dog)
        owner.add_pet(cat)

        conflicts = Scheduler(owner).detect_conflicts()

        assert len(conflicts) == 1
        assert len(conflicts[0]) == 2
        descriptions = {t.description for t in conflicts[0]}
        assert descriptions == {"Walk", "Medication"}

    def test_completing_a_task_does_not_remove_it_from_conflict_detection(self):
        """A completed task is still scheduled at that time and must still flag a conflict."""
        owner = Owner(name="Alex")
        pet = Pet(name="Buddy", species="Dog")
        t1 = Task(description="Feeding",  time="12:00", frequency="Daily")
        t2 = Task(description="Medicine", time="12:00", frequency="Daily")
        t1.mark_complete()
        pet.add_task(t1)
        pet.add_task(t2)
        owner.add_pet(pet)

        conflicts = Scheduler(owner).detect_conflicts()
        assert len(conflicts) == 1
