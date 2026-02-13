## phone_screens.rpy - Phone UI screens styled to match FutaDomWorld aesthetic

## ===================================================================
## COLOR CONSTANTS
## ===================================================================
define PHONE_BG = "#0f0f1a"
define PHONE_STATUSBAR_BG = "#141425"
define PHONE_HEADER_BG = "#141425"
define PHONE_INPUT_BG = "#141425"
define PHONE_BUBBLE_PLAYER = "#4a6cf7"
define PHONE_BUBBLE_NPC = "#2b2d42"
define PHONE_TEXT_PLAYER = "#ffffff"
define PHONE_TEXT_NPC = "#e0e0e8"
define PHONE_ACCENT = "#4a6cf7"
define PHONE_NAV_BG = "#0a0a14"
define PHONE_FRAME_COLOR = "#1a1a2e"
define PHONE_CARD_TEXT = "#ffffff"
define PHONE_CARD_PREVIEW = "#8b8da0"
define PHONE_DIVIDER = "#2d2d4a"


## ===================================================================
## SHARED SUB-SCREENS
## ===================================================================

screen phone_status_bar():
    frame:
        xfill True
        ysize 22
        background Solid(PHONE_STATUSBAR_BG)
        padding (12, 2, 12, 2)
        hbox:
            xfill True
            hbox:
                spacing 6
                yalign 0.5
                add "gui/phone/icon_signal.png" yalign 0.5
                add "gui/phone/icon_wifi.png" yalign 0.5
            text "12:34" size 11 color "#ffffffaa" xalign 0.5 yalign 0.5
            hbox:
                spacing 4
                xalign 1.0
                yalign 0.5
                text "100%" size 10 color "#ffffffaa" yalign 0.5
                add "gui/phone/icon_battery.png" yalign 0.5

screen phone_bottom_bar():
    ## Navigation bar
    frame:
        xfill True
        ysize 44
        background Solid(PHONE_NAV_BG)
        padding (0, 0, 0, 0)
        hbox:
            xfill True
            yalign 0.5
            fixed:
                xfill True
                yfit True
                add "gui/phone/icon_nav_back.png" xalign 0.2 yalign 0.5
                add "gui/phone/icon_nav_circle.png" xalign 0.5 yalign 0.5
                add "gui/phone/icon_nav_square.png" xalign 0.8 yalign 0.5

    ## Bottom bezel with home indicator
    frame:
        xfill True
        ysize 20
        background Solid(PHONE_FRAME_COLOR)
        add "gui/phone/home_indicator.png" xalign 0.5 yalign 0.6


## ===================================================================
## MESSAGES LIST SCREEN
## ===================================================================
screen phone_messages_list(chat_sessions):
    modal True

    ## Background (Midjourney desktop art)
    add "images/ui/desktop_bg.png"

    ## Phone shadow
    add "gui/phone/phone_shadow.png" xalign 0.5 yalign 0.5

    ## Phone body
    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 640
        background Frame("gui/phone/phone_body.png", 30, 30, 30, 30)
        padding (2, 2, 2, 2)

        vbox:
            xfill True

            ## Top bezel with camera dot
            frame:
                xfill True
                ysize 26
                background Solid(PHONE_FRAME_COLOR)
                add "gui/phone/camera_dot.png" xalign 0.5 yalign 0.5

            ## Status bar
            use phone_status_bar

            ## Messages header (ornate banner)
            frame:
                xfill True
                ysize 44
                background "images/ui/messages_header.png"
                padding (10, 5, 10, 5)
                hbox:
                    xfill True
                    yalign 0.5
                    text "Messages" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True outlines [(1, "#00000088", 0, 0)]

            ## Thin divider
            frame:
                xfill True
                ysize 1
                background Solid(PHONE_DIVIDER)

            ## Contact list (scrollable)
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True

                vbox:
                    xfill True

                    for session in chat_sessions:
                        button:
                            xfill True
                            ysize 72
                            background Frame("gui/phone/contact_card.png", 10, 10, 10, 10)
                            hover_background Frame("gui/phone/contact_card_hover.png", 10, 10, 10, 10)
                            action Return(("open_chat", session))
                            padding (12, 10, 12, 10)

                            hbox:
                                spacing 12
                                yalign 0.5

                                ## Circular avatar
                                add session.get_circle_avatar() xsize 48 ysize 48 yalign 0.5

                                ## Name and preview
                                vbox:
                                    spacing 3
                                    yalign 0.5
                                    text session.character_name color PHONE_CARD_TEXT size 16 bold True
                                    text session.get_last_message_preview() color PHONE_CARD_PREVIEW size 13

                        ## Thin divider between contacts
                        frame:
                            xfill True
                            ysize 1
                            background Solid(PHONE_DIVIDER)

            ## Bottom bar
            use phone_bottom_bar


