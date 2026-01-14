# CLAUDE.MD

## Project Overview

### Purpose

Life Logging Tracker - A simple CLI tool for daily life tracking including mood, weight, todos, and medication (Retatrutide) tracking. Designed for personal use with local JSON file storage.

### Technology Stack

- **Languages**: Python 3
- **Storage**: JSON files (no database required)
- **Tools**: Standard library only (no external dependencies)

## Project Structure

```
/
├── lifelog           # Convenience shell wrapper script
├── src/
│   └── lifelog.py    # Main CLI application
├── data/
│   ├── mood/         # Monthly mood tracking JSON files
│   ├── weight/       # Monthly weight tracking JSON files
│   ├── todos/        # Todo list JSON file
│   └── retatrutide/  # Monthly Retatrutide tracking JSON files
└── CLAUDE.MD         # This file
```

## Development Setup

### Prerequisites

- Python 3.6+

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Playground-

# Make scripts executable (already done)
chmod +x lifelog src/lifelog.py
```

### Running

```bash
# Using the wrapper script
./lifelog <command>

# Or directly with Python
python3 src/lifelog.py <command>
```

## Usage

### Mood Tracking

```bash
# Log mood (1-10 scale)
./lifelog mood 7
./lifelog mood 8 --notes "Great day at work"
./lifelog mood 6 --energy 7 --anxiety 3

# View mood summary
./lifelog mood --summary
./lifelog mood --summary --days 14
```

**Mood Scale:**
- 1-2: Very Low/Low
- 3-4: Below Average/Slightly Low
- 5: Neutral
- 6-7: Slightly Good/Good
- 8-9: Very Good/Great
- 10: Excellent

### Weight Tracking

```bash
# Log weight
./lifelog weight 180.5
./lifelog weight 82 --unit kg
./lifelog weight 179 --notes "After morning workout"

# View weight summary
./lifelog weight --summary
./lifelog weight --summary --days 30
```

### Todo Management

```bash
# Add todos
./lifelog todo add "Buy groceries"
./lifelog todo add "Call doctor" --priority high
./lifelog todo add "Submit report" --due 2026-01-20

# List todos
./lifelog todo list
./lifelog todo list --all  # Include completed

# Complete a todo
./lifelog todo done 1

# Delete a todo
./lifelog todo delete 2
```

**Priority Levels:**
- `high` - Displayed with [!]
- `medium` - Displayed with [-] (default)
- `low` - Displayed with [ ]

### Retatrutide Tracking

```bash
# Log injection
./lifelog reta 2.0
./lifelog reta 4.0 --site "left abdomen"
./lifelog reta 4.0 --notes "Slight redness at site"

# View history and schedule
./lifelog reta --summary
```

**Standard Titration Schedule:**
- Weeks 1-4: 0.5 mg/week
- Weeks 5-8: 1.0 mg/week
- Weeks 9-12: 2.0 mg/week
- Weeks 13-16: 4.0 mg/week
- Weeks 17-20: 8.0 mg/week
- Weeks 21+: 12.0 mg/week (maintenance)

### Daily Summary

```bash
# View comprehensive daily summary
./lifelog summary
./lifelog  # Default action shows summary
```

## Data Storage

All data is stored in JSON files organized by month (except todos):

- `data/mood/YYYY-MM.json` - Monthly mood entries
- `data/weight/YYYY-MM.json` - Monthly weight entries
- `data/retatrutide/YYYY-MM.json` - Monthly medication entries
- `data/todos/todos.json` - Persistent todo list

### Data Format Examples

**Mood Entry:**
```json
{
  "date": "2026-01-14",
  "timestamp": "2026-01-14T10:30:00",
  "score": 7,
  "label": "Good",
  "notes": "Productive morning",
  "energy": 8,
  "anxiety": 3
}
```

**Weight Entry:**
```json
{
  "date": "2026-01-14",
  "timestamp": "2026-01-14T07:00:00",
  "weight": 180.5,
  "unit": "lbs",
  "notes": "Morning weigh-in"
}
```

**Todo Entry:**
```json
{
  "id": 1,
  "task": "Buy groceries",
  "priority": "high",
  "created": "2026-01-14T09:00:00",
  "due": "2026-01-15",
  "status": "pending"
}
```

**Retatrutide Entry:**
```json
{
  "date": "2026-01-14",
  "timestamp": "2026-01-14T08:00:00",
  "dose_mg": 4.0,
  "injection_site": "left abdomen",
  "notes": ""
}
```

## Key Files and Components

### Core Files

- `src/lifelog.py`: Main CLI application with all tracking functionality
- `lifelog`: Shell wrapper for convenient invocation

### Important Patterns

- Monthly JSON files for time-series data (mood, weight, medication)
- Single JSON file for stateful data (todos)
- All dates in ISO 8601 format
- Timestamps stored for precise tracking

## Development Guidelines

### Code Style

- Python 3.6+ compatible
- Standard library only (no pip dependencies)
- Type hints for function parameters
- Clear docstrings for functions

### Git Workflow

- **Main Branch**: `main`
- **Feature Branches**: `claude/<feature-name>-<id>`
- **Commit Messages**: Descriptive present tense

## Notes for Claude AI

### Project-Specific Guidance

- This is a personal life logging tool - keep it simple and focused
- No external dependencies - use only Python standard library
- Data is stored locally in JSON files - no database setup needed
- Monthly file rotation keeps individual files manageable

### Testing Strategy

- Run `./lifelog summary` to verify tool is working
- Test each subcommand manually
- Check JSON files in `data/` directory for correct formatting

### Future Enhancement Ideas

- Export to CSV functionality
- Data visualization/charts
- Backup/sync functionality
- Web interface

---

**Last Updated**: 2026-01-14
**Maintained By**: Life Logging Project
