## screens.rpy - Minimal screen definitions for core Ren'Py functionality
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
    ysize 185
    background Solid("#000000cc")
    padding (20, 10, 20, 10)

style namebox:
    xpos 240
    xanchor 0.0
    xsize None
    ypos 0
    ysize None
    background None
    padding (5, 5, 5, 5)

style say_label:
    color "#ffffff"
    size 24
    bold True

style say_dialogue:
    color "#ffffff"
    size 20
    xpos 0
    xsize 780
    ypos 40

## ===================================================================
## INPUT SCREEN - For renpy.input() text entry
## ===================================================================

screen input(prompt):
    style_prefix "input"

    window:
        xalign 0.5
        yalign 0.8
        xsize 600
        ysize 120
        background Solid("#1a3a4fdd")
        padding (20, 15, 20, 15)

        vbox:
            xalign 0.5
            spacing 8
            text prompt style "input_prompt" color "#aaaaaa" size 16 xalign 0.5
            input id "input" color "#ffffff" size 20 xalign 0.5 length 500

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
        spacing 10

        for i in items:
            textbutton i.caption action i.action:
                xsize 400
                ysize 50

style choice_button:
    xalign 0.5
    background Solid("#4a90d9")
    hover_background Solid("#66aaff")
    padding (20, 10, 20, 10)

style choice_button_text:
    color "#ffffff"
    size 20
    xalign 0.5

## ===================================================================
## NVL SCREEN - For NVL mode text (minimal)
## ===================================================================

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"
        has vbox:
            spacing 15

        for d in dialogue:
            window:
                id d.window_id
                has hbox:
                    spacing 10
                if d.who is not None:
                    text d.who size 20 color "#4fc3f7" bold True minwidth 150
                text d.what size 18 color "#ffffff"

        if items:
            for i in items:
                textbutton i.caption action i.action style "nvl_button"

style nvl_window:
    xfill True
    yfill True
    background Solid("#000000cc")
    padding (30, 30, 30, 30)

## ===================================================================
## MAIN MENU
## ===================================================================

screen main_menu():
    tag menu
    style_prefix "main_menu"

    add Solid("#0d2f44")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 450
        background Solid("#1a3a4f")
        padding (40, 40, 40, 40)

        vbox:
            xalign 0.5
            spacing 20

            text "FutaDomWorld Chat" size 32 color "#ffffff" xalign 0.5 bold True
            text "v0.1.0" size 16 color "#888888" xalign 0.5

            null height 20

            textbutton "Start" action Start() xalign 0.5:
                text_size 24
                text_color "#4fc3f7"
                text_hover_color "#ffffff"

            textbutton "Load" action ShowMenu("load") xalign 0.5:
                text_size 24
                text_color "#4fc3f7"
                text_hover_color "#ffffff"

            textbutton "Subscription Key" action ShowMenu("subscription") xalign 0.5:
                text_size 24
                text_color "#4fc3f7"
                text_hover_color "#ffffff"

            textbutton "Quit" action Quit(confirm=True) xalign 0.5:
                text_size 24
                text_color "#4fc3f7"
                text_hover_color "#ffffff"

            ## Login status indicator
            if is_logged_in():
                text "Subscription: Active" size 14 color "#66cc66" xalign 0.5
            else:
                text "Subscription: Not set" size 14 color "#ff6666" xalign 0.5


## ===================================================================
## SUBSCRIPTION KEY SCREEN
## ===================================================================

screen subscription():
    tag menu

    add Solid("#0d2f44")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 350
        background Solid("#1a3a4f")
        padding (40, 30, 40, 30)

        vbox:
            xalign 0.5
            spacing 15

            text "Subscription Key" size 28 color "#ffffff" xalign 0.5 bold True

            null height 5

            text "Enter your subscription key to enable chatting." size 14 color "#aaaaaa" xalign 0.5 text_align 0.5

            null height 10

            if is_logged_in():
                text "Current key: [persistent.player_token[:8]]..." size 14 color "#66cc66" xalign 0.5

            null height 5

            textbutton "Enter Key" action Function(prompt_subscription_key) xalign 0.5:
                text_size 20
                text_color "#ffffff"
                background Solid("#4a90d9")
                hover_background Solid("#66aaff")
                xsize 200
                text_xalign 0.5
                ysize 40

            if is_logged_in():
                textbutton "Clear Key" action Function(clear_subscription_key) xalign 0.5:
                    text_size 16
                    text_color "#ff6666"
                    text_hover_color "#ff8888"

            null height 10

            textbutton "Back" action Return() xalign 0.5:
                text_size 18
                text_color "#4fc3f7"
                text_hover_color "#ffffff"

