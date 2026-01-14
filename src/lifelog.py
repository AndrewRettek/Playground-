#!/usr/bin/env python3
"""
Life Logging CLI Tool
Tracks mood, weight, todos, and Retatrutide dosing.
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
import argparse
import sys

# Base data directory
DATA_DIR = Path(__file__).parent.parent / "data"


def ensure_data_dirs():
    """Ensure all data directories exist."""
    for subdir in ["mood", "weight", "todos", "retatrutide"]:
        (DATA_DIR / subdir).mkdir(parents=True, exist_ok=True)


def get_today_str():
    """Get today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def get_month_file(category: str) -> Path:
    """Get the data file path for current month."""
    month_str = datetime.now().strftime("%Y-%m")
    return DATA_DIR / category / f"{month_str}.json"


def load_month_data(category: str) -> dict:
    """Load data for the current month."""
    filepath = get_month_file(category)
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return {"entries": []}


def save_month_data(category: str, data: dict):
    """Save data for the current month."""
    filepath = get_month_file(category)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


# =============================================================================
# MOOD TRACKING
# =============================================================================

MOOD_SCALE = {
    1: "Very Low",
    2: "Low",
    3: "Below Average",
    4: "Slightly Low",
    5: "Neutral",
    6: "Slightly Good",
    7: "Good",
    8: "Very Good",
    9: "Great",
    10: "Excellent"
}


def log_mood(score: int, notes: str = "", energy: int = None, anxiety: int = None):
    """Log a mood entry."""
    if not 1 <= score <= 10:
        print("Error: Mood score must be between 1 and 10")
        return False

    data = load_month_data("mood")
    entry = {
        "date": get_today_str(),
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "label": MOOD_SCALE.get(score, "Unknown"),
        "notes": notes
    }

    if energy is not None:
        if 1 <= energy <= 10:
            entry["energy"] = energy
        else:
            print("Warning: Energy must be 1-10, ignoring")

    if anxiety is not None:
        if 1 <= anxiety <= 10:
            entry["anxiety"] = anxiety
        else:
            print("Warning: Anxiety must be 1-10, ignoring")

    data["entries"].append(entry)
    save_month_data("mood", data)
    print(f"Logged mood: {score}/10 ({MOOD_SCALE[score]})")
    if notes:
        print(f"Notes: {notes}")
    return True


def show_mood_summary(days: int = 7):
    """Show mood summary for recent days."""
    data = load_month_data("mood")
    entries = data.get("entries", [])

    if not entries:
        print("No mood entries found for this month.")
        return

    # Get last N entries
    recent = entries[-days:] if len(entries) >= days else entries

    print(f"\n{'='*50}")
    print(f"MOOD SUMMARY (Last {len(recent)} entries)")
    print(f"{'='*50}")

    total_score = 0
    for entry in recent:
        score = entry["score"]
        total_score += score
        extras = []
        if "energy" in entry:
            extras.append(f"Energy: {entry['energy']}")
        if "anxiety" in entry:
            extras.append(f"Anxiety: {entry['anxiety']}")
        extra_str = f" | {', '.join(extras)}" if extras else ""
        print(f"{entry['date']}: {score}/10 ({entry['label']}){extra_str}")
        if entry.get("notes"):
            print(f"         Notes: {entry['notes']}")

    avg = total_score / len(recent)
    print(f"\nAverage mood: {avg:.1f}/10")


# =============================================================================
# WEIGHT TRACKING
# =============================================================================

def log_weight(weight: float, unit: str = "lbs", notes: str = ""):
    """Log a weight entry."""
    if weight <= 0:
        print("Error: Weight must be positive")
        return False

    data = load_month_data("weight")
    entry = {
        "date": get_today_str(),
        "timestamp": datetime.now().isoformat(),
        "weight": weight,
        "unit": unit,
        "notes": notes
    }

    data["entries"].append(entry)
    save_month_data("weight", data)
    print(f"Logged weight: {weight} {unit}")

    # Show change from last entry if available
    if len(data["entries"]) > 1:
        prev = data["entries"][-2]
        if prev["unit"] == unit:
            change = weight - prev["weight"]
            direction = "up" if change > 0 else "down"
            print(f"Change from last: {abs(change):.1f} {unit} {direction}")

    return True


