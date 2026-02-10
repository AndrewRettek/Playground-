# CLAUDE.MD

## Project Overview

FutaDomWorld Chat - A Ren'Py-based phone texting simulator where players chat with AI-powered characters through an in-game phone interface. Spinoff of FutaDomWorld, targeting Steam distribution with adult content rating.

### Technology Stack

- **Engine**: Ren'Py (Python-based visual novel engine)
- **Language**: Ren'Py script (.rpy) + Python
- **AI Backend**: DeepInfra API (DeepSeek V3.2) for chatbot responses
- **Target Platform**: Steam (Windows, Mac, Linux)

## Project Structure

```
/
├── CLAUDE.MD              # This file
├── game/                  # Ren'Py game directory (all game logic and assets)
│   ├── options.rpy        # Game config, build settings, Steam distribution
│   ├── gui.rpy            # GUI visual configuration (colors, fonts, sizes)
│   ├── screens.rpy        # Core Ren'Py screens (menus, save/load, input, confirm)
│   ├── phone_screens.rpy  # Phone UI screens (phone frame, chat, messages, contacts, Bindr)
│   ├── chat_api.rpy       # DeepInfra API integration, ChatMessage/ChatSession classes
│   ├── script.rpy         # Main game script and phone navigation loop
│   ├── gui/
│   │   └── phone/         # Phone UI image assets (frames, backgrounds)
│   └── images/
│       └── characters/    # Character avatars and sprites
│           └── placeholder_avatar.png
└── README.txt             # Distributed with the game
```

## Key Files and Components

- `game/chat_api.rpy`: DeepInfra API calls, ChatMessage class, ChatSession class (manages conversation history, API context window)
- `game/phone_screens.rpy`: All phone UI - phone_frame (outer shell), phone_chat (conversation view), phone_messages_list, phone_contacts, phone_bindr
- `game/script.rpy`: Game entry point (`label start`), phone navigation state machine, chat input loop
- `game/screens.rpy`: Standard Ren'Py screens (main_menu, save, load, preferences, input, confirm)
- `game/options.rpy`: Steam build configuration, window size, game metadata

## Development Setup

### Prerequisites

- Ren'Py SDK 8.x+ (download from https://www.renpy.org/)
- DeepInfra API key (set in `game/chat_api.rpy` - `DEEPINFRA_API_KEY`)

### Running Locally

1. Place this project folder inside your Ren'Py projects directory
2. Open Ren'Py Launcher, select the project
3. Click "Launch Project"

### Building for Steam

1. In Ren'Py Launcher: Build > "Windows, Mac, Linux for Markets"
2. Upload via SteamPipe to Steamworks

## Configuration

### Environment Variables / Config

- `DEEPINFRA_API_KEY`: Set in `game/chat_api.rpy` - your DeepInfra API key
- `DEEPINFRA_MODEL`: Model identifier, currently `deepseek-ai/DeepSeek-V3-0324`
- `DEFAULT_SYSTEM_PROMPT`: Character personality prompt in `game/chat_api.rpy`

## Architecture Notes

- The phone UI uses Ren'Py's `call screen` pattern with a state machine in `script.rpy`
- `phone_frame` is a wrapper screen that draws the phone shell and delegates content to inner screens
- Chat history is stored in `ChatSession` objects (both display messages and API context)
- API context is capped at 40 messages (20 exchanges) to manage token usage
- Player text input uses `renpy.input()` which shows the built-in input screen
- HTTP calls use `renpy.fetch()` (built-in, non-blocking)

## Notes for Claude AI

- All phone UI styling constants are at the top of `phone_screens.rpy` (PHONE_BG, PHONE_BUBBLE_PLAYER, etc.)
- When adding new characters, create a new ChatSession in `script.rpy` defaults and add to `all_chats`
- System prompts for characters will be refined separately - placeholder is in `chat_api.rpy`
- Do NOT commit API keys - the key field in chat_api.rpy should remain as placeholder text

---

**Last Updated**: 2026-02-10