## ===================================================================
## GAME MENU / NAVIGATION
## ===================================================================

screen navigation():
    vbox:
        style_prefix "navigation"
        xpos 60
        yalign 0.5
        spacing 8

        textbutton _("Return") action Return()
        textbutton _("Save") action ShowMenu("save")
        textbutton _("Load") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Quit") action Quit(confirm=True)

style navigation_button_text:
    color "#ffffff"
    hover_color "#4fc3f7"
    size 20

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
        xsize 800
        ysize 500
        background Solid("#1a3a4f")
        padding (20, 20, 20, 20)

        vbox:
            xalign 0.5
            spacing 10

            text title size 28 color "#ffffff" xalign 0.5 bold True
            null height 10

            grid 3 2:
                xalign 0.5
                spacing 15
                transpose True

                for i in range(1, 7):
                    button:
                        xsize 230
                        ysize 90
                        background Solid("#0d2f44")
                        hover_background Solid("#1a5276")
                        action FileAction(i)
                        padding (10, 10, 10, 10)

                        vbox:
                            text "Slot [i]" size 16 color "#ffffff"
                            text FileTime(i, format=_("{#file_time}%B %d %Y, %H:%M"), empty=_("Empty")) size 12 color "#aaaaaa"

            null height 10
            hbox:
                xalign 0.5
                spacing 20
                textbutton "<" action FilePagePrevious() text_color "#4fc3f7" text_size 20
                text "Page" color "#ffffff" size 18 yalign 0.5
                textbutton ">" action FilePageNext() text_color "#4fc3f7" text_size 20

## ===================================================================
## PREFERENCES SCREEN
## ===================================================================

screen preferences():
    tag menu
    use navigation

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 400
        background Solid("#1a3a4f")
        padding (30, 30, 30, 30)

        vbox:
            xalign 0.5
            spacing 15

            text "Preferences" size 28 color "#ffffff" xalign 0.5 bold True
            null height 10

            hbox:
                spacing 10
                text "Music Volume" color "#ffffff" size 18 yalign 0.5 xsize 180
                bar value Preference("music volume") xsize 300 ysize 20

            hbox:
                spacing 10
                text "Sound Volume" color "#ffffff" size 18 yalign 0.5 xsize 180
                bar value Preference("sound volume") xsize 300 ysize 20

            hbox:
                spacing 10
                text "Fullscreen" color "#ffffff" size 18 yalign 0.5 xsize 180
                textbutton "Toggle" action Preference("display", "toggle") text_color "#4fc3f7" text_size 18

## ===================================================================
## CONFIRM SCREEN
## ===================================================================

screen confirm(message, yes_action, no_action):
    modal True

    add Solid("#00000088")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 400
        ysize 180
        background Solid("#1a3a4f")
        padding (30, 25, 30, 25)

        vbox:
            xalign 0.5
            spacing 20

            text message color "#ffffff" size 20 xalign 0.5 text_align 0.5
            hbox:
                xalign 0.5
                spacing 30
                textbutton "Yes" action yes_action text_color "#4fc3f7" text_size 20
                textbutton "No" action no_action text_color "#ff6666" text_size 20

## ===================================================================
## SKIP INDICATOR
## ===================================================================

screen skip_indicator():
    zorder 100
    text "Skipping" color "#ffffff" size 14 xalign 1.0 yalign 0.0

## ===================================================================
## NOTIFY SCREEN
## ===================================================================

screen notify(message):
    zorder 100

    frame:
        xalign 0.5
        ypos 25
        background Solid("#1a3a4fcc")
        padding (20, 8, 20, 8)
        text "[message!tq]" color "#ffffff" size 16

    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0
