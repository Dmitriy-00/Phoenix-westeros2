# -*- coding: utf-8 -*-
"""
Main editor screen and navigation for dev mode.
Provides access to all entity editors.
"""

## Editor Main Menu
screen editor_main_screen():
    tag menu
    modal True

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            text "РЕЖИМ РЕДАКТОРА":
                size 40
                xalign 0.5
                color "#ff0000"

            text "Выберите тип сущности для редактирования:":
                size 20
                xalign 0.5
                color "#ffffff"

            null height 20

            textbutton "Редактор персонажей":
                xalign 0.5
                action Show("character_editor_screen")

            textbutton "Редактор фракций":
                xalign 0.5
                action Show("faction_editor_screen")

            textbutton "Редактор локаций":
                xalign 0.5
                action Show("location_editor_screen")

            textbutton "Редактор улик":
                xalign 0.5
                action Show("clue_editor_screen")

            textbutton "Редактор дел":
                xalign 0.5
                action Show("case_editor_screen")

            null height 20

            textbutton "Сохранить все данные":
                xalign 0.5
                background "#00aa00"
                action Function(data_loader.save_all_game_data, game_state)

            textbutton "Назад в главное меню":
                xalign 0.5
                action Show("main_menu")


## Character Editor Screen
screen character_editor_screen():
    tag menu
    modal True

    default selected_char = None
    default edit_mode = "view"  # view, edit, create

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a1acc"

        hbox:
            spacing 20
            xalign 0.5
            yalign 0.5

            # List of characters
            vbox:
                spacing 10
                xsize 400

                text "ПЕРСОНАЖИ":
                    size 28
                    color "#ffffff"

                viewport:
                    xsize 400
                    ysize 700
                    scrollbars "vertical"
                    mousewheel True

                    vbox:
                        spacing 5

                        for char in game_state.characters.values():
                            textbutton "[char.name]":
                                xsize 380
                                action SetScreenVariable("selected_char", char)
                                background ("#ffcc00" if selected_char == char else "#2a2a2a")

                textbutton "Создать нового":
                    xsize 380
                    action [
                        SetScreenVariable("edit_mode", "create"),
                        SetScreenVariable("selected_char", None)
                    ]

                textbutton "Назад":
                    xsize 380
                    action Show("editor_main_screen")

            # Character details/editor
            vbox:
                spacing 10
                xsize 900

                if selected_char:
                    text "Редактирование: [selected_char.name]":
                        size 24
                        color "#ffcc00"

                    viewport:
                        xsize 900
                        ysize 750
                        scrollbars "vertical"
                        mousewheel True

                        vbox:
                            spacing 15

                            text "ID: [selected_char.id]":
                                size 18
                                color "#ffffff"

                            text "Имя: [selected_char.name]":
                                size 18
                                color "#ffffff"

                            text "Титул: [selected_char.title]":
                                size 18
                                color "#ffffff"

                            text "Фракция: [selected_char.faction_id]":
                                size 18
                                color "#ffffff"

                            text "Описание:":
                                size 18
                                color "#ffffff"

                            text "[selected_char.description]":
                                size 16
                                color "#cccccc"
                                xsize 850

                            text "Базовое отношение: [selected_char.base_relationship]":
                                size 18
                                color "#ffffff"

                            text "Текущее отношение: [selected_char.current_relationship]":
                                size 18
                                color "#ffffff"

                            text "Черты: [', '.join(selected_char.traits)]":
                                size 18
                                color "#ffffff"

                            text "Статус: [('Жив' if selected_char.is_alive else 'Мёртв')]":
                                size 18
                                color ("#00ff00" if selected_char.is_alive else "#ff0000")

                    hbox:
                        spacing 20
                        xalign 0.5

                        textbutton "Удалить":
                            background "#aa0000"
                            action [
                                Function(delete_character, selected_char.id),
                                SetScreenVariable("selected_char", None)
                            ]

                        textbutton "Сбросить отношения":
                            action Function(reset_character_relationship, selected_char.id)

                elif edit_mode == "create":
                    text "Создание нового персонажа":
                        size 24
                        color "#00ff00"

                    text "(Базовая версия - используйте JSON для полного редактирования)":
                        size 16
                        color "#888888"

                else:
                    text "Выберите персонажа для редактирования":
                        size 20
                        color "#888888"
                        xalign 0.5
                        yalign 0.5


