# CLAUDE.MD

## Project Overview

FutaDomWorld Chat - A Ren'Py phone texting simulator where players chat with AI characters via DeepInfra (DeepSeek V3.2). Spinoff of FutaDomWorld, targeting Steam with adult content rating. Subscription-based access through a proxy server.

### Technology Stack

- **Engine**: Ren'Py 8.x (Python-based visual novel engine)
- **Language**: Ren'Py script (.rpy) + Python
- **AI Backend**: DeepInfra API (DeepSeek V3.2) via proxy server
- **Proxy Server**: Flask (Python)
- **Target Platform**: Steam (Windows, Mac, Linux)

## Project Structure

```
/
├── CLAUDE.MD
├── .gitignore
├── game/                       # Ren'Py game directory
│   ├── characters.rpy          # <<< CHARACTER PROMPTS & DEFINITIONS GO HERE
│   ├── chat_api.rpy            # Proxy server integration, ChatSession class
│   ├── script.rpy              # Game entry point, phone navigation, chat loop
│   ├── phone_screens.rpy       # Phone UI (messages list, chat view, contacts)
│   ├── screens.rpy             # Menus, save/load, subscription key screen
│   ├── options.rpy             # Steam build config, window settings
│   ├── gui.rpy                 # Colors, fonts, sizing
│   └── images/
│       └── characters/         # <<< CHARACTER ART GOES HERE
│           └── placeholder_avatar.png
└── server/                     # Proxy server (deploy separately)
    ├── app.py                  # Flask proxy (auth, rate limit, DeepInfra relay)
    ├── requirements.txt        # Python dependencies
    └── .env.example            # Template for server environment variables
```

## Where To Put Things

### System Prompts
Edit `game/characters.rpy` - each character has a named prompt variable:
- `MALLORY_PROMPT` - Mallory's personality
- `CHARACTER_2_PROMPT` through `CHARACTER_5_PROMPT` - slots for more characters

### Character Art
Drop PNG files into `game/images/characters/`:
- Name them anything (e.g. `mallory.png`, `vicky.png`)
- Update the `avatar=` path in the ChatSession definition in `characters.rpy`
- Recommended size: 128x128 or larger, square aspect ratio

### Adding a New Character
1. Write their system prompt in `game/characters.rpy`
2. Drop their avatar PNG in `game/images/characters/`
3. Uncomment/add a `default xxx_chat = ChatSession(...)` block in `characters.rpy`
4. Add them to the `all_chats` list in `game/script.rpy`

### Proxy Server URL
Edit `game/chat_api.rpy` line 11: `PROXY_SERVER_URL = "http://localhost:8080"`
Change to your deployed server URL for production.

## Running Locally

### Game
1. Install Ren'Py SDK 8.x from https://www.renpy.org/
2. Open Ren'Py Launcher, point it at this project
3. Click "Launch Project"

### Proxy Server
```bash
cd server
cp .env.example .env       # Edit .env with your real keys
pip install -r requirements.txt
python app.py
```

## Server Deployment

The proxy server keeps the DeepInfra API key server-side. Deploy to any Python hosting (Railway, Fly.io, Render, VPS, etc).

Required environment variables (set on your hosting provider):
- `DEEPINFRA_API_KEY` - Your DeepInfra API key
- `TOKEN_SECRET` - Random secret for signing player tokens
- `ADMIN_KEY` - Secret for the admin token-creation endpoint
- `DEEPINFRA_MODEL` - Model ID (default: `deepseek-ai/DeepSeek-V3-0324`)

Create player tokens via: `POST /admin/create_token` with `{"admin_key": "...", "player_id": "...", "duration_days": 30}`

## Architecture

- Game client authenticates with proxy using player subscription tokens
- Proxy validates token, rate-limits (20 req/min), forwards to DeepInfra
- API key never ships in the game build
- Player tokens stored in Ren'Py `persistent` (survives across game sessions)
- Phone UI uses `call screen` pattern with state machine in `script.rpy`
- Chat history capped at 40 messages (20 exchanges) for token management
- Phone styling constants at top of `phone_screens.rpy`

## Notes for Claude AI

- Do NOT commit API keys or .env files
- Character prompts and definitions are in `characters.rpy`, NOT `chat_api.rpy`
- When adding characters, update both `characters.rpy` and the `all_chats` list in `script.rpy`
- Phone UI colors are `define` constants in `phone_screens.rpy`
- `renpy.fetch()` is used for HTTP (built-in, non-blocking)
- `persistent.player_token` stores the subscription key across sessions
