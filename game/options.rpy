# -*- coding: utf-8 -*-
"""
Ren'Py options and configuration.
"""

## Basics
define config.name = _("Тени над Королевством")
define gui.show_name = True
define config.version = "0.1.0"

## Sound and Music
define config.has_sound = True
define config.has_music = True
define config.has_voice = False

## Transition
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

## Window management
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

## Default preferences
default preferences.text_cps = 0
default preferences.afm_time = 15

## Build configuration
define build.name = "ShadowsOverKingdom"
define build.directory_name = "ShadowsOverKingdom-1.0"

## File patterns
define build.classify('**~', None)
define build.classify('**.bak', None)
define build.classify('**/.**', None)
define build.classify('**/#**', None)
define build.classify('**/thumbs.db', None)

## Documentation
define build.documentation('*.html')
define build.documentation('*.txt')
