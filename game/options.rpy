## options.rpy - Game configuration for Steam distribution

define config.name = _("FutaDomWorld Chat")
define config.version = "0.1.0"

## Save directory name - must be unique per game
define config.save_directory = "FutaDomWorldChat-1234567890"

## Logical resolution (art/layout designed for 1920x1080)
define config.screen_width = 1920
define config.screen_height = 1080

## Physical window size (2/3 of logical — fits nicely on 1080p monitors)
define config.physical_width = 1280
define config.physical_height = 720

## Start windowed (player can press F or Alt+Enter for fullscreen)
default preferences.fullscreen = False

## Allow window resizing
define config.window_icon = None

## Sound settings
define config.has_sound = True
define config.has_music = True
define config.has_voice = False

## Main menu music (placeholder - set to None until you have audio)
define config.main_menu_music = None

## Transition settings
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

## Text speed defaults
default preferences.text_cps = 0
default preferences.afm_time = 15

## Build configuration for Steam
init python:
    build.name = "FutaDomWorldChat"

    ## File classifications
    build.classify("game/**.rpy", None)
    build.classify("game/**.rpyc", "all")
    build.classify("game/**.png", "all")
    build.classify("game/**.jpg", "all")
    build.classify("game/**.ogg", "all")
    build.classify("game/**.mp3", "all")
    build.classify("game/**.wav", "all")
    build.classify("game/**.webp", "all")
    build.classify("game/**.txt", "all")

    ## Exclude dev/temp files
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
    build.classify("game/saves/**", None)
    build.classify("game/cache/**", None)

    ## Documentation
    build.documentation("README.txt")
