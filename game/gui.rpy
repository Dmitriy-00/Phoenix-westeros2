# -*- coding: utf-8 -*-
"""
GUI Configuration for the visual novel.
"""

## Initialization
init offset = -1

## Colors
define gui.accent_color = '#ffcc00'
define gui.idle_color = '#888888'
define gui.idle_small_color = '#666666'
define gui.hover_color = '#ffffff'
define gui.selected_color = '#ffcc00'
define gui.insensitive_color = '#444444'
define gui.muted_color = '#003d51'
define gui.hover_muted_color = '#005b7a'
define gui.text_color = '#ffffff'
define gui.interface_text_color = '#ffffff'

## Fonts
define gui.text_font = "DejaVuSans.ttf"
define gui.name_text_font = "DejaVuSans-Bold.ttf"
define gui.interface_text_font = "DejaVuSans.ttf"

## Font sizes
define gui.text_size = 22
define gui.name_text_size = 30
define gui.interface_text_size = 18
define gui.label_text_size = 24
define gui.notify_text_size = 16
define gui.title_text_size = 50

## Main and Game Menus
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"

## Dialogue
define gui.textbox_height = 185
define gui.textbox_yalign = 1.0
define gui.name_xpos = 240
define gui.name_ypos = 0
define gui.name_xalign = 0.0
define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False

define gui.dialogue_xpos = 268
define gui.dialogue_ypos = 50
define gui.dialogue_width = 744
define gui.dialogue_text_xalign = 0.0

## Buttons
define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(4, 4, 4, 4)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_xalign = 0.5
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color

## Choice buttons
define gui.choice_button_width = 790
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(100, 5, 100, 5)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#cccccc"
define gui.choice_button_text_hover_color = "#ffffff"

## File slots
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

## Navigation
define gui.navigation_xpos = 40
define gui.skip_ypos = 10
define gui.notify_ypos = 45

## NVL-mode
define gui.nvl_borders = Borders(0, 10, 0, 20)
define gui.nvl_height = 115
define gui.nvl_spacing = 10

## Localization
define gui.language = "russian"

## Mobile devices
define config.screen_width = 1920
define config.screen_height = 1080

## Advanced
define config.adjust_view_size = None
