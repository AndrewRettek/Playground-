## screens.rpy - Minimal screen definitions for core Ren'Py functionality (1920x1080)
##
## This file provides the minimum screens needed for Ren'Py to function.
## The phone UI screens are in phone_screens.rpy.

## ===================================================================
## SAY SCREEN - For any standard dialogue (minimal, since we use phone UI)
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
    background Solid("#000000cc")
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
    color "#ffffff"
    size 36
    bold True

style say_dialogue:
    color "#ffffff"
    size 30
    xpos 0
    xsize 1170
    ypos 60

## ===================================================================
## INPUT SCREEN - For renpy.input() text entry
## ===================================================================

screen input(prompt):
    style_prefix "input"

    window:
        xalign 0.5
        yalign 0.8
        xsize 900
        ysize 180
        background Solid("#1a3a4fdd")
        padding (30, 22, 30, 22)

        vbox:
            xalign 0.5
            spacing 12
            text prompt style "input_prompt" color "#aaaaaa" size 24 xalign 0.5
            input id "input" color "#ffffff" size 30 xalign 0.5 length 500

style input_prompt:
    xalign 0.5

## ===================================================================
## CHOICE SCREEN - For in-game choices
## ===================================================================

screen choice(items):
    style_prefix "choice"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 16

        for i in items:
            textbutton i.caption action i.action:
                xsize 600
                ysize 75

style choice_button:
    xalign 0.5
    background Frame("gui/panels/button_primary.png", 20, 20, 20, 20)
    hover_background Frame("gui/panels/button_primary_hover.png", 20, 20, 20, 20)
    padding (32, 16, 32, 16)

style choice_button_text:
    color "#ffffff"
    size 30
    xalign 0.5

## ===================================================================
## NVL SCREEN - For NVL mode text (minimal)
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
                text d.who size 30 color "#4fc3f7" bold True minwidth 225
            text d.what size 27 color "#ffffff"

        if items:
            for i in items:
                textbutton i.caption action i.action style "nvl_button"

style nvl_window:
    xfill True
    yfill True
    background Solid("#000000cc")
    padding (45, 45, 45, 45)

## ===================================================================
## MAIN MENU
## ===================================================================

screen main_menu():
    tag menu
    style_prefix "main_menu"

    ## Midjourney gothic cityscape background
    add "images/ui/menu_bg.png"

    ## Dark overlay for readability
    add Solid("#00000088")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 750
        ysize 750
        background Frame("gui/panels/panel_dark.png", 24, 24, 24, 24)
        padding (64, 48, 64, 48)

        vbox:
            xalign 0.5
            spacing 24

            ## Midjourney logo
            add "images/ui/logo.png" xalign 0.5

            text "v0.1.0" size 21 color "#E8849A" xalign 0.5

            ## Ornate divider between version and Start
            add "gui/panels/divider_ornate.png" xalign 0.5

            null height 16

            textbutton "Start" action Start() xalign 0.5:
                text_size 36
                text_color "#E8849A"
                text_hover_color "#FFB0C0"

            textbutton "Quit" action Quit(confirm=True) xalign 0.5:
                text_size 36
                text_color "#4fc3f7"
                text_hover_color "#E8849A"


## ===================================================================
## SUBSCRIPTION KEY SCREEN
## ===================================================================

