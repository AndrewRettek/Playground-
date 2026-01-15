#!/usr/bin/env python3
"""
Life Logging CLI Tool
Tracks mood, weight, todos, Retatrutide dosing, and Oura Ring data.
"""

import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path
import argparse
import sys
import urllib.request
import urllib.error

# Base directories
DATA_DIR = Path(__file__).parent.parent / "data"
CONFIG_DIR = Path(__file__).parent.parent / "config"


def ensure_data_dirs():
    """Ensure all data directories exist."""
    for subdir in ["mood", "weight", "todos", "retatrutide", "oura"]:
        (DATA_DIR / subdir).mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


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
# OURA RING INTEGRATION
# =============================================================================

OURA_API_BASE = "https://api.ouraring.com/v2/usercollection"


def get_config_file() -> Path:
    """Get the config file path."""
    return CONFIG_DIR / "config.json"


def load_config() -> dict:
    """Load configuration."""
    filepath = get_config_file()
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    """Save configuration."""
    filepath = get_config_file()
    with open(filepath, "w") as f:
        json.dump(config, f, indent=2)


def set_oura_token(token: str):
    """Set the Oura API token."""
    config = load_config()
    config["oura_token"] = token
    save_config(config)
    print("Oura API token saved successfully.")


def get_oura_token() -> str:
    """Get the Oura API token."""
    config = load_config()
    token = config.get("oura_token")
    if not token:
        # Also check environment variable
        token = os.environ.get("OURA_TOKEN")
    return token


def oura_api_request(endpoint: str, params: dict = None) -> dict:
    """Make a request to the Oura API."""
    token = get_oura_token()
    if not token:
        print("Error: Oura API token not set.")
        print("Run: ./lifelog oura token YOUR_TOKEN")
        return None

    url = f"{OURA_API_BASE}/{endpoint}"
    if params:
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query_string}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("Error: Invalid Oura API token. Please update your token.")
        elif e.code == 429:
            print("Error: Rate limited. Please wait before trying again.")
        else:
            print(f"Error: Oura API returned {e.code}: {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to Oura API: {e.reason}")
        return None


