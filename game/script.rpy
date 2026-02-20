## script.rpy - Main game script

## ===================================================================
## CHARACTER LIST - Add new characters here after defining them
## in characters.rpy
## ===================================================================

## all_chats is defined in characters.rpy (init 1 python block)
## Add new characters there after defining their ChatSession.

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
## SAVE MIGRATION - Handles old saves with previous ChatSession format
## ===================================================================

label after_load:
    python:
        if not hasattr(mallory_chat, 'config'):
            mallory_chat = ChatSession(CHARACTERS["Mallory"])
            rye_chat = ChatSession(CHARACTERS["Rye"])
            demitria_chat = ChatSession(CHARACTERS["Demitria"])
            gabby_chat = ChatSession(CHARACTERS["Gabby"])
            all_chats = [mallory_chat, rye_chat, demitria_chat, gabby_chat]
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
    ## Mark messages as read when entering chat
    $ current_chat.is_active = True
    $ current_chat.mark_read()

    label .loop:
        call screen phone_chat(current_chat)

        $ action = _return[0]

        if action == "back":
            $ current_chat.is_active = False
            $ phone_state = "messages"
            return

        elif action == "send":
            $ player_msg = _return[1].strip() if _return[1] else ""
            if player_msg:
                $ renpy.play("audio/message_sent.wav", channel="sound")
                $ current_chat.send_message(player_msg)

        elif action == "reset":
            $ current_chat.reset()

    jump .loop
