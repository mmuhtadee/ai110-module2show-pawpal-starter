import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Persistent state: initialize once, survive every re-run ---
if "owner" not in st.session_state:
    default_pet = Pet(name="Mochi", species="Dog")
    default_owner = Owner(name="Jordan")
    default_owner.add_pet(default_pet)
    st.session_state.owner = default_owner

owner: Owner = st.session_state.owner

st.title("🐾 PawPal+")
st.caption(f"Managing pets for **{owner.name}**")

st.divider()

# ── Section 1: Add a Pet ──────────────────────────────────────────────────────
st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_pet_name = st.text_input("Pet name", placeholder="e.g. Buddy")
    with col2:
        new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    submitted_pet = st.form_submit_button("Add Pet")

if submitted_pet:
    if new_pet_name.strip():
        owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species))
        st.success(f"{new_pet_name.strip()} added!")
    else:
        st.warning("Please enter a pet name.")

# Show current pets
pet_names = [p.name for p in owner.pets]
if pet_names:
    st.write("**Current pets:**", ", ".join(pet_names))
else:
    st.info("No pets yet — add one above.")

st.divider()

# ── Section 2: Add a Task to a Pet ───────────────────────────────────────────
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        target_pet_name = st.selectbox("Assign to pet", pet_names)
        col1, col2, col3 = st.columns(3)
        with col1:
            task_desc = st.text_input("Description", placeholder="e.g. Morning walk")
        with col2:
            task_time = st.text_input("Time (HH:MM)", placeholder="08:00")
        with col3:
            task_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Once"])
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        if task_desc.strip() and task_time.strip():
            target_pet = next(p for p in owner.pets if p.name == target_pet_name)
            target_pet.add_task(Task(
                description=task_desc.strip(),
                time=task_time.strip(),
                frequency=task_freq,
            ))
            st.success(f"Task '{task_desc.strip()}' added to {target_pet_name}.")
        else:
            st.warning("Please fill in both a description and a time.")

st.divider()

# ── Section 3: Today's Schedule ──────────────────────────────────────────────
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.info("No tasks scheduled yet.")
    else:
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_time()

        rows = []
        for task in sorted_tasks:
            rows.append({
                "Time": task.time,
                "Description": task.description,
                "Frequency": task.frequency,
                "Status": "Done" if task.is_completed else "Pending",
            })
        st.table(rows)

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning("Scheduling conflicts detected:")
            for group in conflicts:
                names = ", ".join(t.description for t in group)
                st.write(f"- {group[0].time}: {names}")
        else:
            st.success("No conflicts detected.")
