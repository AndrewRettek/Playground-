## screens.rpy - Minimal screen definitions for core Ren'Py functionality (1280x720)
##
## Warm marble & gold theme for School of Athens

## ===================================================================
## SAY SCREEN
## ===================================================================

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

style window:
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 278
    background Solid("#2c2418cc")
    padding (30, 15, 30, 15)

style namebox:
    xpos 360
    xanchor 0.0
    xsize None
    ypos 0
    ysize None
    background None
    padding (8, 8, 8, 8)

style say_label:
    color "#c4a265"
    size 36
    bold True

style say_dialogue:
    color "#f5efe0"
    size 30
    xpos 0
    xsize 1170
    ypos 60

## ===================================================================
## INPUT SCREEN
## ===================================================================

screen input(prompt):
    style_prefix "input"

    window:
        xalign 0.5
        yalign 0.8
        xsize 900
        ysize 180
        background Solid("#3a3020dd")
        padding (30, 22, 30, 22)

        vbox:
            xalign 0.5
            spacing 12
            text prompt style "input_prompt" color "#a09580" size 24 xalign 0.5
            input id "input" color "#f5efe0" size 30 xalign 0.5 length 500

style input_prompt:
    xalign 0.5

## ===================================================================
## CHOICE SCREEN
## ===================================================================

screen choice(items):
    style_prefix "choice"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 15

        for i in items:
            textbutton i.caption action i.action:
                xsize 600
                ysize 75

style choice_button:
    xalign 0.5
    background Solid("#8a6832")
    hover_background Solid("#c4a265")
    padding (30, 15, 30, 15)

style choice_button_text:
    color "#f5efe0"
    size 30
    xalign 0.5

## ===================================================================
## NVL SCREEN
## ===================================================================

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"
        has vbox:
            spacing 22

        for d in dialogue:
            window:
                id d.window_id
                has hbox:
                    spacing 15
            if d.who is not None:
                text d.who size 30 color "#c4a265" bold True minwidth 225
            text d.what size 27 color "#f5efe0"

        if items:
            for i in items:
                textbutton i.caption action i.action style "nvl_button"

style nvl_window:
    xfill True
    yfill True
    background Solid("#2c2418cc")
    padding (45, 45, 45, 45)

## ===================================================================
## MAIN MENU
## ===================================================================

screen main_menu():
    tag menu
    style_prefix "main_menu"

    ## Background
    add "images/ui/menu_bg.png"

    ## Dark overlay for readability
    add Solid("#1a140a88")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 750
        ysize 750
        background Solid("#2c2418cc")
        padding (60, 45, 60, 45)

        vbox:
            xalign 0.5
            spacing 27

            ## Logo
            add "images/ui/logo.png" xalign 0.5

            text "v0.1.0" size 21 color "#7a6540" xalign 0.5

            null height 30

            textbutton "Start" action Start() xalign 0.5:
                text_size 36
                text_color "#c4a265"
                text_hover_color "#f5efe0"

            textbutton "Quit" action Quit(confirm=True) xalign 0.5:
                text_size 36
                text_color "#c4a265"
                text_hover_color "#f5efe0"


## ===================================================================
## SUBSCRIPTION KEY SCREEN
## ===================================================================

screen subscription():
    modal True

    add Solid("#1a140a")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 750
        ysize 525
        background Solid("#3a3020")
        padding (60, 45, 60, 45)

        vbox:
            xalign 0.5
            spacing 22

            text "Subscription Key" size 42 color "#f5efe0" xalign 0.5 bold True

            null height 8

            text "Enter your subscription key to enable chatting." size 21 color "#a09580" xalign 0.5 text_align 0.5

            null height 15

            if is_logged_in():
                text "Current key: [persistent.player_token[:8]]..." size 21 color "#5a8a4e" xalign 0.5

            null height 8

            textbutton "Enter Key" action Return("enter_key") xalign 0.5:
                text_size 30
                text_color "#f5efe0"
                background Solid("#8a6832")
                hover_background Solid("#c4a265")
                xsize 300
                text_xalign 0.5
                ysize 60

            if is_logged_in():
                textbutton "Clear Key" action Return("clear_key") xalign 0.5:
                    text_size 24
                    text_color "#8a3040"
                    text_hover_color "#a04050"

            null height 15

            textbutton "Back" action Return("back") xalign 0.5:
                text_size 27
                text_color "#c4a265"
                text_hover_color "#f5efe0"