def show_weight_summary(days: int = 30):
    """Show weight summary."""
    data = load_month_data("weight")
    entries = data.get("entries", [])

    if not entries:
        print("No weight entries found for this month.")
        return

    recent = entries[-days:] if len(entries) >= days else entries

    print(f"\n{'='*50}")
    print(f"WEIGHT SUMMARY (Last {len(recent)} entries)")
    print(f"{'='*50}")

    weights = []
    for entry in recent:
        weight = entry["weight"]
        unit = entry["unit"]
        weights.append(weight)
        print(f"{entry['date']}: {weight} {unit}")
        if entry.get("notes"):
            print(f"         Notes: {entry['notes']}")

    if len(weights) >= 2:
        print(f"\nStarting: {weights[0]} | Current: {weights[-1]}")
        print(f"Total change: {weights[-1] - weights[0]:.1f}")
        print(f"Average: {sum(weights)/len(weights):.1f}")


# =============================================================================
# TODO TRACKING
# =============================================================================

def get_todos_file() -> Path:
    """Get the todos file path."""
    return DATA_DIR / "todos" / "todos.json"


def load_todos() -> dict:
    """Load todos data."""
    filepath = get_todos_file()
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return {"todos": [], "completed": []}


def save_todos(data: dict):
    """Save todos data."""
    filepath = get_todos_file()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def add_todo(task: str, priority: str = "medium", due: str = None):
    """Add a new todo item."""
    data = load_todos()

    todo = {
        "id": len(data["todos"]) + len(data["completed"]) + 1,
        "task": task,
        "priority": priority,
        "created": datetime.now().isoformat(),
        "due": due,
        "status": "pending"
    }

    data["todos"].append(todo)
    save_todos(data)
    print(f"Added todo #{todo['id']}: {task}")
    if priority != "medium":
        print(f"Priority: {priority}")
    if due:
        print(f"Due: {due}")
    return True


def complete_todo(todo_id: int):
    """Mark a todo as complete."""
    data = load_todos()

    for i, todo in enumerate(data["todos"]):
        if todo["id"] == todo_id:
            todo["status"] = "completed"
            todo["completed_at"] = datetime.now().isoformat()
            data["completed"].append(todo)
            data["todos"].pop(i)
            save_todos(data)
            print(f"Completed: {todo['task']}")
            return True

    print(f"Todo #{todo_id} not found")
    return False


def list_todos(show_completed: bool = False):
    """List all todos."""
    data = load_todos()

    print(f"\n{'='*50}")
    print("PENDING TODOS")
    print(f"{'='*50}")

    if not data["todos"]:
        print("No pending todos!")
    else:
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_todos = sorted(data["todos"], key=lambda x: priority_order.get(x["priority"], 1))

        for todo in sorted_todos:
            priority_marker = {"high": "[!]", "medium": "[-]", "low": "[ ]"}.get(todo["priority"], "[-]")
            due_str = f" (due: {todo['due']})" if todo.get("due") else ""
            print(f"{priority_marker} #{todo['id']}: {todo['task']}{due_str}")

    if show_completed and data["completed"]:
        print(f"\n{'='*50}")
        print("COMPLETED TODOS")
        print(f"{'='*50}")
        for todo in data["completed"][-10:]:  # Last 10 completed
            print(f"[x] #{todo['id']}: {todo['task']}")


def delete_todo(todo_id: int):
    """Delete a todo item."""
    data = load_todos()

    for i, todo in enumerate(data["todos"]):
        if todo["id"] == todo_id:
            removed = data["todos"].pop(i)
            save_todos(data)
            print(f"Deleted: {removed['task']}")
            return True

    print(f"Todo #{todo_id} not found")
    return False


# =============================================================================
# RETATRUTIDE TRACKING
# =============================================================================

RETATRUTIDE_DOSES = [0.5, 1.0, 2.0, 4.0, 8.0, 12.0]  # mg, standard titration


def log_retatrutide(dose: float, site: str = "", notes: str = ""):
    """Log a Retatrutide injection."""
    data = load_month_data("retatrutide")

    entry = {
        "date": get_today_str(),
        "timestamp": datetime.now().isoformat(),
        "dose_mg": dose,
        "injection_site": site,
        "notes": notes
    }

    data["entries"].append(entry)
    save_month_data("retatrutide", data)
    print(f"Logged Retatrutide: {dose} mg")
    if site:
        print(f"Injection site: {site}")
    if notes:
        print(f"Notes: {notes}")

    # Calculate next dose date (weekly)
    next_date = date.today()
    from datetime import timedelta
    next_date = next_date + timedelta(days=7)
    print(f"Next dose due: {next_date.isoformat()}")

    return True