def sync_oura_data(date_str: str = None):
    """Sync Oura data for a specific date."""
    if date_str is None:
        date_str = get_today_str()

    # For Oura API, we need to query a range
    # Sleep data is attributed to the day you wake up
    start_date = date_str
    end_date = (datetime.fromisoformat(date_str) + timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Syncing Oura data for {date_str}...")

    synced = {}

    # Fetch sleep data
    sleep_data = oura_api_request("daily_sleep", {"start_date": start_date, "end_date": end_date})
    if sleep_data and sleep_data.get("data"):
        synced["sleep"] = sleep_data["data"]
        print(f"  Sleep: {len(sleep_data['data'])} record(s)")

    # Fetch readiness data
    readiness_data = oura_api_request("daily_readiness", {"start_date": start_date, "end_date": end_date})
    if readiness_data and readiness_data.get("data"):
        synced["readiness"] = readiness_data["data"]
        print(f"  Readiness: {len(readiness_data['data'])} record(s)")

    # Fetch activity data
    activity_data = oura_api_request("daily_activity", {"start_date": start_date, "end_date": end_date})
    if activity_data and activity_data.get("data"):
        synced["activity"] = activity_data["data"]
        print(f"  Activity: {len(activity_data['data'])} record(s)")

    # Fetch heart rate data
    hr_data = oura_api_request("heartrate", {"start_datetime": f"{start_date}T00:00:00", "end_datetime": f"{end_date}T00:00:00"})
    if hr_data and hr_data.get("data"):
        synced["heart_rate"] = hr_data["data"]
        print(f"  Heart Rate: {len(hr_data['data'])} reading(s)")

    if not synced:
        print("No data found for this date.")
        return False

    # Save to monthly file
    data = load_month_data("oura")

    # Update or add entry for this date
    existing_idx = None
    for i, entry in enumerate(data["entries"]):
        if entry.get("date") == date_str:
            existing_idx = i
            break

    entry = {
        "date": date_str,
        "synced_at": datetime.now().isoformat(),
        **synced
    }

    if existing_idx is not None:
        data["entries"][existing_idx] = entry
    else:
        data["entries"].append(entry)

    save_month_data("oura", data)
    print(f"Oura data saved for {date_str}")
    return True


def get_oura_data_for_date(date_str: str = None) -> dict:
    """Get cached Oura data for a specific date."""
    if date_str is None:
        date_str = get_today_str()

    data = load_month_data("oura")
    for entry in data.get("entries", []):
        if entry.get("date") == date_str:
            return entry
    return None


def show_oura_sleep(date_str: str = None):
    """Show Oura sleep data."""
    if date_str is None:
        date_str = get_today_str()

    entry = get_oura_data_for_date(date_str)

    print(f"\n{'='*50}")
    print(f"OURA SLEEP - {date_str}")
    print(f"{'='*50}")

    if not entry or not entry.get("sleep"):
        print("No sleep data found. Run: ./lifelog oura sync")
        return

    for sleep in entry["sleep"]:
        score = sleep.get("score")
        if score:
            print(f"\nSleep Score: {score}")

        contributors = sleep.get("contributors", {})
        if contributors:
            print("\nContributors:")
            for key, value in contributors.items():
                if value is not None:
                    print(f"  {key.replace('_', ' ').title()}: {value}")


def show_oura_readiness(date_str: str = None):
    """Show Oura readiness data."""
    if date_str is None:
        date_str = get_today_str()

    entry = get_oura_data_for_date(date_str)

    print(f"\n{'='*50}")
    print(f"OURA READINESS - {date_str}")
    print(f"{'='*50}")

    if not entry or not entry.get("readiness"):
        print("No readiness data found. Run: ./lifelog oura sync")
        return

    for readiness in entry["readiness"]:
        score = readiness.get("score")
        if score:
            print(f"\nReadiness Score: {score}")

        contributors = readiness.get("contributors", {})
        if contributors:
            print("\nContributors:")
            for key, value in contributors.items():
                if value is not None:
                    print(f"  {key.replace('_', ' ').title()}: {value}")


def show_oura_activity(date_str: str = None):
    """Show Oura activity data."""
    if date_str is None:
        date_str = get_today_str()

    entry = get_oura_data_for_date(date_str)

    print(f"\n{'='*50}")
    print(f"OURA ACTIVITY - {date_str}")
    print(f"{'='*50}")

    if not entry or not entry.get("activity"):
        print("No activity data found. Run: ./lifelog oura sync")
        return

    for activity in entry["activity"]:
        score = activity.get("score")
        if score:
            print(f"\nActivity Score: {score}")

        print(f"\nMetrics:")
        metrics = [
            ("steps", "Steps"),
            ("active_calories", "Active Calories"),
            ("total_calories", "Total Calories"),
            ("equivalent_walking_distance", "Walking Distance (m)"),
            ("low_activity_time", "Low Activity (min)"),
            ("medium_activity_time", "Medium Activity (min)"),
            ("high_activity_time", "High Activity (min)"),
        ]
        for key, label in metrics:
            value = activity.get(key)
            if value is not None:
                print(f"  {label}: {value}")


def show_oura_summary(date_str: str = None, days: int = 7):
    """Show Oura summary for recent days."""
    if date_str is None:
        date_str = get_today_str()

    print(f"\n{'='*50}")
    print(f"OURA SUMMARY (Last {days} days)")
    print(f"{'='*50}")

    data = load_month_data("oura")
    entries = data.get("entries", [])

    if not entries:
        print("No Oura data found. Run: ./lifelog oura sync")
        return

    # Sort by date and get recent
    entries = sorted(entries, key=lambda x: x.get("date", ""))
    recent = entries[-days:] if len(entries) >= days else entries

    print(f"\n{'Date':<12} {'Sleep':<8} {'Ready':<8} {'Active':<8} {'Steps':<8}")
    print("-" * 50)

    for entry in recent:
        date_val = entry.get("date", "N/A")

        sleep_score = "-"
        if entry.get("sleep"):
            sleep_score = str(entry["sleep"][0].get("score", "-"))

        readiness_score = "-"
        if entry.get("readiness"):
            readiness_score = str(entry["readiness"][0].get("score", "-"))

        activity_score = "-"
        steps = "-"
        if entry.get("activity"):
            activity_score = str(entry["activity"][0].get("score", "-"))
            steps = str(entry["activity"][0].get("steps", "-"))

        print(f"{date_val:<12} {sleep_score:<8} {readiness_score:<8} {activity_score:<8} {steps:<8}")

    # Calculate averages
    sleep_scores = [e["sleep"][0]["score"] for e in recent if e.get("sleep") and e["sleep"][0].get("score")]
    readiness_scores = [e["readiness"][0]["score"] for e in recent if e.get("readiness") and e["readiness"][0].get("score")]
    activity_scores = [e["activity"][0]["score"] for e in recent if e.get("activity") and e["activity"][0].get("score")]

    print("-" * 50)
    if sleep_scores:
        print(f"Avg Sleep: {sum(sleep_scores)/len(sleep_scores):.0f}", end="  ")
    if readiness_scores:
        print(f"Avg Readiness: {sum(readiness_scores)/len(readiness_scores):.0f}", end="  ")
    if activity_scores:
        print(f"Avg Activity: {sum(activity_scores)/len(activity_scores):.0f}")
    print()


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
        next_date = last_date + timedelta(days=7)
        days_until = (next_date - date.today()).days

        if days_until <= 0:
            print(f"Retatrutide: DUE {'TODAY' if days_until == 0 else f'{abs(days_until)} days ago'}! (current: {last_entry['dose_mg']} mg)")
        else:
            print(f"Retatrutide: Next dose in {days_until} days (current: {last_entry['dose_mg']} mg)")
    else:
        print(f"Retatrutide: No doses logged")

    # Oura Ring
    oura_entry = get_oura_data_for_date(today)
    if oura_entry:
        oura_parts = []
        if oura_entry.get("sleep") and oura_entry["sleep"][0].get("score"):
            oura_parts.append(f"Sleep: {oura_entry['sleep'][0]['score']}")
        if oura_entry.get("readiness") and oura_entry["readiness"][0].get("score"):
            oura_parts.append(f"Readiness: {oura_entry['readiness'][0]['score']}")
        if oura_entry.get("activity") and oura_entry["activity"][0].get("score"):
            oura_parts.append(f"Activity: {oura_entry['activity'][0]['score']}")
            if oura_entry["activity"][0].get("steps"):
                oura_parts.append(f"Steps: {oura_entry['activity'][0]['steps']}")
        if oura_parts:
            print(f"Oura: {' | '.join(oura_parts)}")
        else:
            print(f"Oura: Data synced but no scores available")
    else:
        print(f"Oura: Not synced today (run: ./lifelog oura sync)")

    print(f"\n{'='*60}")


# =============================================================================
# CLI ARGUMENT PARSING
# =============================================================================

def main():
    ensure_data_dirs()

    parser = argparse.ArgumentParser(
        description="Life Logging CLI - Track mood, weight, todos, Retatrutide, and Oura Ring data",
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
  %(prog)s oura token YOUR_API_TOKEN
  %(prog)s oura sync
  %(prog)s oura sleep
  %(prog)s oura --summary
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

    # Oura commands
    oura_parser = subparsers.add_parser("oura", help="Oura Ring integration")
    oura_subparsers = oura_parser.add_subparsers(dest="action", help="Oura actions")

    oura_token = oura_subparsers.add_parser("token", help="Set Oura API token")
    oura_token.add_argument("value", help="Your Oura API token")

    oura_sync = oura_subparsers.add_parser("sync", help="Sync Oura data")
    oura_sync.add_argument("--date", "-d", help="Date to sync (YYYY-MM-DD), defaults to today")
    oura_sync.add_argument("--days", type=int, default=1, help="Number of days to sync (backwards from date)")

    oura_sleep = oura_subparsers.add_parser("sleep", help="Show sleep data")
    oura_sleep.add_argument("--date", "-d", help="Date to show (YYYY-MM-DD)")

    oura_readiness = oura_subparsers.add_parser("readiness", help="Show readiness data")
    oura_readiness.add_argument("--date", "-d", help="Date to show (YYYY-MM-DD)")

    oura_activity = oura_subparsers.add_parser("activity", help="Show activity data")
    oura_activity.add_argument("--date", "-d", help="Date to show (YYYY-MM-DD)")

    oura_parser.add_argument("--summary", "-s", action="store_true", help="Show Oura summary")
    oura_parser.add_argument("--days", type=int, default=7, help="Days to show in summary")

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

    elif args.command == "oura":
        if args.action == "token":
            set_oura_token(args.value)
        elif args.action == "sync":
            sync_date = args.date or get_today_str()
            if args.days > 1:
                # Sync multiple days
                for i in range(args.days):
                    d = (datetime.fromisoformat(sync_date) - timedelta(days=i)).strftime("%Y-%m-%d")
                    sync_oura_data(d)
            else:
                sync_oura_data(sync_date)
        elif args.action == "sleep":
            show_oura_sleep(args.date)
        elif args.action == "readiness":
            show_oura_readiness(args.date)
        elif args.action == "activity":
            show_oura_activity(args.date)
        elif args.summary or args.action is None:
            show_oura_summary(days=args.days)
        else:
            show_oura_summary(days=args.days)

    elif args.command == "summary":
        show_daily_summary()


if __name__ == "__main__":
    main()