## ===================================================================
## GAME MENU / NAVIGATION
## ===================================================================

screen navigation():
    vbox:
        style_prefix "navigation"
        xpos 90
        yalign 0.5
        spacing 12

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Quit") action Quit(confirm=True)

style navigation_button_text:
    color "#f5efe0"
    hover_color "#c4a265"
    size 30

## ===================================================================
## SAVE / LOAD SCREENS
## ===================================================================

screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use navigation

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 750
        background Solid("#3a3020")
        padding (30, 30, 30, 30)

        vbox:
            xalign 0.5
            spacing 15

            text title size 42 color "#f5efe0" xalign 0.5 bold True
            null height 15

            grid 3 2:
                xalign 0.5
                spacing 22
                transpose True

                for i in range(1, 7):
                    button:
                        xsize 345
                        ysize 135
                        background Solid("#2c2418")
                        hover_background Solid("#4a3d2a")
                        action FileAction(i)
                        padding (15, 15, 15, 15)

                        vbox:
                            text "Slot [i]" size 24 color "#f5efe0"
                            text FileTime(i, format=_("{#file_time}%B %d %Y, %H:%M"), empty=_("Empty")) size 18 color "#a09580"

            null height 15
            hbox:
                xalign 0.5
                spacing 30
                textbutton "<" action FilePagePrevious() text_color "#c4a265" text_size 30
                text "Page" color "#f5efe0" size 27 yalign 0.5
                textbutton ">" action FilePageNext() text_color "#c4a265" text_size 30

## ===================================================================
## PREFERENCES SCREEN
## ===================================================================

screen preferences():
    tag menu
    use navigation

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 600
        background Solid("#3a3020")
        padding (45, 45, 45, 45)

        vbox:
            xalign 0.5
            spacing 22

            text "Preferences" size 42 color "#f5efe0" xalign 0.5 bold True
            null height 15

            hbox:
                spacing 15
                text "Music Volume" color "#f5efe0" size 27 yalign 0.5 xsize 270
                bar value Preference("music volume") xsize 450 ysize 30

            hbox:
                spacing 15
                text "Sound Volume" color "#f5efe0" size 27 yalign 0.5 xsize 270
                bar value Preference("sound volume") xsize 450 ysize 30

            hbox:
                spacing 15
                text "Fullscreen" color "#f5efe0" size 27 yalign 0.5 xsize 270
                textbutton "Toggle" action Preference("display", "toggle") text_color "#c4a265" text_size 27

## ===================================================================
## CONFIRM SCREEN
## ===================================================================

screen confirm(message, yes_action, no_action):
    modal True

    add Solid("#00000088")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 270
        background Solid("#3a3020")
        padding (45, 38, 45, 38)

        vbox:
            xalign 0.5
            spacing 30

            text message color "#f5efe0" size 30 xalign 0.5 text_align 0.5
            hbox:
                xalign 0.5
                spacing 45
                textbutton "Yes" action yes_action text_color "#c4a265" text_size 30
                textbutton "No" action no_action text_color "#8a3040" text_size 30

## ===================================================================
## SKIP INDICATOR
## ===================================================================

screen skip_indicator():
    zorder 100
    text "Skipping" color "#f5efe0" size 21 xalign 1.0 yalign 0.0

## ===================================================================
## NOTIFY SCREEN
## ===================================================================

screen notify(message):
    zorder 100

    frame:
        xalign 0.5
        ypos 38
        background Solid("#3a3020cc")
        padding (30, 12, 30, 12)
        text "[message!tq]" color "#f5efe0" size 24

    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0
