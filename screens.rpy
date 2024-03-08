init offset = -501

screen value_input(message, ok_action, alloww):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    key "K_RETURN" action ok_action
    frame:
        background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
        padding gui.confirm_frame_borders.padding
        xalign .5
        yalign .5
        has vbox:
            xalign .5
            yalign .5
            spacing 30
        label _(message):
            style "gui_prompt"
            xalign 0.5
        input default "" value VariableInputValue("value") length 18 allow alloww color "#ff16d8" outlines [] text_align 0.5 layout "subtitle"
        hbox:
            xalign 0.5
            spacing 100
            textbutton _("OK") action ok_action

screen dialog(message, ok_action):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    frame:
        background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
        padding gui.confirm_frame_borders.padding
        xalign .5
        yalign .5
        has vbox:
            xalign .5
            yalign .5
            spacing 30
        label _(message):
            style "gui_prompt"
            xalign 0.5
        hbox:
            xalign 0.5
            spacing 100
            textbutton _("OK") action ok_action

init offset = 200
define gui.page_spacing = -15
screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Страница {}"), auto=_("Автоматические сохранения"), quick=_("Быстрые сохранения"))
    use game_menu(title):
        fixed:
            order_reverse True
            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value
            hbox:
                xalign 0.5
                yalign 0.9
                if title == "Сохранить":
                    text "Нажми на страницу, чтобы переименовать её. Нажатие ПКМ по сохранению ПЕРЕЗАПИШЕТ сохранение с новым именем" style "gui_text"
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action SetVariable("save_name", FileSaveName(slot)), FileAction(slot)
                        if title == "Сохранить":
                            alternate Show("save_rename", slot=slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        # text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("пустой слот")):
                        #     style "slot_time_text"
                        text FileTime(slot, format=_("{#file_time}%A %d.%m.%Y"), empty=_("пустой слот")):
                            style "slot_time_text"
                        text FileSaveName(slot):
                            style "slot_name_text"
                        key "save_delete" action FileDelete(slot)
            hbox:
                xalign 0.5
                yalign 0.925
                if config.has_autosave:
                    textbutton _("{#auto_page}Автосохранения") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("{#quick_page}Быстрые сохранения") action FilePage("quick")
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 0.975
                spacing gui.page_spacing
                if FilePageName() != u'a' and FilePageName() != u'q' and int(FilePageName()) > 1:
                    textbutton _("<<") action FilePage(max(int(FilePageName())-10,1)) alternate FilePage(1)
                else:
                    textbutton _("<<") action NullAction()
                textbutton _("<") action FilePagePrevious()
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.025
                spacing gui.page_spacing
                if FilePageName() != u'a' and FilePageName() != u'q' and int(FilePageName()) > 1:
                    for page in range(max(int(FilePageName())-9, 1), max(int(FilePageName())+11, 21)):
                        textbutton "[page]" action FilePage(page)
                else:
                    for page in range(1,21):
                        textbutton "[page]" action FilePage(page)
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.075
                spacing gui.page_spacing
                textbutton _(">") action FilePageNext()
                if FilePageName() != u'a' and FilePageName() != u'q':
                    textbutton _(">>") action FilePage(int(FilePageName())+10) alternate FilePage(int(FilePageName())+100)
                else:
                    textbutton _(">>") action NullAction()

            # hbox:
            #     style_prefix "page"
            #     xalign 0.5
            #     yalign 1.0
            #     spacing gui.page_spacing
                # if FilePageName() != u'a' and FilePageName() != u'q' and int(FilePageName()) > 1:
                #     textbutton _("<<") action FilePage(max(int(FilePageName())-10,1)) alternate FilePage(1)
                # else:
                #     textbutton _("<<") action NullAction()
                # textbutton _("<") action FilePagePrevious()
                # if config.has_autosave:
                #     textbutton _("{#auto_page}А") action FilePage("auto")
                # if config.has_quicksave:
                #     textbutton _("{#quick_page}Б") action FilePage("quick")
                # if FilePageName() != u'a' and FilePageName() != u'q' and int(FilePageName()) > 1:
                #     for page in range(max(int(FilePageName())-9, 1), max(int(FilePageName())+11, 21)):
                #         textbutton "[page]" action FilePage(page)
                # else:
                #     for page in range(1,21):
                #         textbutton "[page]" action FilePage(page)
                # textbutton _(">") action FilePageNext()
                # if FilePageName() != u'a' and FilePageName() != u'q':
                #     textbutton _(">>") action FilePage(int(FilePageName())+10) alternate FilePage(int(FilePageName())+100)
                # else:
                #     textbutton _(">>") action NullAction()



screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.5
            yalign 1.0
            textbutton _("История") action ShowMenu('history')
            textbutton _("Пропускать") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Девушки") action ShowMenu('amitrackerm2')
            textbutton _("Прогресс") action ShowMenu('progressmod')
            if show_hints:
                if current_chapter == 1:
                    textbutton _("Подсказки") action ShowMenu('hinttracker1')
                if current_chapter == 2:
                    textbutton _("Подсказки") action ShowMenu('hinttracker2')
                if current_chapter == 3:
                    textbutton _("Подсказки") action ShowMenu('hinttracker3')
            textbutton _("Сохранить") action ShowMenu('save')
            textbutton _("Загрузить") action ShowMenu('load')
            textbutton _("Б.Сохр.") action QuickSave()
            textbutton _("Б.Загр.") action QuickLoad()
            textbutton _("Парам.") action ShowMenu('preferences')
            textbutton _("Мод меню") action ShowMenu('modmenu')

screen quick_menu():
    variant "touch"
    zorder 100
    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.5
            yalign 1.0
            textbutton _("Назад") action Rollback()
            textbutton _("Пропускать") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Меню") action ShowMenu()
            textbutton _("События") action ShowMenu('eventtracker11')
            textbutton _("Девушки") action ShowMenu('eventtrackercharahub')
            textbutton _("Прогресс") action ShowMenu('affection')
            if bonus == True:
                textbutton _("Вики") action OpenURL("https://lessonsinlove.wiki/")
            textbutton _("Мод меню") action ShowMenu('modmenu')
            textbutton _("Спрятать") action HideInterface()

screen modmenunavigation(title):
    style_prefix "game_menu"
    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing
        if mhb == True:
            if day150 == True:
                textbutton _("Кнопка исцеления Молли") action ShowMenu("MHB")
            else:
                textbutton _("{s}Ирландка не найдена{/s}")
        if lovelustchanger == True:
            textbutton _("Меню изменения очков") action ShowMenu("lovelustchanger")
        if helper == True:
            textbutton _("Помощь в прохождении") action ShowMenu("helper")
        if packmod == True:
            textbutton _("Пак меню") action ShowMenu("packmenu")
        if customizationmod == True:
            textbutton _("Изменение Иконок Персонажей") action ShowMenu("icon_setter")
    textbutton _("Вернуться"):
        xpos 60
        ypos 900
        action [Return()]
    label title
    add "gametime" xpos 254

screen menu_mod(title, scroll=None, yinitial=0.0):
    style_prefix "game_menu"
    frame:
        style "game_menu_outer_frame"
        hbox:
            frame:
                style "game_menu_navigation_frame"
            frame:
                style "game_menu_content_frame"
                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        transclude
                else:
                    transclude
    label title
    use modmenunavigation(title="")

screen modmenu():
    tag menu
    add define_mods_images["mod_menu"]
    use menu_mod(_("Меню модификаций"), scroll="viewport")

screen download_screen(ok_action=[Function(renpy.set_autoreload, True), Function(renpy.reload_script), Hide("download_screen")]):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    $ status = {
        "DOWNLOADING":"Мод загружается",
        "EXTRACTING":"Распаковка архива",
        "DELETING":"Удаление старых файлов",
        "FINISH":"Готово",
        "...":"...",
        "REPLACE":"Перенос папок",
        "START":"Старт"
    }
    frame:
        background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
        padding gui.confirm_frame_borders.padding
        xalign .5
        yalign .5
        has vbox:
            xalign .5
            yalign .5
            spacing 30
        label _(persistent.mod_updater["DOWNLOADING_MOD"]):
            style "gui_prompt"
            xalign 0.3
        label _(status[persistent.mod_updater.get("STATUS", "...")]):
            style "gui_prompt"
            xalign 0.5
        hbox:
            xalign 0.5
            spacing 100
            textbutton _("Закрыть") action ok_action
    
    timer 0.05 action Function(renpy.restart_interaction) repeat True

screen mod_news:
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    frame:
        background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
        padding gui.confirm_frame_borders.padding
        xalign .5
        yalign .5
        has vbox:
            xalign .5
            yalign .5
            spacing 30
        label _("{size=+20}Модификации{/size}"):
            style "gui_prompt"
            xalign 0.1
        vbox:
            for mod in persistent.mod_updater["MODS"]:
                textbutton _(mod):
                    action ToggleDict(persistent.mod_updater["TOGGLE_MODS"], mod, True, False)
        hbox:
            spacing 100
            textbutton _("Выход") action Hide("mod_news") xalign 0
            textbutton _("OK") action [Hide("mod_news"), Function(renpy.invoke_in_thread, start_install), Show("download_screen")] xalign 1

screen preferences():
    tag menu
    use game_menu(_("Параметры"), scroll="viewport"):
        vbox:
            hbox:
                box_wrap True
                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "radio"
                        label _("Экран")
                        textbutton _("Оконный") action Preference("display", "window")
                        textbutton _("Полноэкранный") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    label _("Сторона отката")
                    textbutton _("Отключить") action Preference("rollback side", "disable")
                    textbutton _("Слева") action Preference("rollback side", "left")
                    textbutton _("Справа") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Пропускать")
                    textbutton _("Весь Текст") action Preference("skip", "toggle")
                    textbutton _("После Выбора") action Preference("after choices", "toggle")
                if not main_menu:
                    vbox:
                        style_prefix "radio"
                        label _("Метка «читера»")
                        if cheater == True:
                            text _("Ты читер.")
                        else:
                            text _("Ты не читер.")
                        textbutton _("Хочешь это изменить?") action Jump("chitak")
                    vbox:
                        style_prefix "radio"
                        label _("Тройничок с Чикой")
                        textbutton _("Аянэ") action SetVariable("ayanecthree", not ayanecthree)
                    vbox:
                        style_prefix "radio"
                        label _("Участвует?")
                        if ayanecthree == True:
                            text _("Да")
                        else:
                            text _("Нет")
            null height (4 * gui.pref_spacing)
            hbox:
                style_prefix "slider"
                box_wrap True
                vbox:
                    label _("Скорость Текста")
                    bar value Preference("text speed")
                    label _("Скорость Авто-чтения")
                    bar value Preference("auto-forward time")
                vbox:
                    if config.has_music:
                        label _("Громкость Музыки")
                        hbox:
                            bar value Preference("music volume")
                    if config.has_sound:
                        label _("Громкость Звука")
                        hbox:
                            bar value Preference("sound volume")
                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)
                    if config.has_voice:
                        label _("Громкость Голоса")
                        hbox:
                            bar value Preference("voice volume")
                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)
                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing
                        textbutton _("Отключить Всё"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"
        if main_menu:
            textbutton _("Обновление модификаций"):
                align (0.0, 0.0)
                action [Function(check_update), Show("mod_news")]