def show_retatrutide_summary():
    """Show Retatrutide history and dosing schedule."""
    data = load_month_data("retatrutide")
    entries = data.get("entries", [])

    print(f"\n{'='*50}")
    print("RETATRUTIDE TRACKING")
    print(f"{'='*50}")

    if not entries:
        print("No Retatrutide entries found for this month.")
        print("\nStandard titration schedule:")
        print("  Weeks 1-4:   0.5 mg/week")
        print("  Weeks 5-8:   1.0 mg/week")
        print("  Weeks 9-12:  2.0 mg/week")
        print("  Weeks 13-16: 4.0 mg/week")
        print("  Weeks 17-20: 8.0 mg/week")
        print("  Weeks 21+:   12.0 mg/week (maintenance)")
        return

    print("Recent doses:")
    for entry in entries[-8:]:  # Last 8 weeks
        site_str = f" @ {entry['injection_site']}" if entry.get("injection_site") else ""
        print(f"  {entry['date']}: {entry['dose_mg']} mg{site_str}")
        if entry.get("notes"):
            print(f"           Notes: {entry['notes']}")

    # Calculate stats
    total_doses = len(entries)
    current_dose = entries[-1]["dose_mg"]

    print(f"\nTotal doses logged: {total_doses}")
    print(f"Current dose: {current_dose} mg")

    # Next dose reminder
    last_date = datetime.fromisoformat(entries[-1]["timestamp"]).date()
    from datetime import timedelta
    next_date = last_date + timedelta(days=7)
    days_until = (next_date - date.today()).days

    if days_until < 0:
        print(f"\nOVERDUE: Next dose was due {abs(days_until)} days ago!")
    elif days_until == 0:
        print(f"\nDue TODAY!")
    else:
        print(f"\nNext dose due: {next_date.isoformat()} ({days_until} days)")


# =============================================================================
# DAILY SUMMARY
# =============================================================================

def show_daily_summary():
    """Show a comprehensive daily summary."""
    today = get_today_str()

    print(f"\n{'='*60}")
    print(f"LIFE LOG SUMMARY - {today}")
    print(f"{'='*60}")

    # Mood
    mood_data = load_month_data("mood")
    today_moods = [e for e in mood_data.get("entries", []) if e["date"] == today]
    if today_moods:
        latest = today_moods[-1]
        print(f"\nMood: {latest['score']}/10 ({latest['label']})")
    else:
        print(f"\nMood: Not logged today")

    # Weight
    weight_data = load_month_data("weight")
    today_weights = [e for e in weight_data.get("entries", []) if e["date"] == today]
    if today_weights:
        latest = today_weights[-1]
        print(f"Weight: {latest['weight']} {latest['unit']}")
    else:
        weights = weight_data.get("entries", [])
        if weights:
            latest = weights[-1]
            print(f"Weight: {latest['weight']} {latest['unit']} (last: {latest['date']})")
        else:
            print(f"Weight: Not logged")

    # Todos
    todos_data = load_todos()
    pending = len(todos_data.get("todos", []))
    high_priority = len([t for t in todos_data.get("todos", []) if t.get("priority") == "high"])
    print(f"Todos: {pending} pending ({high_priority} high priority)")

    # Retatrutide
    reta_data = load_month_data("retatrutide")
    entries = reta_data.get("entries", [])
    if entries:
        last_entry = entries[-1]
        last_date = datetime.fromisoformat(last_entry["timestamp"]).date()
        from datetime import timedelta
        next_date = last_date + timedelta(days=7)
        days_until = (next_date - date.today()).days

        if days_until <= 0:
            print(f"Retatrutide: DUE {'TODAY' if days_until == 0 else f'{abs(days_until)} days ago'}! (current: {last_entry['dose_mg']} mg)")
        else:
            print(f"Retatrutide: Next dose in {days_until} days (current: {last_entry['dose_mg']} mg)")
    else:
        print(f"Retatrutide: No doses logged")

    print(f"\n{'='*60}")


