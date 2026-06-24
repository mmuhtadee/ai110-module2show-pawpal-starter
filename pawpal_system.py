from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple, Optional

@dataclass
class Task:
    name: str
    task_type: str
    scheduled_time: datetime
    frequency: str
    status: str = "pending"
    duration_minutes: int = 30
    notes: str = ""

    def mark_complete(self) -> None:
        """Sets status to 'completed' and handles recurrence."""
        pass

    def mark_skipped(self) -> None:
        """Sets status to 'skipped'."""
        pass

    def reschedule(self, new_time: datetime) -> None:
        """Updates the scheduled_time."""
        pass

    def is_overdue(self) -> bool:
        """Returns True if scheduled_time has passed and status is pending."""
        return False

@dataclass
class Pet:
    name: str
    breed: str
    age: int
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attaches a task to this pet."""
        pass

    def remove_task(self, task_name: str) -> None:
        """Removes a task by name."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Returns tasks not yet completed."""
        return []

    def get_task_by_type(self, task_type: str) -> List[Task]:
        """Filters tasks by type."""
        return []

@dataclass
class Owner:
    name: str
    email: str
    phone: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's list."""
        pass

    def remove_pet(self, pet_name: str) -> None:
        """Removes a pet by name."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks across all owned pets."""
        return []

    def view_schedule(self) -> None:
        """Displays the full schedule for all pets."""
        pass

class Scheduler:
    def __init__(self):
        self.owners: List[Owner] = []
        self.task_queue: List[Tuple[Pet, Task]] = []

    def load_tasks(self, owner: Owner) -> None:
        """Pulls all tasks from an owner's pets into the queue."""
        pass

    def sort_by_time(self) -> None:
        """Sorts task_queue by scheduled_time ascending."""
        pass

    def get_upcoming_tasks(self, hours: int) -> List[Task]:
        """Returns tasks due within the next N hours."""
        return []

    def send_reminders(self) -> None:
        """Triggers notifications for overdue or imminent tasks."""
        pass

    def generate_daily_summary(self, owner: Owner) -> str:
        """Produces a summary of the day's tasks."""
        return ""