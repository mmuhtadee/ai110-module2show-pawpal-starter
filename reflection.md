# PawPal+ Project Reflection

## 1. System Design
- Add pet profiles
- Schedule tasks for a pet
- View the schedule

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design splits the app into four core classes (Owner, Pet, Task, Scheduler) to cleanly separate who owns the data, what the data is, and how the schedule gets managed.
- What classes did you include, and what responsibilities did you assign to each?
Owner: Represents the human.
Pet: Represents the animal.
Task: Represents each objective.
Scheduler: Utilizes owner's data to manage the schedule gracefully.

**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
After adding additional functions to the program, the AI code became less readable in expense of the pythonic aesthetic. Therefore, we had to refactor, and expand out the condensed methods and list comprehensions to achieve readabilty.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler primarily constrains tasks by time and ownership.
- How did you decide which constraints mattered most?
I prioritized these because they are the constraints that ensure the app functions as a reliable tool.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The next() form is more Pythonic and saves a line, but the explicit loop is easier to read for anyone newer to Python. Neither has a performance difference at this scale.
- Why is that tradeoff reasonable for this scenario?
It is reasonable because this version is more readable, and the one liner improvement is just for aesthetic, not a real improvement.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI across the entire process as a tech consultant and programmar.
- What kinds of prompts or questions were most helpful?
I figured that asking AI with context, and explain the why to a semi-technical person helps me both learn and notice and hallucinations.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
There was a point, claude wrote code that uses the sorted algorithm and lambda key to write concisely. Since I was not familiar with those, I asked it to refactor with a simple for-loop to keep it readable and understandable.
- How did you evaluate or verify what the AI suggested?
I verified AI responses by testing the website constantly, and asking it to explain its reasoning simply.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested task sorting, and conflict between tasks.
- Why were these tests important?
They were important because they validate the critical functions of the program, and if they fail, the program becomes unusable
**b. Confidence**

- How confident are you that your scheduler works correctly? 5/5
- What edge cases would you test next if you had more time?
If I had more energy and time available, I'd like to test how the scheduler handles change in time-zones.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied with how cool the app turned out to be. Also, how different components are beautifully separated, but comes together when the app runs.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I'd improve how Task handles user input. Also, I'd love to integrate a pet theme to the UI

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Asking the right question to AI is only a part of what we have to do to get the best result. We have to be careful about when to start a new chat, or how much context the AI needs to be able to build your dream program.
