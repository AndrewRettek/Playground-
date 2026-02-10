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
## PHONE FRAME - The outer phone shell
## ===================================================================
screen phone_frame(content_screen, *args, **kwargs):
    modal True

    ## Darken background
    add Solid("#00000088")

    ## Phone body - centered on screen
    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ysize 700
        background Solid(PHONE_FRAME_COLOR)
        padding (0, 0, 0, 0)

        vbox:
            xfill True
            yfill True

            ## Top bezel with camera notch
            frame:
                xfill True
                ysize 28
                background Solid(PHONE_FRAME_COLOR)
                ## Camera dot
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 10 ysize 10

            ## Status bar (signal, wifi, battery)
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_STATUSBAR_BG)
                padding (12, 2, 12, 2)
                hbox:
                    xfill True
                    ## Left side - signal bars
                    text "||||" size 11 color "#ffffff" yalign 0.5
                    text "  WiFi" size 11 color "#ffffff" yalign 0.5
                    null width 10
                    ## Spacer
                    null
                    ## Right side - battery
                    text "100%" size 11 color "#ffffff" xalign 1.0 yalign 0.5

            ## Main content area - uses the passed screen
            frame:
                xfill True
                ysize 588
                background Solid(PHONE_BG)
                padding (0, 0, 0, 0)
                use expression content_screen pass (*args, **kwargs)

            ## Bottom navigation bar
            frame:
                xfill True
                ysize 36
                background Solid(PHONE_NAV_BG)
                padding (0, 0, 0, 0)
                hbox:
                    xfill True
                    yalign 0.5
                    ## Three-button nav (Back, Home, Recent)
                    textbutton "|||" action NullAction() xalign 0.25 text_size 16 text_color "#888888"
                    textbutton "O" action NullAction() xalign 0.5 text_size 16 text_color "#888888"
                    textbutton "V" action NullAction() xalign 0.75 text_size 16 text_color "#888888"

            ## Bottom bezel with home button
            frame:
                xfill True
                ysize 24
                background Solid(PHONE_FRAME_COLOR)
                ## Home button circle
                add Solid("#444444") xalign 0.5 yalign 0.5 xsize 14 ysize 14


## ===================================================================
## MESSAGES LIST SCREEN - Shows contacts with last message
## ===================================================================
screen phone_messages_list(chat_sessions):
    tag phone_content

    vbox:
        xfill True
        yfill True

        ## Header
        frame:
            xfill True
            ysize 40
            background Solid(PHONE_HEADER_BG)
            padding (10, 5, 10, 5)
            text "Messages" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True

        ## Contact list - scrollable
        viewport:
            xfill True
            ysize 548
            mousewheel True
            scrollbars "vertical"

            vbox:
                xfill True
                spacing 2

                for session in chat_sessions:
                    button:
                        xfill True
                        ysize 80
                        background "#d4e6f1"
                        hover_background "#aed6f1"
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


## ===================================================================
## CHAT SCREEN - Active conversation with a character
## ===================================================================
screen phone_chat(session):
    tag phone_content

    ## We need a variable to track the input text
    default chat_input_text = ""

    vbox:
        xfill True
        yfill True

        ## Chat header with back button and character name
        frame:
            xfill True
            ysize 44
            background Solid(PHONE_HEADER_BG)
            padding (6, 4, 10, 4)

            hbox:
                spacing 8
                yalign 0.5

                ## Back button
                textbutton "< Back" action Return(("back", None)):
                    text_size 14
                    text_color PHONE_ACCENT

                ## Character avatar (small)
                add session.avatar xsize 32 ysize 32 yalign 0.5

                ## Character name
                text session.character_name color "#ffffff" size 17 bold True yalign 0.5

        ## Message area - scrollable
        viewport id "chat_viewport":
            xfill True
            ysize 492
            mousewheel True
            draggable True
            yinitial 1.0
            scrollbars "vertical"

            vbox:
                xfill True
                spacing 6
                xsize 395
                padding (8, 8, 8, 8)

                ## Render each message
                for msg in session.messages:
                    if msg.sender == "player":
                        ## Player message - right-aligned, blue bubble
                        hbox:
                            xfill True
                            ## Spacer to push bubble right
                            null width 80
                            frame:
                                xalign 1.0
                                xmaximum 300
                                background Solid(PHONE_BUBBLE_PLAYER)
                                padding (12, 8, 12, 8)
                                text msg.text color PHONE_TEXT_PLAYER size 15
                    else:
                        ## NPC message - left-aligned, light bubble
                        hbox:
                            xfill True
                            spacing 6
                            ## Small avatar
                            add session.avatar xsize 28 ysize 28 yalign 0.0
                            frame:
                                xmaximum 280
                                background Solid(PHONE_BUBBLE_NPC)
                                padding (12, 8, 12, 8)
                                text msg.text color PHONE_TEXT_NPC size 15
                            ## Spacer
                            null width 60

                ## Loading indicator
                if session.is_loading:
                    hbox:
                        xfill True
                        spacing 6
                        add session.avatar xsize 28 ysize 28 yalign 0.0
                        frame:
                            xmaximum 100
                            background Solid(PHONE_BUBBLE_NPC)
                            padding (12, 8, 12, 8)
                            text "..." color PHONE_TEXT_NPC size 15

        ## Input area at bottom
        frame:
            xfill True
            ysize 52
            background Solid(PHONE_INPUT_BG)
            padding (8, 6, 8, 6)

            hbox:
                spacing 6
                xfill True
                yalign 0.5

                ## Text input field
                button:
                    xsize 300
                    ysize 36
                    background Solid("#1a3a4f")
                    padding (10, 6, 10, 6)
                    action Return(("type", None))
                    text "Type a message..." color "#888888" size 14 yalign 0.5

                ## Send button
                textbutton "Send":
                    xsize 70
                    ysize 36
                    text_size 15
                    text_color "#ffffff"
                    background Solid(PHONE_ACCENT)
                    action Return(("send", None))


