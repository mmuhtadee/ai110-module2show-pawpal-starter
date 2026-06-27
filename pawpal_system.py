from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

@dataclass
class Task:
    name: str
    task_type: str  # e.g., "walk", "feeding", "medication"
    scheduled_time: datetime
    frequency: str  # "once", "daily", "weekly"
    status: str = "pending"  # "pending", "completed", "skipped"
    duration_minutes: int = 30
    notes: str = ""

    def mark_complete(self) -> Optional['Task']:
        """Sets status to 'completed' and returns a new recurring Task if applicable."""
        self.status = "completed"
        if self.frequency == "daily":
            return Task(
                name=self.name,
                task_type=self.task_type,
                scheduled_time=self.scheduled_time + timedelta(days=1),
                frequency=self.frequency,
                status="pending",
                duration_minutes=self.duration_minutes,
                notes=self.notes
            )
        elif self.frequency == "weekly":
            return Task(
                name=self.name,
                task_type=self.task_type,
                scheduled_time=self.scheduled_time + timedelta(weeks=1),
                frequency=self.frequency,
                status="pending",
                duration_minutes=self.duration_minutes,
                notes=self.notes
            )
        return None

    def mark_skipped(self) -> None:
        """Sets status to 'skipped'."""
        self.status = "skipped"

    def reschedule(self, new_time: datetime) -> None:
        """Updates the scheduled_time."""
        self.scheduled_time = new_time

    def is_overdue(self) -> bool:
        """Returns True if scheduled_time has passed and status is pending."""
        return datetime.now() > self.scheduled_time and self.status == "pending"

@dataclass
class Pet:
    name: str
    breed: str
    age: int
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attaches a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Removes a task by name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_pending_tasks(self) -> List[Task]:
        """Returns tasks not yet completed."""
        return [t for t in self.tasks if t.status == "pending"]

    def get_task_by_type(self, task_type: str) -> List[Task]:
        """Filters tasks by type."""
        return [t for t in self.tasks if t.task_type.lower() == task_type.lower()]

@dataclass
class Owner:
    name: str
    email: str
    phone: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Removes a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def view_schedule(self) -> None:
        """Prints the full schedule for all pets to console."""
        for pet in self.pets:
            print(f"\n--- {pet.name}'s Schedule ---")
            for task in pet.tasks:
                print(f"[{task.status.upper()}] {task.name} at {task.scheduled_time.strftime('%H:%M')} ({task.frequency})")

class Scheduler:
    def __init__(self):
        self.owners: List[Owner] = []
        self.task_queue: List[Tuple[Pet, Task]] = []

    def load_tasks(self, owner: Owner) -> None:
        """Pulls all tasks from an owner's pets into the queue."""
        if owner not in self.owners:
            self.owners.append(owner)
        self.task_queue.clear()
        for pet in owner.pets:
            for task in pet.tasks:
                self.task_queue.append((pet, task))

    def sort_by_time(self) -> None:
        """Sorts task_queue by scheduled_time ascending."""
        self.task_queue.sort(key=lambda item: item[1].scheduled_time)

    def get_upcoming_tasks(self, hours: int) -> List[Task]:
        """Returns tasks due within the next N hours."""
        now = datetime.now()
        threshold = now + timedelta(hours=hours)
        return [task for _, task in self.task_queue if now <= task.scheduled_time <= threshold]

    def check_conflicts(self) -> List[str]:
        """Detects if two tasks for the same pet overlap or hit the exact same time."""
        warnings = []
        # Group tasks by pet to check individual schedules
        pet_schedules = {}
        for pet, task in self.task_queue:
            if pet.name not in pet_schedules:
                pet_schedules[pet.name] = []
            pet_schedules[pet.name].append(task)
        
        for pet_name, tasks in pet_schedules.items():
            # Check exact time collisions
            seen_times = {}
            for t in tasks:
                if t.scheduled_time in seen_times:
                    warnings.append(f"⚠️ Conflict: '{t.name}' and '{seen_times[t.scheduled_time].name}' are scheduled at the same time for {pet_name}!")
                seen_times[t.scheduled_time] = t
        return warnings

    def generate_daily_summary(self, owner: Owner) -> str:
        """Produces a text summary of the day's tasks."""
        self.load_tasks(owner)
        total = len(self.task_queue)
        completed = len([t for _, t in self.task_queue if t.status == "completed"])
        return f"Daily Summary for {owner.name}: {completed}/{total} tasks completed today."