# Asset Credits & Attribution

Track all external assets, references, and third-party resources used in this project.
Replace with original assets before release, or ensure proper licensing/attribution.

---

## Phone UI Assets (Generated)

All phone UI assets in `game/gui/phone/` are **procedurally generated** by
`generate_phone_assets.py` using PIL/Pillow. They are original to this project.

**Design reference:**
- [Yet Another Phone for Ren'Py](https://github.com/NathanGuilhot/yet-another-phone-for-renpy) by Nighten
  - License: Art assets CC0, code MIT
  - Used as **visual reference only** for phone bezel style, camera/speaker placement
  - No assets were copied — our phone body, bubbles, icons are all generated from scratch

**Other resources evaluated (not used):**
- [Ren'Py Phone System](https://kleineluka.itch.io/phone) by kleineluka — Free with credit required
- [Kenney UI Pack](https://kenney.nl/assets/ui-pack) — CC0
- [Unblast Smartphone Mockup](https://unblast.com/smartphone-mockup-in-psd-and-png/) — Free commercial

---

## Fonts

- **Inter** (Regular, Medium, SemiBold, Bold) — `game/gui/fonts/`
  - License: SIL Open Font License 1.1
  - Source: https://rsms.me/inter/
  - Status: **Free for commercial use, no attribution required**

---

## Sound Effects (Generated)

All sound effects in `game/audio/` are **procedurally generated** by
`generate_sounds.py` using Python's wave/struct modules. Original to this project.

---

## Midjourney Art

UI backgrounds and character portraits in `game/images/` are generated with Midjourney.
- `images/ui/desktop_bg.png` — Desktop background behind phone
- `images/ui/menu_bg.png` — Main menu background
- `images/ui/chat_bg.png` — Chat message area texture
- `images/ui/messages_header.png` — Messages list header banner
- `images/ui/logo.png` — Game logo
- `images/characters/*.png` — Character portraits/avatars
- Status: **Verify Midjourney license terms for commercial use before release**

---

## TODO Before Release

- [ ] Verify Midjourney commercial license covers all generated art
- [ ] Consider replacing generated phone assets with hand-drawn art for unique style
- [ ] Consider replacing generated sounds with professionally recorded audio
- [ ] Confirm Inter font OFL compliance (include license file in distribution)
