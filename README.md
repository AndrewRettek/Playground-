# BindrChat

A standalone chat companion app built as a spinoff of [FutaDomWorld](https://store.steampowered.com/app/1296590/FutaDomWorld/). Chat with AI-powered characters through a stylized phone interface built in Ren'Py.

## What Is This?

BindrChat is a desktop app that simulates a phone messaging interface. You select a character from your contacts list and have freeform conversations powered by AI (DeepSeek V3 via DeepInfra). Each character has a unique personality defined by detailed system prompts.

### Characters
- **Mallory** — A young temple acolyte with a golden halo and quiet devotion
- **Rye Romanov** — A red-haired noble's daughter and unapologetic party girl
- **Demitria** — The Eminence, regal head of the Imperial Temple
- **Gabby** — A friendly teal-haired IT worker

## Features

The app features a phone-style UI with:
- Rounded phone frame with shadow and depth
- Circular character avatars with colored border rings
- Rounded chat bubbles (blue for player, dark for characters)
- Dark cohesive color scheme with ornate Midjourney-generated UI art
- Per-character accent colors (gold, red, purple, teal) in headers, badges, and status
- Animated typing indicator (bouncing dots) while waiting for AI responses
- Async AI responses — the game stays interactive while the character "types"
- Message timestamps and read receipts
- Unread message count badges on the contacts list
- Sound effects for sent and received messages
- Smooth dissolve transitions between screens
- Phone entrance animation (fade + zoom)
- Inter font family for clean, modern typography
- Shared world setting prompt that applies to all characters automatically

## Tech Stack

- **Game Engine**: [Ren'Py 8.x](https://www.renpy.org/) — Visual novel engine with Python-based screen language
- **AI Backend**: [DeepInfra](https://deepinfra.com/) running DeepSeek V3 for chat completions
- **Proxy Server**: Flask app deployed on [Railway](https://railway.app/) — sits between the game and DeepInfra to keep the API key secure
- **Character Art**: Generated with [Midjourney](https://www.midjourney.com/)
- **UI Art**: Midjourney-generated backgrounds and banners, plus programmatically generated phone chrome (rounded corners, icons, bubbles) using Python/PIL
- **Font**: [Inter](https://rsms.me/inter/) — clean, modern sans-serif by Rasmus Andersson
- **Sound Effects**: Programmatically generated WAV tones using Python's `wave` module

## How It Was Built

This project was built collaboratively between a human developer and **Claude** (Anthropic's AI assistant, model claude-opus-4-6) using [Claude Code](https://claude.ai/code), Anthropic's CLI tool for AI-assisted software development.

**What Claude did:**
- Architected the full project structure (Ren'Py game + Flask proxy server)
- Wrote all game code: phone UI screens, chat API integration, state management, character definitions framework
- Built the Flask proxy server with rate limiting and token auth
- Generated phone UI assets programmatically with PIL (rounded phone frame, chat bubbles, contact cards, status bar icons, navigation icons, circular avatar borders)
- Wrote Midjourney prompts for character portraits and UI art (backgrounds, banners, logo)
- Processed and integrated all Midjourney art (resizing, cropping, darkening, circular masking)
- Configured Railway deployment (Procfile, nixpacks.toml, railway.toml)
- Debugged Ren'Py screen language issues (dynamic screen delegation, input handling, displayable properties)
- Added polish: animated typing indicator, per-character accent colors, timestamps, read receipts, unread badges, sound effects, screen transitions, phone entrance animation
- Implemented async API calls (background threads with `renpy.invoke_in_thread()`)
- Integrated Inter font family and generated sound effect WAVs programmatically
- Built distributable packages for Windows, Mac, and Linux

**What the human did:**
- Creative direction and game design decisions
- Wrote all character system prompts (personalities, lore, backstories)
- Wrote the comprehensive world setting prompt (Empire lore, biology, laws, locations, organizations)
- Generated character portraits and UI art in Midjourney using Claude's prompts
- Provided the DeepInfra API key and Railway deployment
- QA testing, visual design direction, and feedback

## Running Locally

### Prerequisites
- [Ren'Py 8.x](https://www.renpy.org/latest.html) installed
- Python 3.11+ (for the proxy server)

### Game Client
1. Clone this repo
2. Open Ren'Py Launcher and add this project
3. Click "Launch Project"

### Proxy Server (required for AI chat)
```bash
cd server
pip install -r requirements.txt

# Set your DeepInfra API key
export DEEPINFRA_API_KEY="your-key-here"
export PORT=8080

python app.py
```

The game connects to the proxy server URL configured in `game/chat_api.rpy` (`PROXY_SERVER_URL`).

## Project Structure

```
├── game/
│   ├── chat_api.rpy          # Proxy server integration, ChatSession class
│   ├── characters.rpy         # World setting + character definitions and system prompts
│   ├── phone_screens.rpy      # Phone UI (messages, chat, contacts), transforms
│   ├── screens.rpy            # Main menu, subscription, standard Ren'Py screens
│   ├── script.rpy             # Main game flow, state machine, transitions
│   ├── options.rpy            # Build config
│   ├── gui.rpy                # GUI colors and fonts (Inter)
│   ├── audio/                 # Sound effects (message sent/received)
│   ├── gui/fonts/             # Inter font family (Regular, Medium, SemiBold, Bold)
│   ├── gui/phone/             # Generated phone UI assets (PIL)
│   ├── images/characters/     # Character portrait art (Midjourney)
│   └── images/ui/             # UI art (Midjourney, processed)
├── server/
│   ├── app.py                 # Flask proxy server
│   └── requirements.txt       # Server dependencies
├── generate_phone_assets.py   # PIL script to generate phone UI PNGs
├── generate_sounds.py         # Script to generate sound effect WAVs
├── process_ui_assets.py       # PIL script to resize Midjourney UI art
├── Procfile                   # Railway start command
├── railway.toml               # Railway build config
└── nixpacks.toml              # Nixpacks build config
```

## License

This is a proprietary project — part of the BindrChat / FutaDomWorld franchise. All rights reserved.
