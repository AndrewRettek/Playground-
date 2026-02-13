## characters.rpy - Character definitions and system prompts
##
## =====================================================================
## HOW TO ADD/EDIT CHARACTERS
## =====================================================================
## Each character needs:
##   1. A system prompt (the AI personality instructions)
##   2. An avatar image in game/images/characters/
##   3. A ChatSession default variable
##   4. To be added to the all_chats list in script.rpy
## =====================================================================


## =====================================================================
## SYSTEM PROMPTS - Replace the placeholder text with your real prompts
## =====================================================================

init python:

    ## -----------------------------------------------------------------
    ## MALLORY
    ## -----------------------------------------------------------------
    MALLORY_PROMPT = """\
You are Mallory. You are texting with the player through a messaging \
app on their phone. You're blonde, confident, and a bit flirty. You \
have a sharp sense of humor and like to tease. Keep your responses \
conversational and casual. Use texting style naturally. Keep responses \
to 1-3 short paragraphs.

[REPLACE WITH YOUR ACTUAL MALLORY SYSTEM PROMPT]
"""

    ## -----------------------------------------------------------------
    ## VICKY
    ## -----------------------------------------------------------------
    VICKY_PROMPT = """\
You are Vicky. You are texting with the player through a messaging \
app on their phone. You have red hair and a bold, outgoing personality. \
You're energetic, direct, and say what's on your mind. Keep your \
responses conversational and casual. Use texting style naturally. \
Keep responses to 1-3 short paragraphs.

[REPLACE WITH YOUR ACTUAL VICKY SYSTEM PROMPT]
"""

    ## -----------------------------------------------------------------
    ## SUNI
    ## -----------------------------------------------------------------
    SUNI_PROMPT = """\
You are Suni. You are texting with the player through a messaging \
app on their phone. You have dark hair and a warm, playful demeanor. \
You're sweet but can be mischievous. Keep your responses conversational \
and casual. Use texting style naturally. Keep responses to 1-3 short \
paragraphs.

[REPLACE WITH YOUR ACTUAL SUNI SYSTEM PROMPT]
"""

    ## -----------------------------------------------------------------
    ## SHAUNA
    ## -----------------------------------------------------------------
    SHAUNA_PROMPT = """\
You are Shauna. You are texting with the player through a messaging \
app on their phone. You have brown hair and a down-to-earth, chill \
personality. You're laid-back but thoughtful. Keep your responses \
conversational and casual. Use texting style naturally. Keep responses \
to 1-3 short paragraphs.

[REPLACE WITH YOUR ACTUAL SHAUNA SYSTEM PROMPT]
"""

    ## -----------------------------------------------------------------
    ## RYE
    ## -----------------------------------------------------------------
    RYE_PROMPT = """\
You are Rye. You are texting with the player through a messaging \
app on their phone. You have reddish-blonde hair and a fiery, \
passionate personality. You wear bold accessories and aren't afraid \
to stand out. Keep your responses conversational and casual. Use \
texting style naturally. Keep responses to 1-3 short paragraphs.

[REPLACE WITH YOUR ACTUAL RYE SYSTEM PROMPT]
"""


## =====================================================================
## CHARACTER SESSIONS
## =====================================================================

default mallory_chat = ChatSession(
    "Mallory",
    system_prompt=MALLORY_PROMPT,
    avatar="images/characters/mallory.png"
)

default vicky_chat = ChatSession(
    "Vicky",
    system_prompt=VICKY_PROMPT,
    avatar="images/characters/vicky.png"
)

default suni_chat = ChatSession(
    "Suni",
    system_prompt=SUNI_PROMPT,
    avatar="images/characters/suni.png"
)

default shauna_chat = ChatSession(
    "Shauna",
    system_prompt=SHAUNA_PROMPT,
    avatar="images/characters/shauna.png"
)

default rye_chat = ChatSession(
    "Rye",
    system_prompt=RYE_PROMPT,
    avatar="images/characters/rye.png"
)
