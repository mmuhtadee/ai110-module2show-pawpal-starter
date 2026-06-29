import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pawpal_system import Task, Pet


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
