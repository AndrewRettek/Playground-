## phone_screens.rpy - Phone UI screens styled to match FutaDomWorld aesthetic

## ===================================================================
## COLOR CONSTANTS
## ===================================================================
define PHONE_BG = "#1a5276"
define PHONE_STATUSBAR_BG = "#0d2f44"
define PHONE_HEADER_BG = "#0d2f44"
define PHONE_INPUT_BG = "#0d2f44"
define PHONE_BUBBLE_PLAYER = "#4a90d9"
define PHONE_BUBBLE_NPC = "#e8e8e8"
define PHONE_TEXT_PLAYER = "#ffffff"
define PHONE_TEXT_NPC = "#222222"
define PHONE_ACCENT = "#4fc3f7"
define PHONE_NAV_BG = "#111111"
define PHONE_FRAME_COLOR = "#222222"


## ===================================================================
## MESSAGES LIST SCREEN
## ===================================================================
screen phone_messages_list(chat_sessions):
    modal True

    add Solid("#00000088")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 700
        background Solid(PHONE_FRAME_COLOR)
        padding (0, 0, 0, 0)

        vbox:
            xfill True

            ## Top bezel
            frame:
                xfill True
                ysize 28
                background Solid(PHONE_FRAME_COLOR)
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 10 ysize 10

            ## Status bar
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_STATUSBAR_BG)
                padding (12, 2, 12, 2)
                hbox:
                    xfill True
                    text "||||" size 11 color "#ffffff" yalign 0.5
                    text "  WiFi" size 11 color "#ffffff" yalign 0.5
                    null
                    text "100%" size 11 color "#ffffff" xalign 1.0 yalign 0.5

            ## Messages header
            frame:
                xfill True
                ysize 40
                background Solid(PHONE_HEADER_BG)
                padding (10, 5, 10, 5)
                text "Messages" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True

            ## Contact list
            vbox:
                xfill True

                for session in chat_sessions:
                    button:
                        xfill True
                        ysize 80
                        background Solid("#d4e6f1")
                        hover_background Solid("#aed6f1")
                        action Return(("open_chat", session))
                        padding (8, 8, 8, 8)

                        hbox:
                            spacing 12
                            yalign 0.5

                            ## Character avatar
                            add session.avatar xsize 60 ysize 60 yalign 0.5

                            ## Name and preview
                            vbox:
                                spacing 4
                                text session.character_name color "#222222" size 18 bold True
                                text session.get_last_message_preview() color "#666666" size 14

            ## Spacer fills remaining area with phone background
            frame:
                xfill True
                yfill True
                background Solid(PHONE_BG)

            ## Bottom nav
            frame:
                xfill True
                ysize 36
                background Solid(PHONE_NAV_BG)
                hbox:
                    xfill True
                    yalign 0.5
                    textbutton "|||" action NullAction() xalign 0.25 text_size 16 text_color "#888888"
                    textbutton "O" action NullAction() xalign 0.5 text_size 16 text_color "#888888"
                    textbutton "V" action NullAction() xalign 0.75 text_size 16 text_color "#888888"

            ## Bottom bezel
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_FRAME_COLOR)
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 14 ysize 14


