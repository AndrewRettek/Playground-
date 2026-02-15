# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

School of Athens — a Ren'Py phone-texting simulator where players chat with ancient Greek philosophers (Socrates, Aristotle, Heraclitus, Epicurus, Herodotus, Diogenes) powered by DeepInfra AI (DeepSeek V3) via a Flask proxy server. Resolution is 1280x720 with a warm marble & gold visual theme.

## Architecture

### Two-Part System

1. **Ren'Py Game Client** (`game/`) — The visual novel, a phone UI with chat screens. Uses `renpy.fetch()` for non-blocking HTTP and `renpy.invoke_in_thread()` for background API calls.
2. **Flask Proxy Server** (`server/app.py`) — Deployed separately (Railway). Holds the DeepInfra API key server-side, validates player tokens, rate-limits requests, forwards chat completions. Currently open (auth decorator exists but is not applied to `/v1/chat`).

### Game Code Flow

- `script.rpy` — State machine loop. `phone_state` toggles between `"messages"`, `"contacts"`, and `"chat"`. Uses `call screen` pattern (screens return `(action, data)` tuples via `Return()`).
- `characters.rpy` — System prompts + `ChatSession` instances. `WORLD_SETTING_PROMPT` is prepended to every character's prompt. The `all_chats` list drives what appears in the UI.
- `chat_api.rpy` — `ChatSession` class, `call_chat_api()` function, player auth helpers. API history capped at 40 messages. `_fetch_response` runs in a background thread and calls `renpy.restart_interaction()` when done.
- `phone_screens.rpy` — All phone UI screens. Color constants defined at top as `define` statements. Three main screens: `phone_messages_list`, `phone_chat`, `phone_contacts`.
- `screens.rpy` — Standard Ren'Py screens (main menu, save/load, preferences, confirm, subscription key entry).

### Init Order Matters

- `init -1 python:` — System prompts, `ChatSession` class, API functions (in `characters.rpy` and `chat_api.rpy`)
- `init 1 python:` — Character session instances and `all_chats` list (in `characters.rpy`)
- Screen `define` statements and `default` statements run at their default init levels

### Asset Generation Pipeline

All UI assets are procedurally generated with Python scripts (Pillow required). These produce the PNGs in `game/gui/phone/` and `game/images/ui/`:

- `generate_phone_assets.py` — Phone body, bubbles, buttons, circular avatars, nav/status icons
- `generate_ui_assets.py` — Menu background, desktop background, chat texture, logo
- `generate_portraits.py` — Placeholder character portraits (360x600, 4 poses each)
- `generate_sounds.py` — WAV sound effects (message sent/received, button tap)
- `process_portraits.py` — Background removal pipeline for real character art (uses rembg). Source-to-output mappings configured in `PORTRAITS` list.

Run any generator: `python generate_phone_assets.py` (from project root). After changing character avatar PNGs, re-run `generate_phone_assets.py` to regenerate circular avatars.

### Proxy Server

Deployed on Railway. Run locally: `cd server && pip install -r requirements.txt && python app.py`

Proxy URL configured in `chat_api.rpy` line 12: `PROXY_SERVER_URL`

## Adding a New Character

1. Write system prompt in `characters.rpy` (add `CHARACTER_PROMPT` variable in `init -1 python:` block)
2. Add avatar PNG to `game/images/characters/`
3. Run `python generate_phone_assets.py` to create circular avatar
4. Add `ChatSession` instance in `characters.rpy` `init 1 python:` block
5. Add to `all_chats` list
6. Add color entry to `CHARACTER_COLORS` dict in `chat_api.rpy`

## Self-Review Checklist

After every code change, check:

1. **Ren'Py screen layout** — `yalign`, `xalign`, `ysize` vs `yminimum` interactions. Removing a centering property from a parent causes child drift.
2. **Viewport scroll state** — Chat viewport uses `yadjustment` + `_needs_scroll` flag. New state affecting content height should trigger scroll reset.
3. **Side effects** — Changing fixed `ysize` to `yminimum` affects `yfill True` elements. Changing hbox `yalign` affects all children.
4. **Asset pipeline** — After processing images, verify output dimensions and transparency across all characters.
5. **File naming** — Source images may have spaces/capitals. Game code references lowercase with underscores.
6. **Ren'Py displayable limits** — `input` is single-line. `pixel_width` causes horizontal scroll, not wrapping.
