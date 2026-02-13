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
## SYSTEM PROMPTS - Edit these with your character personalities
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

    ## -----------------------------------------------------------------
    ## DEMITRIA
    ## -----------------------------------------------------------------
    DEMITRIA_PROMPT = """\
You are Demitria. You are texting with the player through a messaging \
app on their phone. Keep your responses conversational and casual. \
Use texting style naturally. Keep responses to 1-3 short paragraphs.

[REPLACE WITH YOUR ACTUAL DEMITRIA SYSTEM PROMPT]
"""

    ## -----------------------------------------------------------------
    ## GABBY
    ## -----------------------------------------------------------------
    GABBY_PROMPT = """\
You are Gabby. You are texting with the player through a messaging \
app on their phone. Keep your responses conversational and casual. \
Use texting style naturally. Keep responses to 1-3 short paragraphs.

[REPLACE WITH YOUR ACTUAL GABBY SYSTEM PROMPT]
"""


## =====================================================================
## CHARACTER SESSIONS
## =====================================================================

default mallory_chat = ChatSession(
    "Mallory",
    system_prompt=MALLORY_PROMPT,
    avatar="images/characters/mallory.png"
)

default rye_chat = ChatSession(
    "Rye",
    system_prompt=RYE_PROMPT,
    avatar="images/characters/rye.png"
)

default demitria_chat = ChatSession(
    "Demitria",
    system_prompt=DEMITRIA_PROMPT,
    avatar="images/characters/demitria.png"
)

default gabby_chat = ChatSession(
    "Gabby",
    system_prompt=GABBY_PROMPT,
    avatar="images/characters/gabby.png"
)
