from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    print("🚀 Initializing PawPal+ CLI Demo Test Ground...\n")
    
    # 1. Create Owner and Pets
    owner = Owner(name="Munshat", email="munshat@example.com", phone="555-0199")
    
    dog = Pet(name="Buddy", breed="Golden Retriever", age=3, species="Dog")
    cat = Pet(name="Luna", breed="Siamese", age=2, species="Cat")
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # 2. Add Tasks (Deliberately out of order to verify sorting later)
    now = datetime.now()
    
    task1 = Task(name="Evening Walk", task_type="walk", scheduled_time=now + timedelta(hours=6), frequency="daily")
    task2 = Task(name="Morning Feeding", task_type="feeding", scheduled_time=now + timedelta(hours=1), frequency="daily")
    # This task3 deliberately conflicts with task2's exact time to test conflict detection!
    task3 = Task(name="Luna Insulin Shot", task_type="medication", scheduled_time=now + timedelta(hours=1), frequency="daily")
    
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)
    
    # 3. Load Engine & Check Conflicts
    scheduler = Scheduler()
    scheduler.load_tasks(owner)
    
    print("--- Conflict Check ---")
    conflicts = scheduler.check_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("✅ No schedule conflicts detected.")
        
    # 4. Sort and View Schedule
    print("\n--- Sorting Tasks Chronologically ---")
    scheduler.sort_by_time()
    
    for pet, task in scheduler.task_queue:
        print(f"⏰ {task.scheduled_time.strftime('%H:%M')} | [{pet.name}] {task.name} ({task.status})")

    # 5. Test Summary Output
    print("\n--- System Metrics ---")
    print(scheduler.generate_daily_summary(owner))

if __name__ == "__main__":
    main()