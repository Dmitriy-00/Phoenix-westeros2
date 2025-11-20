# -*- coding: utf-8 -*-
"""
Quick Access Shortcuts
Быстрый доступ и горячие клавиши
"""

## Глобальный экран быстрого доступа (всегда активен)
screen quick_access_overlay():
    zorder 100

    # Горячие клавиши
    key "K_n" action ShowMenu("evidence_notebook")
    key "K_m" action ShowMenu("world_map_screen")
    key "K_c" action ShowMenu("character_gallery_screen")
    key "K_a" action ShowMenu("achievements_screen")
    key "K_h" action Show("quick_help")
    key "K_F5" action QuickSave()
    key "K_F9" action QuickLoad()

    # Индикаторы в углу экрана
    if game_state:
        # Счётчик улик
        hbox:
            xalign 0.02
            yalign 0.02
            spacing 10

            frame:
                background "#000000aa"
                padding (15, 10)

                hbox:
                    spacing 10

                    text "📜" size 20
                    text "[evidence_manager.get_discovered_count()]":
                        size 20
                        color "#ffcc00"

        # Текущее дело (если активно)
        if case_manager and case_manager.current_case:
            frame:
                xalign 0.98
                yalign 0.02
                background "#000000aa"
                padding (15, 10)

                vbox:
                    spacing 5

                    text "[case_manager.current_case.title]":
                        size 16
                        color "#ffcc00"
                        xalign 1.0

                    $ stage_name = case_manager.get_current_stage_name()
                    if stage_name:
                        text "Этап: [stage_name]":
                            size 14
                            color "#cccccc"
                            xalign 1.0


## Быстрое меню (ПКМ или ESC)
screen quick_menu():
    variant "pc"
    zorder 100

    if quick_menu:
        hbox:
            xalign 0.5
            yalign 0.98
            spacing 15

            textbutton "История" action ShowMenu("history")
            textbutton "Пропуск" action Skip() alternate Skip(fast=True, confirm=True)
            textbutton "Авто" action Preference("auto-forward", "toggle")
            textbutton "Сохранить" action ShowMenu("save")
            textbutton "Загрузить" action ShowMenu("load")
            textbutton "Настройки" action ShowMenu("preferences")
            textbutton "Выход" action MainMenu()


## Улучшенный экран паузы
screen pause_menu():
    modal True
    zorder 200

    add "#000000aa"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 700
        background "#1a1a2a"

        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5

            text "ПАУЗА" size 48 xalign 0.5 color "#ffcc00"

            null height 20

            vbox:
                spacing 15
                xalign 0.5

                textbutton "Продолжить" action Return() xsize 400
                textbutton "Блокнот (N)" action ShowMenu("evidence_notebook") xsize 400
                textbutton "Карта (M)" action ShowMenu("world_map_screen") xsize 400
                textbutton "Персонажи (C)" action ShowMenu("character_gallery_screen") xsize 400
                textbutton "Достижения (A)" action ShowMenu("achievements_screen") xsize 400

                null height 10

                textbutton "Сохранить (F5)" action QuickSave() xsize 400
                textbutton "Загрузить (F9)" action QuickLoad() xsize 400
                textbutton "Настройки" action ShowMenu("settings_menu") xsize 400

                null height 10

                textbutton "Помощь (H)" action Show("quick_help") xsize 400
                textbutton "Главное меню" action MainMenu() xsize 400


## Индикатор сохранения
screen save_indicator():
    zorder 200

    frame:
        xalign 0.98
        yalign 0.98
        background "#000000aa"
        padding (15, 10)

        text "💾 Сохранено":
            size 18
            color "#00ff00"

    timer 2.0 action Hide("save_indicator")


## Расширенный QuickSave с уведомлением
init python:
    def quick_save_with_notification():
        """Быстрое сохранение с уведомлением"""
        renpy.take_screenshot()
        renpy.save("quick-1", "Быстрое сохранение")

        # Показать индикатор
        renpy.show_screen("save_indicator")

        # Сохранить статистику
        game_statistics.save_statistics()

        return True


## Переопределение QuickSave
define config.keymap['quicksave'] = []
define config.keymap['quickload'] = []

init python:
    config.keymap['quicksave'] = ['K_F5', 's']
    config.keymap['quickload'] = ['K_F9', 'l']


## Экран статуса игры (для разработки/отладки)
screen debug_overlay():
    zorder 300

    if config.developer:
        frame:
            xalign 0.02
            yalign 0.95
            background "#000000cc"
            padding (10, 8)

            vbox:
                spacing 3

                text "FPS: [renpy.get_fps():.1f]" size 12 color "#00ff00"

                if game_state:
                    text "Улик: [len(game_state.discovered_clues)]" size 12 color "#00ff00"

                if game_statistics:
                    $ completion = game_statistics.get_completion_percentage()
                    text "Завершение: [completion]%%" size 12 color "#00ff00"


## Навигационные кнопки во время игры
screen game_navigation():
    zorder 90

    # Кнопка паузы
    imagebutton:
        xalign 0.98
        yalign 0.12
        idle "#ffcc0033"
        hover "#ffcc0066"
        xsize 50
        ysize 50

        action Show("pause_menu")

        frame:
            background None
            xalign 0.5
            yalign 0.5

            text "⏸":
                size 30
                color "#ffffff"


## Автоматическое показ quick_access при загрузке
label after_load:
    # Восстановить музыку для текущей локации
    python:
        if hasattr(store, 'current_location_id') and current_location_id:
            play_location_music(current_location_id)

    return


## Обработчик начала диалога
label start_dialogue_auto(dialogue_id):
    python:
        # Загрузить диалог
        dialogue_manager.load_dialogue(dialogue_id)
        dialogue_manager.start_dialogue()

        # Автосохранение
        if game_settings.auto_save:
            renpy.save("auto-dialogue")

    jump dialogue_scene


## Быстрые команды для консоли (режим разработчика)
# Активируйте консоль: config.console = True

init python:
    def unlock_all_achievements():
        """Разблокировать все достижения (для тестирования)"""
        for ach_id in achievements_manager.achievements:
            achievements_manager.unlock_achievement(ach_id, show_notification=False)
        renpy.notify("Все достижения разблокированы!")

    def reset_achievements():
        """Сбросить все достижения"""
        for ach in achievements_manager.achievements.values():
            ach.unlocked = False
        game_statistics.achievements_unlocked = []
        renpy.notify("Достижения сброшены!")

    def unlock_all_gallery():
        """Разблокировать всю галерею"""
        if game_state:
            for char_id in game_state.characters:
                character_gallery.unlock_character(char_id)
            for loc in game_state.world_map.locations:
                character_gallery.unlock_location(loc.id)
            for faction_id in game_state.factions:
                character_gallery.unlock_faction(faction_id)
        renpy.notify("Галерея полностью разблокирована!")

    def add_all_clues():
        """Добавить все улики"""
        if game_state and evidence_manager:
            for clue_id in game_state.clues:
                evidence_manager.discover_clue(clue_id)
        renpy.notify("Все улики добавлены!")

    def max_relationships():
        """Максимальные отношения со всеми"""
        if game_state:
            for char in game_state.characters.values():
                char.current_relationship = 100
        renpy.notify("Отношения максимальны!")


## Справка по горячим клавишам (показывается при первом запуске)
label first_time_tutorial:
    if not persistent.seen_tutorial:
        call screen quick_help

        python:
            persistent.seen_tutorial = True

    return


## Инициализация persistent переменных
default persistent.seen_tutorial = False
default persistent.total_playtime = 0.0
default persistent.games_completed = 0
