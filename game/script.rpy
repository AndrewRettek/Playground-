## script.rpy - Main game script

## ===================================================================
## CHARACTER AND SESSION INITIALIZATION
## ===================================================================

## Initialize chat sessions on game start
default mallory_chat = ChatSession(
    "Mallory",
    system_prompt=DEFAULT_SYSTEM_PROMPT,
    avatar="images/characters/placeholder_avatar.png"
)

default all_chats = [mallory_chat]

## Track which screen we're on
default phone_state = "messages"
default current_chat = None

## ===================================================================
## MAIN GAME FLOW
## ===================================================================

label start:
    ## Skip straight to the phone interface
    call phone_main
    return

## ===================================================================
## PHONE MAIN LOOP
## ===================================================================

label phone_main:
    ## Main phone navigation loop
    $ phone_state = "messages"

    label .loop:

        if phone_state == "messages":
            call screen phone_frame("phone_messages_list", all_chats)

            $ action = _return[0]
            $ data = _return[1]

            if action == "open_chat":
                $ current_chat = data
                $ phone_state = "chat"

        elif phone_state == "contacts":
            call screen phone_frame("phone_contacts", all_chats)

            $ action = _return[0]
            $ data = _return[1]

            if action == "open_chat":
                $ current_chat = data
                $ phone_state = "chat"
            elif action == "back":
                $ phone_state = "messages"

        elif phone_state == "chat":
            call chat_loop

        jump .loop

## ===================================================================
## CHAT CONVERSATION LOOP
## ===================================================================

label chat_loop:
    ## Show the chat screen and handle interactions
    label .loop:
        call screen phone_frame("phone_chat", current_chat)

        $ action = _return[0]

        if action == "back":
            $ phone_state = "messages"
            return

        elif action == "type":
            ## Player wants to type a message - use renpy.input
            $ player_msg = renpy.input(
                "Type your message:",
                length=500,
                exclude="{}",
                allow=None
            )
            $ player_msg = player_msg.strip()

            if player_msg:
                ## Send the message and get AI response
                $ current_chat.send_message(player_msg)

        elif action == "send":
            ## Send button pressed without typing first - prompt for input
            $ player_msg = renpy.input(
                "Type your message:",
                length=500,
                exclude="{}",
                allow=None
            )
            $ player_msg = player_msg.strip()

            if player_msg:
                $ current_chat.send_message(player_msg)

    jump .loop
