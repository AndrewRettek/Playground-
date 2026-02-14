## phone_screens.rpy - Phone UI screens styled to match FutaDomWorld aesthetic (1920x1080)

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
define PHONE_TIMESTAMP = "#ffffff44"
define PHONE_READ_COLOR = "#4a6cf766"

## Bold font for headers/names
define PHONE_FONT_BOLD = "gui/fonts/Inter-Bold.ttf"
define PHONE_FONT_SEMI = "gui/fonts/Inter-SemiBold.ttf"


## ===================================================================
## ATL TRANSFORMS
## ===================================================================

## Animated typing indicator - three dots with staggered bounce
transform typing_dot_1:
    alpha 0.3 yoffset 0
    block:
        ease 0.4 alpha 1.0 yoffset -4
        ease 0.4 alpha 0.3 yoffset 0
        repeat

transform typing_dot_2:
    alpha 0.3 yoffset 0
    pause 0.15
    block:
        ease 0.4 alpha 1.0 yoffset -4
        ease 0.4 alpha 0.3 yoffset 0
        repeat

transform typing_dot_3:
    alpha 0.3 yoffset 0
    pause 0.30
    block:
        ease 0.4 alpha 1.0 yoffset -4
        ease 0.4 alpha 0.3 yoffset 0
        repeat

## Phone entrance - static (dissolve transition handles screen switches)
transform phone_entrance:
    alpha 1.0 zoom 1.0


## ===================================================================
## SHARED SUB-SCREENS
## ===================================================================

screen phone_status_bar():
    frame:
        xfill True
        ysize 33
        background Solid(PHONE_STATUSBAR_BG)
        padding (18, 3, 18, 3)
        hbox:
            xfill True
            hbox:
                spacing 9
                yalign 0.5
                add "gui/phone/icon_signal.png" yalign 0.5
                add "gui/phone/icon_wifi.png" yalign 0.5
            text "[get_timestamp()]" size 16 color "#ffffffaa" xalign 0.5 yalign 0.5
            hbox:
                spacing 6
                xalign 1.0
                yalign 0.5
                text "100%" size 15 color "#ffffffaa" yalign 0.5
                add "gui/phone/icon_battery.png" yalign 0.5