screen subscription():
    modal True

    add Solid("#0d2f44")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 750
        ysize 525
        background Frame("gui/panels/panel_dark_solid.png", 24, 24, 24, 24)
        padding (64, 48, 64, 48)

        vbox:
            xalign 0.5
            spacing 24

            text "Subscription Key" size 42 color "#ffffff" xalign 0.5 bold True

            null height 8

            text "Enter your subscription key to enable chatting." size 21 color "#aaaaaa" xalign 0.5 text_align 0.5

            null height 16

            if is_logged_in():
                text "Current key: [persistent.player_token[:8]]..." size 21 color "#66cc66" xalign 0.5

            null height 8

            textbutton "Enter Key" action Return("enter_key") xalign 0.5:
                text_size 30
                text_color "#ffffff"
                background Frame("gui/panels/button_primary.png", 20, 20, 20, 20)
                hover_background Frame("gui/panels/button_primary_hover.png", 20, 20, 20, 20)
                xsize 300
                text_xalign 0.5
                ysize 60

            if is_logged_in():
                textbutton "Clear Key" action Return("clear_key") xalign 0.5:
                    text_size 24
                    text_color "#ff6666"
                    text_hover_color "#ff8888"

            null height 16

            textbutton "Back" action Return("back") xalign 0.5:
                text_size 27
                text_color "#4fc3f7"
                text_hover_color "#ffffff"

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
    color "#ffffff"
    hover_color "#4fc3f7"
    size 30

## ===================================================================
## SAVE / LOAD SCREENS (kept for Ren'Py compatibility)
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
        background Frame("gui/panels/panel_dark_solid.png", 24, 24, 24, 24)
        padding (32, 32, 32, 32)

        vbox:
            xalign 0.5
            spacing 16

            text title size 42 color "#ffffff" xalign 0.5 bold True
            null height 16

            grid 3 2:
                xalign 0.5
                spacing 24
                transpose True

                for i in range(1, 7):
                    button:
                        xsize 345
                        ysize 135
                        background Frame("gui/panels/panel_slot.png", 16, 16, 16, 16)
                        hover_background Frame("gui/panels/panel_slot_hover.png", 16, 16, 16, 16)
                        action FileAction(i)
                        padding (16, 16, 16, 16)

                        vbox:
                            text "Slot [i]" size 24 color "#ffffff"
                            text FileTime(i, format=_("{#file_time}%B %d %Y, %H:%M"), empty=_("Empty")) size 18 color "#aaaaaa"

            null height 16
            hbox:
                xalign 0.5
                spacing 32
                textbutton "<" action FilePagePrevious() text_color "#4fc3f7" text_size 30
                text "Page" color "#ffffff" size 27 yalign 0.5
                textbutton ">" action FilePageNext() text_color "#4fc3f7" text_size 30

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
        background Frame("gui/panels/panel_dark_solid.png", 24, 24, 24, 24)
        padding (48, 48, 48, 48)

        vbox:
            xalign 0.5
            spacing 24

            text "Preferences" size 42 color "#ffffff" xalign 0.5 bold True
            null height 16

            hbox:
                spacing 16
                text "Music Volume" color "#ffffff" size 27 yalign 0.5 xsize 270
                bar value Preference("music volume") xsize 450 ysize 32

            hbox:
                spacing 16
                text "Sound Volume" color "#ffffff" size 27 yalign 0.5 xsize 270
                bar value Preference("sound volume") xsize 450 ysize 32

            hbox:
                spacing 16
                text "Fullscreen" color "#ffffff" size 27 yalign 0.5 xsize 270
                textbutton "Toggle" action Preference("display", "toggle") text_color "#4fc3f7" text_size 27

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
        background Frame("gui/panels/panel_dark_solid.png", 24, 24, 24, 24)
        padding (48, 40, 48, 40)

        vbox:
            xalign 0.5
            spacing 32

            text message color "#ffffff" size 30 xalign 0.5 text_align 0.5
            hbox:
                xalign 0.5
                spacing 48
                textbutton "Yes" action yes_action text_color "#4fc3f7" text_size 30
                textbutton "No" action no_action text_color "#ff6666" text_size 30

## ===================================================================
## SKIP INDICATOR
## ===================================================================

screen skip_indicator():
    zorder 100
    text "Skipping" color "#ffffff" size 21 xalign 1.0 yalign 0.0

## ===================================================================
## NOTIFY SCREEN
## ===================================================================

screen notify(message):
    zorder 100

    frame:
        xalign 0.5
        ypos 40
        background Frame("gui/panels/panel_dark.png", 24, 24, 24, 24)
        padding (32, 16, 32, 16)
        text "[message!tq]" color "#ffffff" size 24

    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0
