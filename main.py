from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner: Owner) -> None:
    print("=" * 40)
    print("       TODAY'S SCHEDULE - PawPal+")
    print("=" * 40)
    print(f"Owner : {owner.name}\n")

    for pet in owner.pets:
        print(f"  [{pet.species}] {pet.name}")
        print(f"  {'-' * 30}")
        tasks = pet.get_tasks()
        if not tasks:
            print("    No tasks scheduled.")
        for task in tasks:
            status = "DONE" if task.is_completed else "PENDING"
            print(f"    {task.time}  |  {task.description:<25} |  {task.frequency:<8}  |  [{status}]")
        print()

    print("=" * 40)


def main():
    # --- Create owner ---
    owner = Owner(name="Alex")

    # --- Create pets ---
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna", species="Cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    # --- Add tasks to Buddy ---
    dog.add_task(Task(description="Morning walk",   time="08:00", frequency="Daily"))
    dog.add_task(Task(description="Lunch feeding",  time="12:00", frequency="Daily"))
    dog.add_task(Task(description="Evening walk",   time="18:00", frequency="Daily"))

    # --- Add tasks to Luna ---
    cat.add_task(Task(description="Breakfast",      time="08:30", frequency="Daily"))
    cat.add_task(Task(description="Medication",     time="12:00", frequency="Weekly"))
    cat.add_task(Task(description="Dinner",         time="19:00", frequency="Daily"))

    # --- Mark one task complete to show the status column works ---
    dog.get_tasks()[0].mark_complete()

    # --- Print human-readable schedule ---
    print_schedule(owner)

    # --- Demonstrate Scheduler ---
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()
    print("Tasks sorted by time:")
    for task in sorted_tasks:
        print(f"  {task.time}  {task.description}")

    print()
    pending = scheduler.filter_by_status(status=False)
    print(f"Pending tasks : {len(pending)}")
    done = scheduler.filter_by_status(status=True)
    print(f"Completed tasks: {len(done)}")

    print()
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("Scheduling conflicts detected:")
        for group in conflicts:
            names = ", ".join(t.description for t in group)
            print(f"  {group[0].time}  ->  {names}")
    else:
        print("No scheduling conflicts detected.")


if __name__ == "__main__":
    main()
