default value = ''
init python:
    define_mods_images = {}
    if persistent.mod_updater is None:
        persistent.mod_updater = {}
init 200 python:
    define_mods_images.update({
        "mod_menu":"mods/compatibility/modmenu/mod_menu.png"
    })
init 500 python:
    lovelustchanger = False
    customizationmod = False
    helper = False
    shrekmod = False
    blackmod = False
    mhb = False
    packmod = False
# init 1000 python:
define config.developer = True
define config.console = True