## phone_screens.rpy - Phone UI screens for BindrChat (1280x720)

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
define PHONE_TIMESTAMP = "#ffffff88"
define PHONE_READ_COLOR = "#4a6cf766"

## Warm dating-sim accent colors
define PHONE_ACCENT_WARM = "#E8849A"    ## Rose pink — dating sim accent
define PHONE_HEART_COLOR = "#FF6B8A"    ## Brighter pink for hearts (fallback)
define PHONE_BADGE_COLOR = "#E8849A"    ## Unread notification badge

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
        ease 0.4 alpha 1.0 yoffset -3
        ease 0.4 alpha 0.3 yoffset 0
        repeat

transform typing_dot_2:
    alpha 0.3 yoffset 0
    pause 0.15
    block:
        ease 0.4 alpha 1.0 yoffset -3
        ease 0.4 alpha 0.3 yoffset 0
        repeat

transform typing_dot_3:
    alpha 0.3 yoffset 0
    pause 0.30
    block:
        ease 0.4 alpha 1.0 yoffset -3
        ease 0.4 alpha 0.3 yoffset 0
        repeat

## Floating heart transforms — staggered float-up with fade
transform heart_float_1:
    alpha 1.0 yoffset 0 xoffset 0
    ease 1.6 alpha 0.0 yoffset -120 xoffset -30

transform heart_float_2:
    alpha 0.0 yoffset 0 xoffset 0
    pause 0.2
    alpha 1.0
    ease 1.5 alpha 0.0 yoffset -100 xoffset 25

transform heart_float_3:
    alpha 0.0 yoffset 0 xoffset 0
    pause 0.35
    alpha 1.0
    ease 1.8 alpha 0.0 yoffset -140 xoffset -10

transform heart_float_4:
    alpha 0.0 yoffset 0 xoffset 0
    pause 0.5
    alpha 1.0
    ease 1.7 alpha 0.0 yoffset -90 xoffset 40

transform heart_float_5:
    alpha 0.0 yoffset 0 xoffset 0
    pause 0.65
    alpha 1.0
    ease 2.0 alpha 0.0 yoffset -150 xoffset -20

## Portrait entrance - fade in from left
transform portrait_entrance:
    alpha 0.0 xoffset -30
    ease 0.5 alpha 1.0 xoffset 0