## ===================================================================
## BINDR SCREEN - Dating app profile cards
## ===================================================================
screen phone_bindr(profiles, current_index):
    tag phone_content

    vbox:
        xfill True
        yfill True

        ## Header
        frame:
            xfill True
            ysize 40
            background Solid(PHONE_HEADER_BG)
            padding (10, 5, 10, 5)
            hbox:
                textbutton "< Back" action Return(("back", None)):
                    text_size 14
                    text_color PHONE_ACCENT
                    yalign 0.5
                text "Bindr" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True

        ## Profile card area
        if current_index < len(profiles):
            $ profile = profiles[current_index]
            frame:
                xfill True
                yfill True
                background Solid(PHONE_BG)
                padding (20, 20, 20, 20)

                vbox:
                    xalign 0.5
                    yalign 0.4
                    spacing 12

                    ## Profile image
                    add profile["avatar"] xsize 120 ysize 120 xalign 0.5

                    ## Name
                    text profile["name"] color "#ffffff" size 22 bold True xalign 0.5

                    ## Bio
                    if profile.get("bio"):
                        text profile["bio"] color "#aaaaaa" size 14 xalign 0.5 italic True
                    else:
                        text "No bio available" color "#aaaaaa" size 14 xalign 0.5 italic True

                    null height 20

                    ## Pass / Match buttons
                    hbox:
                        xalign 0.5
                        spacing 20

                        textbutton "Pass":
                            xsize 140
                            ysize 44
                            text_size 18
                            text_color "#666666"
                            background Solid("#e8e8e8")
                            text_xalign 0.5
                            action Return(("pass", current_index))

                        textbutton "Match!":
                            xsize 140
                            ysize 44
                            text_size 18
                            text_color "#ffffff"
                            background Solid(PHONE_ACCENT)
                            text_xalign 0.5
                            action Return(("match", current_index))
        else:
            ## No more profiles
            frame:
                xfill True
                yfill True
                background Solid(PHONE_BG)
                text "No new profiles nearby" color "#aaaaaa" size 16 xalign 0.5 yalign 0.4


## ===================================================================
## CONTACTS SCREEN
## ===================================================================
screen phone_contacts(chat_sessions):
    tag phone_content

    vbox:
        xfill True
        yfill True

        ## Header
        frame:
            xfill True
            ysize 40
            background Solid(PHONE_HEADER_BG)
            padding (10, 5, 10, 5)
            text "Contacts" color "#ffffff" size 20 xalign 0.5 yalign 0.5 bold True

        ## Contact list
        viewport:
            xfill True
            ysize 548
            mousewheel True
            scrollbars "vertical"

            vbox:
                xfill True
                spacing 2

                for session in chat_sessions:
                    button:
                        xfill True
                        ysize 90
                        background "#d4e6f1"
                        hover_background "#aed6f1"
                        action Return(("open_chat", session))
                        padding (10, 10, 10, 10)

                        hbox:
                            spacing 14
                            yalign 0.5

                            ## Character avatar
                            add session.avatar xsize 66 ysize 66 yalign 0.5

                            ## Name
                            text session.character_name color "#222222" size 20 bold True yalign 0.5