# =============================================================================
# CLI ARGUMENT PARSING
# =============================================================================

def main():
    ensure_data_dirs()

    parser = argparse.ArgumentParser(
        description="Life Logging CLI - Track mood, weight, todos, and Retatrutide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s mood 7 --notes "Feeling good today"
  %(prog)s mood 8 --energy 7 --anxiety 3
  %(prog)s weight 185.5
  %(prog)s todo add "Buy groceries" --priority high
  %(prog)s todo done 1
  %(prog)s todo list
  %(prog)s reta 2.0 --site "left abdomen"
  %(prog)s summary
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Mood commands
    mood_parser = subparsers.add_parser("mood", help="Log or view mood")
    mood_parser.add_argument("score", type=int, nargs="?", help="Mood score 1-10")
    mood_parser.add_argument("--notes", "-n", default="", help="Additional notes")
    mood_parser.add_argument("--energy", "-e", type=int, help="Energy level 1-10")
    mood_parser.add_argument("--anxiety", "-a", type=int, help="Anxiety level 1-10")
    mood_parser.add_argument("--summary", "-s", action="store_true", help="Show mood summary")
    mood_parser.add_argument("--days", "-d", type=int, default=7, help="Days to show in summary")

    # Weight commands
    weight_parser = subparsers.add_parser("weight", help="Log or view weight")
    weight_parser.add_argument("value", type=float, nargs="?", help="Weight value")
    weight_parser.add_argument("--unit", "-u", default="lbs", help="Unit (lbs/kg)")
    weight_parser.add_argument("--notes", "-n", default="", help="Additional notes")
    weight_parser.add_argument("--summary", "-s", action="store_true", help="Show weight summary")
    weight_parser.add_argument("--days", "-d", type=int, default=30, help="Days to show in summary")

    # Todo commands
    todo_parser = subparsers.add_parser("todo", help="Manage todos")
    todo_subparsers = todo_parser.add_subparsers(dest="action", help="Todo actions")

    todo_add = todo_subparsers.add_parser("add", help="Add a new todo")
    todo_add.add_argument("task", help="Task description")
    todo_add.add_argument("--priority", "-p", choices=["high", "medium", "low"], default="medium")
    todo_add.add_argument("--due", "-d", help="Due date (YYYY-MM-DD)")

    todo_done = todo_subparsers.add_parser("done", help="Complete a todo")
    todo_done.add_argument("id", type=int, help="Todo ID to complete")

    todo_delete = todo_subparsers.add_parser("delete", help="Delete a todo")
    todo_delete.add_argument("id", type=int, help="Todo ID to delete")

    todo_list = todo_subparsers.add_parser("list", help="List todos")
    todo_list.add_argument("--all", "-a", action="store_true", help="Show completed todos too")

    # Retatrutide commands
    reta_parser = subparsers.add_parser("reta", help="Log or view Retatrutide")
    reta_parser.add_argument("dose", type=float, nargs="?", help="Dose in mg")
    reta_parser.add_argument("--site", "-s", default="", help="Injection site")
    reta_parser.add_argument("--notes", "-n", default="", help="Additional notes")
    reta_parser.add_argument("--summary", action="store_true", help="Show Retatrutide summary")

    # Summary command
    subparsers.add_parser("summary", help="Show daily summary")

    # Parse and execute
    args = parser.parse_args()

    if not args.command:
        show_daily_summary()
        return

    if args.command == "mood":
        if args.summary or args.score is None:
            show_mood_summary(args.days)
        else:
            log_mood(args.score, args.notes, args.energy, args.anxiety)

    elif args.command == "weight":
        if args.summary or args.value is None:
            show_weight_summary(args.days)
        else:
            log_weight(args.value, args.unit, args.notes)

    elif args.command == "todo":
        if args.action == "add":
            add_todo(args.task, args.priority, args.due)
        elif args.action == "done":
            complete_todo(args.id)
        elif args.action == "delete":
            delete_todo(args.id)
        elif args.action == "list" or args.action is None:
            list_todos(args.all if hasattr(args, "all") else False)
        else:
            list_todos()

    elif args.command == "reta":
        if args.summary or args.dose is None:
            show_retatrutide_summary()
        else:
            log_retatrutide(args.dose, args.site, args.notes)

    elif args.command == "summary":
        show_daily_summary()


if __name__ == "__main__":
    main()