screen phone_bottom_bar():
    ## Navigation bar
    frame:
        xfill True
        ysize 66
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
        ysize 30
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
    frame at phone_entrance:
        xalign 0.5
        yalign 0.5
        xsize 630
        ysize 960
        background Frame("gui/phone/phone_body.png", 45, 45, 45, 45)
        padding (3, 3, 3, 3)

        vbox:
            xfill True

            ## Top bezel with camera dot
            frame:
                xfill True
                ysize 39
                background Solid(PHONE_FRAME_COLOR)
                add "gui/phone/camera_dot.png" xalign 0.5 yalign 0.5

            ## Status bar
            use phone_status_bar

            ## Messages header (ornate banner)
            frame:
                xfill True
                ysize 66
                background "images/ui/messages_header.png"
                padding (15, 8, 15, 8)
                hbox:
                    xfill True
                    yalign 0.5
                    text "Messages" color "#ffffff" size 30 xalign 0.5 yalign 0.5 bold True outlines [(2, "#00000088", 0, 0)]

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
                            ysize 108
                            background Frame("gui/phone/contact_card.png", 15, 15, 15, 15)
                            hover_background Frame("gui/phone/contact_card_hover.png", 15, 15, 15, 15)
                            action Return(("open_chat", session))
                            padding (18, 15, 18, 15)

                            hbox:
                                spacing 18
                                xfill True
                                yalign 0.5

                                ## Circular avatar
                                add session.get_circle_avatar() xsize 72 ysize 72 yalign 0.5

                                ## Name and preview
                                vbox:
                                    spacing 5
                                    yalign 0.5
                                    xfill True
                                    text session.character_name color PHONE_CARD_TEXT size 24 font PHONE_FONT_SEMI
                                    text session.get_last_message_preview() color PHONE_CARD_PREVIEW size 20

                                ## Unread badge
                                if session.unread_count > 0:
                                    frame:
                                        xsize 36
                                        ysize 36
                                        xalign 1.0
                                        yalign 0.5
                                        background Solid(session.accent_color)
                                        text str(session.unread_count) color "#ffffff" size 18 font PHONE_FONT_SEMI xalign 0.5 yalign 0.5

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

    ## Play received sound if pending
    if session._sound_pending:
        timer 0.01 action [Play("sound", "audio/message_received.wav"), SetField(session, "_sound_pending", False)]

    ## Background (Midjourney desktop art)
    add "images/ui/desktop_bg.png"

    ## Phone shadow
    add "gui/phone/phone_shadow.png" xalign 0.5 yalign 0.5

    ## Phone body
    frame at phone_entrance:
        xalign 0.5
        yalign 0.5
        xsize 630
        ysize 960
        background Frame("gui/phone/phone_body.png", 45, 45, 45, 45)
        padding (3, 3, 3, 3)

        vbox:
            xfill True

            ## Top bezel with camera dot
            frame:
                xfill True
                ysize 39
                background Solid(PHONE_FRAME_COLOR)
                add "gui/phone/camera_dot.png" xalign 0.5 yalign 0.5

            ## Status bar
            use phone_status_bar

            ## Chat header
            frame:
                xfill True
                ysize 72
                background Solid(PHONE_HEADER_BG)
                padding (12, 9, 18, 9)

                hbox:
                    spacing 15
                    yalign 0.5

                    ## Back button
                    button:
                        yalign 0.5
                        padding (6, 6, 12, 6)
                        background None
                        action Return(("back", None))
                        hbox:
                            spacing 6
                            add "gui/phone/icon_nav_back.png" yalign 0.5
                            text "Back" color session.accent_color size 21 yalign 0.5

                    ## Character avatar
                    add session.get_circle_avatar() xsize 48 ysize 48 yalign 0.5

                    ## Character name + status
                    vbox:
                        yalign 0.5
                        text session.character_name color "#ffffff" size 24 font PHONE_FONT_SEMI
                        text "Online" color session.accent_color size 17

            ## Header accent line (character color)
            frame:
                xfill True
                ysize 3
                background Solid(session.accent_color)

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
                        spacing 9

                        null height 15

                        for msg in session.messages:
                            if msg.sender == "player":
                                ## Player bubble (right-aligned, blue)
                                vbox:
                                    xfill True
                                    hbox:
                                        xfill True
                                        null width 120
                                        frame:
                                            xalign 1.0
                                            xmaximum 450
                                            background Frame("gui/phone/bubble_player.png", 24, 24, 24, 24)
                                            padding (21, 15, 21, 15)
                                            text msg.text color PHONE_TEXT_PLAYER size 21
                                    ## Timestamp + read receipt
                                    hbox:
                                        xalign 1.0
                                        spacing 9
                                        if msg.read:
                                            text "Read" color PHONE_READ_COLOR size 15
                                        text msg.timestamp color PHONE_TIMESTAMP size 15
                            else:
                                ## NPC bubble (left-aligned, dark, with avatar)
                                vbox:
                                    hbox:
                                        spacing 12
                                        xpos 12
                                        add session.get_circle_avatar() xsize 42 ysize 42 yalign 0
                                        frame:
                                            xmaximum 420
                                            background Frame("gui/phone/bubble_npc.png", 24, 24, 24, 24)
                                            padding (21, 15, 21, 15)
                                            text msg.text color PHONE_TEXT_NPC size 21
                                    ## Timestamp
                                    text msg.timestamp color PHONE_TIMESTAMP size 15 xpos 66

                        ## Typing indicator
                        if session.is_loading:
                            hbox:
                                spacing 12
                                xpos 12
                                add session.get_circle_avatar() xsize 42 ysize 42 yalign 0
                                frame:
                                    xmaximum 150
                                    background Frame("gui/phone/bubble_npc.png", 24, 24, 24, 24)
                                    padding (21, 15, 21, 15)
                                    hbox:
                                        spacing 5
                                        yalign 0.5
                                        text "." color PHONE_TEXT_NPC size 27 at typing_dot_1
                                        text "." color PHONE_TEXT_NPC size 27 at typing_dot_2
                                        text "." color PHONE_TEXT_NPC size 27 at typing_dot_3

                        null height 15

            ## Input area
            frame:
                xfill True
                ysize 78
                background Solid(PHONE_INPUT_BG)
                padding (15, 12, 15, 12)

                hbox:
                    spacing 12
                    xfill True
                    yalign 0.5

                    frame:
                        xsize 447
                        ysize 54
                        background Frame("gui/phone/input_field.png", 30, 27, 30, 27)
                        padding (21, 9, 21, 9)
                        input:
                            value ScreenVariableInputValue("msg_input")
                            color "#e0e0e8"
                            size 20
                            yalign 0.5
                            length 500

                    button:
                        xsize 102
                        ysize 54
                        background Frame("gui/phone/send_btn.png", 30, 27, 30, 27)
                        hover_background Frame("gui/phone/send_btn_hover.png", 30, 27, 30, 27)
                        sensitive (not session.is_loading)
                        action Return(("send", msg_input))
                        text "Send" color "#ffffff" size 21 xalign 0.5 yalign 0.5 bold True

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
    frame at phone_entrance:
        xalign 0.5
        yalign 0.5
        xsize 630
        ysize 960
        background Frame("gui/phone/phone_body.png", 45, 45, 45, 45)
        padding (3, 3, 3, 3)

        vbox:
            xfill True

            ## Top bezel with camera dot
            frame:
                xfill True
                ysize 39
                background Solid(PHONE_FRAME_COLOR)
                add "gui/phone/camera_dot.png" xalign 0.5 yalign 0.5

            ## Status bar
            use phone_status_bar

            ## Header with back button
            frame:
                xfill True
                ysize 66
                background Solid(PHONE_HEADER_BG)
                padding (15, 8, 15, 8)
                hbox:
                    xfill True
                    yalign 0.5

                    button:
                        yalign 0.5
                        padding (6, 6, 12, 6)
                        background None
                        action Return(("back", None))
                        hbox:
                            spacing 6
                            add "gui/phone/icon_nav_back.png" yalign 0.5
                            text "Back" color PHONE_ACCENT size 21 yalign 0.5

                    text "Contacts" color "#ffffff" size 30 xalign 0.5 yalign 0.5 bold True

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
                            ysize 120
                            background Frame("gui/phone/contact_card.png", 15, 15, 15, 15)
                            hover_background Frame("gui/phone/contact_card_hover.png", 15, 15, 15, 15)
                            action Return(("open_chat", session))
                            padding (18, 18, 18, 18)

                            hbox:
                                spacing 21
                                yalign 0.5

                                ## Circular avatar (larger on contacts page)
                                add session.get_circle_avatar() xsize 84 ysize 84 yalign 0.5

                                ## Name
                                text session.character_name color PHONE_CARD_TEXT size 27 bold True yalign 0.5

                        ## Thin divider
                        frame:
                            xfill True
                            ysize 1
                            background Solid(PHONE_DIVIDER)

            ## Bottom bar
            use phone_bottom_bar
