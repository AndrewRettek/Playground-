## script.rpy - Main game script

## ===================================================================
## CHARACTER LIST - Add new characters here after defining them
## in characters.rpy
## ===================================================================

default all_chats = [mallory_chat, rye_chat, demitria_chat, gabby_chat]
## When you add more characters in characters.rpy, add them here:
## default all_chats = [mallory_chat, char2_chat, char3_chat]

## Track which screen we're on
default phone_state = "messages"
default current_chat = None

## Phone screen transition
define phone_transition = Dissolve(0.25)

## ===================================================================
## MAIN GAME FLOW
## ===================================================================

label start:
    call phone_main
    return

## ===================================================================
## SUBSCRIPTION KEY FLOW (called from main menu)
## ===================================================================

label subscription_flow:
    label .loop:
        call screen subscription

        if _return == "enter_key":
            $ key = renpy.input("Enter your subscription key:", length=128, exclude="{}")
            $ key = key.strip()
            if key:
                $ set_player_token(key)
                $ renpy.notify("Subscription key saved!")
            jump .loop

        elif _return == "clear_key":
            $ clear_subscription_key()
            jump .loop

        elif _return == "back":
            return

## ===================================================================
## PHONE MAIN LOOP
## ===================================================================

label phone_main:
    $ phone_state = "messages"

    label .loop:

        if phone_state == "messages":
            $ renpy.transition(phone_transition)
            call screen phone_messages_list(all_chats)

            $ action = _return[0]
            $ data = _return[1]

            if action == "open_chat":
                $ current_chat = data
                $ phone_state = "chat"

        elif phone_state == "contacts":
            $ renpy.transition(phone_transition)
            call screen phone_contacts(all_chats)

            $ action = _return[0]
            $ data = _return[1]

            if action == "open_chat":
                $ current_chat = data
                $ phone_state = "chat"
            elif action == "back":
                $ phone_state = "messages"

        elif phone_state == "chat":
            $ renpy.transition(phone_transition)
            call chat_loop

        jump .loop

## ===================================================================
## CHAT CONVERSATION LOOP
## ===================================================================

label chat_loop:
    label .loop:
        call screen phone_chat(current_chat)

        $ action = _return[0]

        if action == "back":
            $ phone_state = "messages"
            return

        elif action == "send":
            $ player_msg = _return[1].strip() if _return[1] else ""
            if player_msg:
                $ current_chat.send_message(player_msg)

    jump .loop
