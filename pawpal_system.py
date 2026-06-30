from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str           # "HH:MM"
    frequency: str      # e.g. "Daily", "Weekly"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return the list of tasks assigned to this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted by their scheduled time (HH:MM)."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda task: task.time)

    def filter_by_status(self, status: bool) -> List[Task]:
        """Return tasks whose is_completed matches the given status."""
        return [task for task in self.owner.get_all_tasks() if task.is_completed == status]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to the pet with the given name, or [] if not found."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def detect_conflicts(self) -> List[List[Task]]:
        """Return groups of tasks scheduled at the exact same time."""
        time_map: dict[str, List[Task]] = {}
        for task in self.owner.get_all_tasks():
            time_map.setdefault(task.time, []).append(task)
        return [group for group in time_map.values() if len(group) > 1]