## Faction Editor Screen (simplified)
screen faction_editor_screen():
    tag menu
    modal True

    default selected_faction = None

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a1acc"

        hbox:
            spacing 20
            xalign 0.5
            yalign 0.5

            vbox:
                spacing 10
                xsize 400

                text "ФРАКЦИИ":
                    size 28
                    color "#ffffff"

                viewport:
                    xsize 400
                    ysize 750
                    scrollbars "vertical"
                    mousewheel True

                    vbox:
                        spacing 5

                        for faction in game_state.factions.values():
                            textbutton "[faction.name]":
                                xsize 380
                                action SetScreenVariable("selected_faction", faction)
                                background ("#ffcc00" if selected_faction == faction else "#2a2a2a")

                textbutton "Назад":
                    xsize 380
                    action Show("editor_main_screen")

            vbox:
                spacing 10
                xsize 900

                if selected_faction:
                    text "Редактирование: [selected_faction.name]":
                        size 24
                        color "#ffcc00"

                    viewport:
                        xsize 900
                        ysize 800
                        scrollbars "vertical"
                        mousewheel True

                        vbox:
                            spacing 15

                            text "ID: [selected_faction.id]":
                                size 18
                                color "#ffffff"

                            text "Название: [selected_faction.name]":
                                size 18
                                color "#ffffff"

                            text "Тип: [selected_faction.type]":
                                size 18
                                color "#ffffff"

                            text "Описание:":
                                size 18
                                color "#ffffff"

                            text "[selected_faction.description]":
                                size 16
                                color "#cccccc"
                                xsize 850

                            text "Репутация: [selected_faction.current_reputation]":
                                size 18
                                color "#ffffff"

                else:
                    text "Выберите фракцию для просмотра":
                        size 20
                        color "#888888"
                        xalign 0.5
                        yalign 0.5


## Simplified editors for other entities
screen location_editor_screen():
    tag menu
    modal True

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "РЕДАКТОР ЛОКАЦИЙ":
                size 30
                color "#ffffff"

            text "Всего локаций: [len(game_state.locations)]":
                size 20
                color "#cccccc"

            text "(Используйте JSON файлы для полного редактирования)":
                size 16
                color "#888888"

            textbutton "Назад":
                xalign 0.5
                action Show("editor_main_screen")


screen clue_editor_screen():
    tag menu
    modal True

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "РЕДАКТОР УЛИК":
                size 30
                color "#ffffff"

            text "Всего улик: [len(game_state.clues)]":
                size 20
                color "#cccccc"

            text "(Используйте JSON файлы для полного редактирования)":
                size 16
                color "#888888"

            textbutton "Назад":
                xalign 0.5
                action Show("editor_main_screen")


screen case_editor_screen():
    tag menu
    modal True

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "РЕДАКТОР ДЕЛ":
                size 30
                color "#ffffff"

            text "Всего дел: [len(game_state.cases)]":
                size 20
                color "#cccccc"

            text "(Используйте JSON файлы для полного редактирования)":
                size 16
                color "#888888"

            textbutton "Назад":
                xalign 0.5
                action Show("editor_main_screen")


## Helper functions for editors
init python:

    def delete_character(char_id):
        """Delete a character from the game state."""
        if char_id in game_state.characters:
            del game_state.characters[char_id]
            renpy.notify("Персонаж удалён")
        return

    def reset_character_relationship(char_id):
        """Reset character relationship to base value."""
        char = game_state.get_character(char_id)
        if char:
            char.current_relationship = char.base_relationship
            renpy.notify("Отношения сброшены")
        return

    def present_evidence(scene, stmt_index, clue_id):
        """Present evidence during interrogation."""
        stmt = scene.statements[stmt_index]
        is_correct, response = evidence_manager.check_clue_relevance(clue_id, stmt.id, scene)

        if is_correct:
            renpy.notify("Верно!")
            # TODO: Show response and advance interrogation
        else:
            scene.add_mistake()
            renpy.notify("Неправильно! Ошибка!")
            if scene.current_mistakes >= scene.max_mistakes:
                renpy.notify("Допрос провален!")
                # TODO: Handle interrogation failure

        return
