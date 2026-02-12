## characters.rpy - Character definitions and system prompts
##
## =====================================================================
## HOW TO ADD/EDIT CHARACTERS
## =====================================================================
## Each character needs:
##   1. A system prompt (the AI personality instructions)
##   2. An avatar image in game/images/characters/
##   3. A ChatSession default variable
##   4. To be added to the all_chats list
##
## To add a new character:
##   1. Write their system prompt below
##   2. Drop their avatar PNG into game/images/characters/
##   3. Add a "default xxx_chat = ChatSession(...)" line
##   4. Add them to the all_chats list in script.rpy
## =====================================================================


## =====================================================================
## SYSTEM PROMPTS - Edit these with your character personalities
## =====================================================================

init python:

    ## -----------------------------------------------------------------
    ## MALLORY
    ## -----------------------------------------------------------------
    MALLORY_PROMPT = """\
You are Mallory, a friendly and witty character. You are texting with \
the player through a messaging app. Keep your responses conversational, \
casual, and in-character. Use texting abbreviations naturally but don't \
overdo it. Keep responses to 1-3 short paragraphs.

[REPLACE THIS WITH YOUR ACTUAL MALLORY SYSTEM PROMPT]
"""

    ## -----------------------------------------------------------------
    ## CHARACTER 2 (rename and fill in)
    ## -----------------------------------------------------------------
    CHARACTER_2_PROMPT = """\
[PASTE YOUR SYSTEM PROMPT HERE]
"""

    ## -----------------------------------------------------------------
    ## CHARACTER 3 (rename and fill in)
    ## -----------------------------------------------------------------
    CHARACTER_3_PROMPT = """\
[PASTE YOUR SYSTEM PROMPT HERE]
"""

    ## -----------------------------------------------------------------
    ## CHARACTER 4 (rename and fill in)
    ## -----------------------------------------------------------------
    CHARACTER_4_PROMPT = """\
[PASTE YOUR SYSTEM PROMPT HERE]
"""

    ## -----------------------------------------------------------------
    ## CHARACTER 5 (rename and fill in)
    ## -----------------------------------------------------------------
    CHARACTER_5_PROMPT = """\
[PASTE YOUR SYSTEM PROMPT HERE]
"""


## =====================================================================
## CHARACTER SESSIONS
## =====================================================================
## Avatar filenames should match what you put in game/images/characters/
## e.g. "images/characters/mallory.png"

default mallory_chat = ChatSession(
    "Mallory",
    system_prompt=MALLORY_PROMPT,
    avatar="images/characters/placeholder_avatar.png"
)

## Uncomment and edit these as you add characters:
##
## default char2_chat = ChatSession(
##     "Character Name",
##     system_prompt=CHARACTER_2_PROMPT,
##     avatar="images/characters/char2.png"
## )
##
## default char3_chat = ChatSession(
##     "Character Name",
##     system_prompt=CHARACTER_3_PROMPT,
##     avatar="images/characters/char3.png"
## )
##
## default char4_chat = ChatSession(
##     "Character Name",
##     system_prompt=CHARACTER_4_PROMPT,
##     avatar="images/characters/char4.png"
## )
##
## default char5_chat = ChatSession(
##     "Character Name",
##     system_prompt=CHARACTER_5_PROMPT,
##     avatar="images/characters/char5.png"
## )