## ===================================================================
## CHAT SCREEN
## ===================================================================
screen phone_chat(session):
    modal True

    default msg_input = ""

    ## Background (Midjourney desktop art)
    add "images/ui/desktop_bg.png"

    ## Phone shadow
    add "gui/phone/phone_shadow.png" xalign 0.5 yalign 0.5

    ## Phone body
    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 640
        background Frame("gui/phone/phone_body.png", 30, 30, 30, 30)
        padding (2, 2, 2, 2)

        vbox:
            xfill True

            ## Top bezel with camera dot
            frame:
                xfill True
                ysize 26
                background Solid(PHONE_FRAME_COLOR)
                add "gui/phone/camera_dot.png" xalign 0.5 yalign 0.5

            ## Status bar
            use phone_status_bar

            ## Chat header
            frame:
                xfill True
                ysize 48
                background Solid(PHONE_HEADER_BG)
                padding (8, 6, 12, 6)

                hbox:
                    spacing 10
                    yalign 0.5

                    ## Back button
                    button:
                        yalign 0.5
                        padding (4, 4, 8, 4)
                        background None
                        action Return(("back", None))
                        hbox:
                            spacing 4
                            add "gui/phone/icon_nav_back.png" yalign 0.5
                            text "Back" color PHONE_ACCENT size 14 yalign 0.5

                    ## Character avatar
                    add session.get_circle_avatar() xsize 32 ysize 32 yalign 0.5

                    ## Character name + status
                    vbox:
                        yalign 0.5
                        text session.character_name color "#ffffff" size 16 bold True
                        text "Online" color "#43b581" size 11

            ## Thin divider
            frame:
                xfill True
                ysize 1
                background Solid(PHONE_DIVIDER)

            ## Message area (with dark damask texture)
            frame:
                xfill True
                yfill True
                background Frame("images/ui/chat_bg.png", 0, 0, 0, 0)
                padding (0, 0, 0, 0)

                viewport id "chat_viewport":
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True
                    yinitial 1.0

                    vbox:
                        xfill True
                        spacing 6

                        null height 10

                        for msg in session.messages:
                            if msg.sender == "player":
                                ## Player bubble (right-aligned, blue)
                                hbox:
                                    xfill True
                                    null width 80
                                    frame:
                                        xalign 1.0
                                        xmaximum 300
                                        background Frame("gui/phone/bubble_player.png", 16, 16, 16, 16)
                                        padding (14, 10, 14, 10)
                                        text msg.text color PHONE_TEXT_PLAYER size 14
                            else:
                                ## NPC bubble (left-aligned, dark, with avatar)
                                hbox:
                                    spacing 8
                                    xpos 8
                                    add session.get_circle_avatar() xsize 28 ysize 28 yalign 0
                                    frame:
                                        xmaximum 280
                                        background Frame("gui/phone/bubble_npc.png", 16, 16, 16, 16)
                                        padding (14, 10, 14, 10)
                                        text msg.text color PHONE_TEXT_NPC size 14

                        ## Typing indicator
                        if session.is_loading:
                            hbox:
                                spacing 8
                                xpos 8
                                add session.get_circle_avatar() xsize 28 ysize 28 yalign 0
                                frame:
                                    xmaximum 100
                                    background Frame("gui/phone/bubble_npc.png", 16, 16, 16, 16)
                                    padding (14, 10, 14, 10)
                                    text "..." color PHONE_TEXT_NPC size 14

                        null height 10

            ## Input area
            frame:
                xfill True
                ysize 52
                background Solid(PHONE_INPUT_BG)
                padding (10, 8, 10, 8)

                hbox:
                    spacing 8
                    xfill True
                    yalign 0.5

                    frame:
                        xsize 298
                        ysize 36
                        background Frame("gui/phone/input_field.png", 20, 18, 20, 18)
                        padding (14, 6, 14, 6)
                        input:
                            value ScreenVariableInputValue("msg_input")
                            color "#e0e0e8"
                            size 13
                            yalign 0.5
                            length 500

                    button:
                        xsize 68
                        ysize 36
                        background Frame("gui/phone/send_btn.png", 20, 18, 20, 18)
                        hover_background Frame("gui/phone/send_btn_hover.png", 20, 18, 20, 18)
                        sensitive (not session.is_loading)
                        action Return(("send", msg_input))
                        text "Send" color "#ffffff" size 14 xalign 0.5 yalign 0.5 bold True

            if not session.is_loading:
                key "input_enter" action Return(("send", msg_input))

            ## Bottom bar
            use phone_bottom_bar


