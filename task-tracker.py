import sys
import json
from datetime import datetime

# A JSON object becomes a Python dict.
# A JSON array becomes a Python list.
# Strings, numbers, booleans map naturally.

file='task.json'
arg=sys.argv

#add
if len(arg) > 1 and arg[1] == "add":
    description = " ".join(arg[2:])
    if not description.strip():
        print("Error: Enter Task description.")
        sys.exit(1)
    with open(file, "r") as f:
        tasks = json.load(f)
    next_id = max([t["id"] for t in tasks], default=0) + 1
    now = datetime.utcnow().isoformat() + "Z"
    task = {
        "id": next_id,
        "description": description.strip(),
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(task)
    with open(file, "w") as f:
        json.dump(tasks, f, indent=2)
    print(f"Task added successfully (ID: {next_id})")

#update
elif len(arg) > 1 and arg[1] == "update":
    index = int(arg[2])
    new_description = " ".join(arg[3:])
    with open(file, "r") as f:
        tasks = json.load(f)
    found = False
    for t in tasks:
        if t['id'] == index:
            t['description'] = new_description.strip()
            t['updatedAt'] = datetime.utcnow().isoformat() + "Z"
            found = True
            break
    if not found:
        print(f"Task with ID {index} not found.")
    else:
        with open(file, "w") as f:
            json.dump(tasks, f, indent=2)
        print(f"Task {index} updated.")

#delete
elif len(arg) > 1 and arg[1] == "delete":
    index = int(arg[2])
    with open(file, "r") as f:
        tasks = json.load(f)
    found = False
    for i, t in enumerate(tasks):
        if t['id'] == index:
            tasks.pop(i)
            found = True
            break
    if not found:
        print(f"Task with ID {index} not found.")
    else:
        with open(file, "w") as f:
            json.dump(tasks, f, indent=2)
        print(f"Task {index} deleted.")
####################################################
#status
elif len(arg) > 1 and arg[1] == "mark-in-progress":
    index = int(arg[2])
    with open(file, "r") as f:
        tasks = json.load(f)
    found = False
    
    for t in tasks:
        if t['id'] == index:
            t['status'] = "in-progress"
            t['updatedAt'] = datetime.utcnow().isoformat() + "Z"
            found = True
            break
    if not found:
        print(f"Task with ID {index} not found.")
    else:
        with open(file, "w") as f:
            json.dump(tasks, f, indent=2)
        print(f"Task {index} marked as in-progress.")

elif len(arg) > 1 and arg[1] == "mark-done":
    index = int(arg[2])
    with open(file, "r") as f:
        tasks = json.load(f)

    found = False
 
    for t in tasks:
        if t['id'] == index:
            t['status'] = "done"
            t['updatedAt'] = datetime.utcnow().isoformat() + "Z"
            found = True
            break

    if not found:
        print(f"Task with ID {index} not found.")
    else:
        with open(file, "w") as f:
            json.dump(tasks, f, indent=2)
        print(f"Task {index} marked as done.")



#listing
elif len(arg) > 1 and arg[1] == "list":
    list_status = arg[2] if len(arg) > 2 else ""

    with open(file, "r") as f:
        tasks = json.load(f)

    if not tasks:
        print("No tasks.")
        sys.exit(0)

    filtered_tasks = tasks
    if list_status:
        filtered_tasks = [t for t in tasks if t['status'] == list_status.strip()]
        if not filtered_tasks:
            print(f"No tasks with status '{list_status}'.")
            sys.exit(0)

    for t in filtered_tasks:
        print(f"{t['id']}: [{t['status']}] {t['description']} (updated: {t['updatedAt']})")


else:
    print("Usage: python task_tracker.py <add|delete|update|mark-in-progress|mark-done|list> ...")