## ===================================================================
## CHAT SCREEN
## ===================================================================
screen phone_chat(session):
    modal True

    add Solid("#00000088")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 700
        background Solid(PHONE_FRAME_COLOR)
        padding (0, 0, 0, 0)

        vbox:
            xfill True

            ## Top bezel
            frame:
                xfill True
                ysize 28
                background Solid(PHONE_FRAME_COLOR)
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 10 ysize 10

            ## Status bar
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_STATUSBAR_BG)
                padding (12, 2, 12, 2)
                hbox:
                    xfill True
                    text "||||" size 11 color "#ffffff" yalign 0.5
                    text "  WiFi" size 11 color "#ffffff" yalign 0.5
                    null
                    text "100%" size 11 color "#ffffff" xalign 1.0 yalign 0.5

            ## Chat header
            frame:
                xfill True
                ysize 44
                background Solid(PHONE_HEADER_BG)
                padding (6, 4, 10, 4)

                hbox:
                    spacing 8
                    yalign 0.5

                    textbutton "< Back" action Return(("back", None)):
                        text_size 14
                        text_color PHONE_ACCENT

                    add session.avatar xsize 32 ysize 32 yalign 0.5

                    text session.character_name color "#ffffff" size 17 bold True yalign 0.5

            ## Message area
            viewport id "chat_viewport":
                xfill True
                yfill True
                mousewheel True
                draggable True
                yinitial 1.0

                vbox:
                    xfill True
                    spacing 6

                    null height 8

                    for msg in session.messages:
                        if msg.sender == "player":
                            hbox:
                                xfill True
                                null width 80
                                frame:
                                    xalign 1.0
                                    xmaximum 300
                                    background Solid(PHONE_BUBBLE_PLAYER)
                                    padding (12, 8, 12, 8)
                                    text msg.text color PHONE_TEXT_PLAYER size 15
                        else:
                            hbox:
                                spacing 6
                                xpos 8
                                add session.avatar xsize 28 ysize 28 yalign 0.0
                                frame:
                                    xmaximum 280
                                    background Solid(PHONE_BUBBLE_NPC)
                                    padding (12, 8, 12, 8)
                                    text msg.text color PHONE_TEXT_NPC size 15

                    if session.is_loading:
                        hbox:
                            spacing 6
                            xpos 8
                            add session.avatar xsize 28 ysize 28 yalign 0.0
                            frame:
                                xmaximum 100
                                background Solid(PHONE_BUBBLE_NPC)
                                padding (12, 8, 12, 8)
                                text "..." color PHONE_TEXT_NPC size 15

                    null height 8

            ## Input area
            frame:
                xfill True
                ysize 52
                background Solid(PHONE_INPUT_BG)
                padding (8, 6, 8, 6)

                hbox:
                    spacing 6
                    xfill True
                    yalign 0.5

                    button:
                        xsize 300
                        ysize 36
                        background Solid("#1a3a4f")
                        padding (10, 6, 10, 6)
                        action Return(("type", None))
                        text "Type a message..." color "#888888" size 14 yalign 0.5

                    textbutton "Send":
                        xsize 70
                        ysize 36
                        text_size 15
                        text_color "#ffffff"
                        background Solid(PHONE_ACCENT)
                        action Return(("send", None))

            ## Bottom nav
            frame:
                xfill True
                ysize 36
                background Solid(PHONE_NAV_BG)
                hbox:
                    xfill True
                    yalign 0.5
                    textbutton "|||" action NullAction() xalign 0.25 text_size 16 text_color "#888888"
                    textbutton "O" action NullAction() xalign 0.5 text_size 16 text_color "#888888"
                    textbutton "V" action NullAction() xalign 0.75 text_size 16 text_color "#888888"

            ## Bottom bezel
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_FRAME_COLOR)
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 14 ysize 14


## ===================================================================
## CONTACTS SCREEN
## ===================================================================
screen phone_contacts(chat_sessions):
    modal True

    add Solid("#00000088")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 700
        background Solid(PHONE_FRAME_COLOR)
        padding (0, 0, 0, 0)

        vbox:
            xfill True

            ## Top bezel
            frame:
                xfill True
                ysize 28
                background Solid(PHONE_FRAME_COLOR)
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 10 ysize 10

            ## Status bar
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_STATUSBAR_BG)
                padding (12, 2, 12, 2)
                hbox:
                    xfill True
                    text "||||" size 11 color "#ffffff" yalign 0.5
                    text "  WiFi" size 11 color "#ffffff" yalign 0.5
                    null
                    text "100%" size 11 color "#ffffff" xalign 1.0 yalign 0.5

            ## Header
            frame:
                xfill True
                ysize 40
                background Solid(PHONE_HEADER_BG)
                padding (10, 5, 10, 5)
                text "Contacts" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True

            ## Contact list
            vbox:
                xfill True
                spacing 2

                for session in chat_sessions:
                    button:
                        xfill True
                        ysize 90
                        background Solid("#d4e6f1")
                        hover_background Solid("#aed6f1")
                        action Return(("open_chat", session))
                        padding (10, 10, 10, 10)

                        hbox:
                            spacing 14
                            yalign 0.5
                            add session.avatar xsize 66 ysize 66 yalign 0.5
                            text session.character_name color "#222222" size 20 bold True yalign 0.5

            ## Spacer
            frame:
                xfill True
                yfill True
                background Solid(PHONE_BG)

            ## Bottom nav
            frame:
                xfill True
                ysize 36
                background Solid(PHONE_NAV_BG)
                hbox:
                    xfill True
                    yalign 0.5
                    textbutton "|||" action NullAction() xalign 0.25 text_size 16 text_color "#888888"
                    textbutton "O" action NullAction() xalign 0.5 text_size 16 text_color "#888888"
                    textbutton "V" action NullAction() xalign 0.75 text_size 16 text_color "#888888"

            ## Bottom bezel
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_FRAME_COLOR)
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 14 ysize 14