## ===================================================================
## CONTACTS SCREEN
## ===================================================================
screen phone_contacts(chat_sessions):
    modal True

    ## Background (Midjourney desktop art)
    add "images/ui/desktop_bg.png"

    ## Phone shadow
    add "gui/phone/phone_shadow.png" xalign 0.5 yalign 0.5

    ## Phone body
    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 640
        background Frame("gui/phone/phone_body.png", 30, 30, 30, 30)
        padding (2, 2, 2, 2)

        vbox:
            xfill True

            ## Top bezel with camera dot
            frame:
                xfill True
                ysize 26
                background Solid(PHONE_FRAME_COLOR)
                add "gui/phone/camera_dot.png" xalign 0.5 yalign 0.5

            ## Status bar
            use phone_status_bar

            ## Header with back button
            frame:
                xfill True
                ysize 44
                background Solid(PHONE_HEADER_BG)
                padding (10, 5, 10, 5)
                hbox:
                    xfill True
                    yalign 0.5

                    button:
                        yalign 0.5
                        padding (4, 4, 8, 4)
                        background None
                        action Return(("back", None))
                        hbox:
                            spacing 4
                            add "gui/phone/icon_nav_back.png" yalign 0.5
                            text "Back" color PHONE_ACCENT size 14 yalign 0.5

                    text "Contacts" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True

            ## Thin divider
            frame:
                xfill True
                ysize 1
                background Solid(PHONE_DIVIDER)

            ## Contact list (scrollable)
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True

                vbox:
                    xfill True

                    for session in chat_sessions:
                        button:
                            xfill True
                            ysize 80
                            background Frame("gui/phone/contact_card.png", 10, 10, 10, 10)
                            hover_background Frame("gui/phone/contact_card_hover.png", 10, 10, 10, 10)
                            action Return(("open_chat", session))
                            padding (12, 12, 12, 12)

                            hbox:
                                spacing 14
                                yalign 0.5

                                ## Circular avatar (larger on contacts page)
                                add session.get_circle_avatar() xsize 56 ysize 56 yalign 0.5

                                ## Name
                                text session.character_name color PHONE_CARD_TEXT size 18 bold True yalign 0.5

                        ## Thin divider
                        frame:
                            xfill True
                            ysize 1
                            background Solid(PHONE_DIVIDER)

            ## Bottom bar
            use phone_bottom_bar
