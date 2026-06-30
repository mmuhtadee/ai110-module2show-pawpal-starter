import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_sets_flag_to_true():
    task = Task(description="Morning walk", time="08:00", frequency="Daily")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(description="Feeding", time="12:00", frequency="Daily"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(Task(description="Evening walk", time="18:00", frequency="Daily"))
    assert len(pet.get_tasks()) == 2


# ---------------------------------------------------------------------------
# Sorting tests
# ---------------------------------------------------------------------------

def _make_scheduler(*time_strings):
    """Helper: build a Scheduler with one pet whose tasks have the given times."""
    owner = Owner(name="TestOwner")
    pet = Pet(name="TestPet", species="Dog")
    for i, t in enumerate(time_strings):
        pet.add_task(Task(description=f"Task{i}", time=t, frequency="Daily"))
    owner.add_pet(pet)
    return Scheduler(owner)


def test_sort_by_time_returns_chronological_order():
    scheduler = _make_scheduler("18:00", "08:00", "12:00")
    sorted_tasks = scheduler.sort_by_time()
    times = [task.time for task in sorted_tasks]
    assert times == ["08:00", "12:00", "18:00"]


def test_sort_by_time_already_sorted_unchanged():
    scheduler = _make_scheduler("07:00", "09:30", "14:00", "21:00")
    sorted_tasks = scheduler.sort_by_time()
    times = [task.time for task in sorted_tasks]
    assert times == ["07:00", "09:30", "14:00", "21:00"]


def test_sort_by_time_single_task():
    scheduler = _make_scheduler("10:00")
    sorted_tasks = scheduler.sort_by_time()
    assert len(sorted_tasks) == 1
    assert sorted_tasks[0].time == "10:00"


def test_sort_by_time_across_multiple_pets():
    owner = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    dog.add_task(Task(description="Evening walk", time="18:00", frequency="Daily"))
    dog.add_task(Task(description="Morning walk", time="08:00", frequency="Daily"))
    cat.add_task(Task(description="Breakfast",    time="08:30", frequency="Daily"))
    cat.add_task(Task(description="Dinner",       time="19:00", frequency="Daily"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)
    times = [t.time for t in scheduler.sort_by_time()]
    assert times == ["08:00", "08:30", "18:00", "19:00"]


# ---------------------------------------------------------------------------
# Conflict detection tests
# ---------------------------------------------------------------------------

def test_detect_conflicts_finds_duplicate_time():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="Feeding",  time="12:00", frequency="Daily"))
    pet.add_task(Task(description="Medicine", time="12:00", frequency="Weekly"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert len(conflicts[0]) == 2


def test_detect_conflicts_none_when_all_unique():
    scheduler = _make_scheduler("08:00", "12:00", "18:00")
    conflicts = scheduler.detect_conflicts()
    assert conflicts == []


def test_detect_conflicts_across_pets():
    owner = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna",  species="Cat")
    dog.add_task(Task(description="Walk",       time="09:00", frequency="Daily"))
    cat.add_task(Task(description="Medication", time="09:00", frequency="Weekly"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    conflict_times = {t.time for t in conflicts[0]}
    assert conflict_times == {"09:00"}


def test_detect_conflicts_multiple_conflict_groups():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="A", time="08:00", frequency="Daily"))
    pet.add_task(Task(description="B", time="08:00", frequency="Daily"))
    pet.add_task(Task(description="C", time="12:00", frequency="Daily"))
    pet.add_task(Task(description="D", time="12:00", frequency="Daily"))
    pet.add_task(Task(description="E", time="15:00", frequency="Daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 2


def test_detect_conflicts_three_tasks_same_slot():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", species="Dog")
    for desc in ("Feed", "Walk", "Groom"):
        pet.add_task(Task(description=desc, time="10:00", frequency="Daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert len(conflicts[0]) == 3