## Phone entrance - static (dissolve transition handles screen switches)
transform phone_entrance:
    alpha 1.0 zoom 1.0


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
            text "[get_timestamp()]" size 12 color "#ffffffaa" xalign 0.5 yalign 0.5
            hbox:
                spacing 4
                xalign 1.0
                yalign 0.5
                text "100%" size 11 color "#ffffffaa" yalign 0.5
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
    frame at phone_entrance:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 540
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
                    text "Messages" color "#ffffff" size 22 xalign 0.5 yalign 0.5 bold True outlines [(1, "#00000088", 0, 0)]

            ## Rose accent line below header (dating sim warmth)
            frame:
                xfill True
                ysize 2
                background Solid(PHONE_ACCENT_WARM)

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
                                xfill True
                                yalign 0.5

                                ## Circular avatar
                                add session.get_circle_avatar() xsize 48 ysize 48 yalign 0.5

                                ## Name and preview
                                vbox:
                                    spacing 3
                                    yalign 0.5
                                    xfill True
                                    text session.character_name color PHONE_CARD_TEXT size 18 font PHONE_FONT_SEMI
                                    text session.get_last_message_preview() color PHONE_CARD_PREVIEW size 14

                                ## Unread badge (warm rose — dating sim style)
                                if session.unread_count > 0:
                                    frame:
                                        xsize 24
                                        ysize 24
                                        xalign 1.0
                                        yalign 0.5
                                        background Solid(PHONE_BADGE_COLOR)
                                        text str(session.unread_count) color "#ffffff" size 13 font PHONE_FONT_SEMI xalign 0.5 yalign 0.5

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

    ## Auto-scroll chat to bottom when new messages arrive
    if session._needs_scroll:
        timer 0.01 action [Function(session._chat_adj.change, 99999), SetField(session, "_needs_scroll", False)]

    ## Background (Midjourney desktop art)
    add "images/ui/desktop_bg.png"

    ## Character portrait (left side of phone, with entrance animation)
    if session.get_portrait():
        add session.get_portrait() at portrait_entrance zoom 0.85 xpos 30 yalign 0.95

    ## Phone shadow
    add "gui/phone/phone_shadow.png" xalign 0.5 yalign 0.5

    ## Phone body
    frame at phone_entrance:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 540
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

                ## Left side: back, avatar, name
                hbox:
                    spacing 10
                    yalign 0.5

                    ## Back button (subtle pill background)
                    button:
                        yalign 0.5
                        padding (4, 4, 8, 4)
                        background Solid("#ffffff11")
                        hover_background Solid("#ffffff22")
                        action Return(("back", None))
                        hbox:
                            spacing 4
                            add "gui/phone/icon_nav_back.png" yalign 0.5
                            text "Back" color session.accent_color size 16 yalign 0.5

                    ## Character avatar
                    add session.get_circle_avatar() xsize 32 ysize 32 yalign 0.5

                    ## Character name + status
                    vbox:
                        yalign 0.5
                        text session.character_name color "#ffffff" size 18 font PHONE_FONT_SEMI
                        if session.is_loading:
                            text "Typing..." color session.accent_color size 13
                        else:
                            text "Online" color session.accent_color size 13

                ## Reset conversation button (right-aligned)
                button:
                    xalign 1.0
                    yalign 0.5
                    padding (8, 5, 8, 5)
                    background Solid("#ff4444aa")
                    hover_background Solid("#ff6666cc")
                    action Return(("reset", None))
                    text "Clear" color "#ffffff" size 13 bold True

            ## Header accent line (character color)
            frame:
                xfill True
                ysize 2
                background Solid(session.accent_color)

            ## Message area (with dark damask texture)
            frame:
                xfill True
                yfill True
                background Frame("images/ui/chat_bg.png", 0, 0, 0, 0)
                padding (0, 0, 0, 0)

                viewport id "chat_viewport" yadjustment session._chat_adj:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True

                    vbox:
                        xfill True
                        spacing 10

                        null height 10

                        for msg in session.messages:
                            if msg.sender == "player":
                                ## Player bubble (right-aligned, blue)
                                vbox:
                                    xfill True
                                    hbox:
                                        xfill True
                                        null width 80
                                        frame:
                                            xalign 1.0
                                            xmaximum 290
                                            background Frame("gui/phone/bubble_player.png", 16, 16, 16, 16)
                                            padding (14, 10, 14, 10)
                                            text msg.text color PHONE_TEXT_PLAYER size 16
                                    ## Timestamp + read receipt
                                    hbox:
                                        xalign 1.0
                                        spacing 6
                                        if msg.read:
                                            text "Read" color PHONE_READ_COLOR size 11
                                        text msg.timestamp color PHONE_TIMESTAMP size 11
                            else:
                                ## NPC bubble (left-aligned, dark, with avatar)
                                vbox:
                                    hbox:
                                        spacing 8
                                        xpos 8
                                        add session.get_circle_avatar() xsize 28 ysize 28 yalign 0
                                        frame:
                                            xmaximum 290
                                            background Frame("gui/phone/bubble_npc.png", 16, 16, 16, 16)
                                            padding (14, 10, 14, 10)
                                            text msg.text color PHONE_TEXT_NPC size 16
                                    ## Timestamp
                                    text msg.timestamp color PHONE_TIMESTAMP size 11 xpos 44

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
                                    hbox:
                                        spacing 3
                                        yalign 0.5
                                        text "." color PHONE_TEXT_NPC size 20 at typing_dot_1
                                        text "." color PHONE_TEXT_NPC size 20 at typing_dot_2
                                        text "." color PHONE_TEXT_NPC size 20 at typing_dot_3

                        null height 10

            ## Input area
            frame:
                xfill True
                yminimum 52
                background Solid(PHONE_INPUT_BG)
                padding (10, 8, 10, 8)

                hbox:
                    spacing 8
                    xfill True

                    frame:
                        xsize 298
                        yminimum 36
                        background Frame("gui/phone/input_field.png", 20, 18, 20, 18)
                        padding (14, 6, 14, 6)
                        input:
                            value ScreenVariableInputValue("msg_input")
                            color "#e0e0e8"
                            size 15
                            xfill True
                            length 500

                    button:
                        xsize 68
                        ysize 36
                        yalign 0.5
                        background Frame("gui/phone/send_btn.png", 20, 18, 20, 18)
                        hover_background Frame("gui/phone/send_btn_hover.png", 20, 18, 20, 18)
                        sensitive (not session.is_loading)
                        action Return(("send", msg_input))
                        text "Send" color "#ffffff" size 16 xalign 0.5 yalign 0.5 bold True

            if not session.is_loading:
                key "input_enter" action Return(("send", msg_input))

            ## Bottom bar
            use phone_bottom_bar

    ## Floating affection hearts (drawn AFTER phone so they appear on top)
    if session._hearts_pending:
        timer 0.01 action SetField(session, "_hearts_pending", False)
        fixed:
            xalign 0.5
            yalign 0.55
            text "\u2665" at heart_float_1 color session.accent_color size 28
            text "\u2665" at heart_float_2 color session.accent_color size 24
            text "\u2665" at heart_float_3 color session.accent_color size 30
            text "\u2665" at heart_float_4 color session.accent_color size 26
            text "\u2665" at heart_float_5 color session.accent_color size 32


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
        xsize 420
        ysize 540
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
                            text "Back" color PHONE_ACCENT size 16 yalign 0.5

                    text "Contacts" color "#ffffff" size 22 xalign 0.5 yalign 0.5 bold True

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
                                text session.character_name color PHONE_CARD_TEXT size 20 bold True yalign 0.5

                        ## Thin divider
                        frame:
                            xfill True
                            ysize 1
                            background Solid(PHONE_DIVIDER)

            ## Bottom bar
            use phone_bottom_bar
