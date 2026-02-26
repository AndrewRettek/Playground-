## gui.rpy - GUI configuration (warm marble & gold theme)

init python:
    gui.init(1280, 720)

## Colors - warm marble & gold palette
define gui.accent_color = '#c4a265'
define gui.idle_color = '#a09580'
define gui.idle_small_color = '#8a7d68'
define gui.hover_color = '#f5efe0'
define gui.selected_color = '#f5efe0'
define gui.insensitive_color = '#55504580'
define gui.muted_color = '#5a4d3a'
define gui.hover_muted_color = '#7a6a50'
define gui.text_color = '#f5efe0'
define gui.interface_text_color = '#f5efe0'

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
define gui.choice_button_text_idle_color = "#c4a265"
define gui.choice_button_text_hover_color = "#f5efe0"

## Scrollbar
define gui.scrollbar_size = 8
define gui.unscrollable = "hide"

## History
define config.history_length = 250
