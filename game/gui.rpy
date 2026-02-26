## gui.rpy - GUI configuration

init python:
    gui.init(1280, 720)

## Colors
define gui.accent_color = '#4a90d9'
define gui.idle_color = '#aaaaaa'
define gui.idle_small_color = '#999999'
define gui.hover_color = '#66aaff'
define gui.selected_color = '#ffffff'
define gui.insensitive_color = '#55555580'
define gui.muted_color = '#3d5166'
define gui.hover_muted_color = '#5b7a99'
define gui.accent_warm = "#E8849A"      ## Rose pink — dating sim accent
define gui.text_color = '#ffffff'
define gui.interface_text_color = '#ffffff'

## Fonts
define gui.text_font = gui.preference("font_transform", "gui/fonts/Inter-Regular.ttf")
define gui.name_text_font = gui.preference("font_transform", "gui/fonts/Inter-Bold.ttf")
define gui.interface_text_font = gui.preference("font_transform", "gui/fonts/Inter-Medium.ttf")

## Font sizes
define gui.text_size = 22
define gui.name_text_size = 24
define gui.interface_text_size = 22
define gui.label_text_size = 28
define gui.notify_text_size = 18
define gui.title_text_size = 50

## Main and game menus
define gui.main_menu_background_size_group = None
define gui.game_menu_background_size_group = None

## Dialogue
define gui.dialogue_xpos = 268
define gui.dialogue_ypos = 2
define gui.dialogue_width = 744
define gui.dialogue_text_xalign = 0.0

## Choice buttons
define gui.choice_button_width = 420
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(100, 5, 100, 5)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#cccccc"
define gui.choice_button_text_hover_color = "#ffffff"

## Scrollbar
define gui.scrollbar_size = 8
define gui.unscrollable = "hide"

## History
define config.history_length = 250
