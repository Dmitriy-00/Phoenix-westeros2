# -*- coding: utf-8 -*-
"""
UI Screens for the detective visual novel.
Includes main menu, case selection, evidence journal, world map, registries, and more.
"""

## Main Menu Screen
screen main_menu():
    tag menu

    add "gui/main_menu.png"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 800
        background "#000000cc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            text "ТЕНИ НАД КОРОЛЕВСТВОМ":
                size 40
                xalign 0.5
                color "#ffffff"

            text "Детективная новелла":
                size 20
                xalign 0.5
                color "#cccccc"

            null height 50

            textbutton "Новая игра":
                xalign 0.5
                action Show("case_selection_screen")

            textbutton "Продолжить":
                xalign 0.5
                action Start()

            textbutton "Журнал мира":
                xalign 0.5
                action Show("world_codex_screen")

            if dev_mode:
                textbutton "Режим редактора":
                    xalign 0.5
                    action Show("editor_main_screen")

            textbutton "Настройки":
                xalign 0.5
                action ShowMenu("preferences")

            textbutton "Выход":
                xalign 0.5
                action Quit(confirm=True)


## Case Selection Screen
screen case_selection_screen():
    tag menu
    modal True

    add "#000000"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 800
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "ВЫБЕРИТЕ ДЕЛО":
                size 40
                xalign 0.5
                color "#ffffff"

            null height 20

            viewport:
                xsize 1100
                ysize 600
                scrollbars "vertical"
                mousewheel True

                vbox:
                    spacing 20

                    for case in game_state.cases.values():
                        button:
                            xsize 1050
                            ysize 150
                            background "#2a2a2acc"
                            hover_background "#3a3a3acc"
                            action [
                                SetVariable("selected_case_id", case.id),
                                Function(case_manager.start_case, case.id),
                                Start()
                            ]

                            hbox:
                                spacing 30
                                xalign 0.5
                                yalign 0.5

                                vbox:
                                    spacing 10

                                    text "[case.name]":
                                        size 28
                                        color "#ffcc00"

                                    text "[case.short_description]":
                                        size 18
                                        color "#cccccc"
                                        xsize 800

                                    hbox:
                                        spacing 20
                                        text "Сложность:":
                                            size 16
                                            color "#aaaaaa"

                                        for i in range(case.difficulty):
                                            text "★":
                                                size 20
                                                color "#ff0000"

            textbutton "Назад":
                xalign 0.5
                action Show("main_menu")


## Evidence Journal Screen
screen evidence_journal_screen():
    tag menu
    modal True

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "ЖУРНАЛ УЛИК":
                size 40
                xalign 0.5
                color "#ffffff"

            hbox:
                spacing 50
                xalign 0.5

                # Left panel - list of clues
                vbox:
                    spacing 10
                    xsize 600

                    text "Найденные улики:":
                        size 24
                        color "#ffcc00"

                    viewport:
                        xsize 600
                        ysize 700
                        scrollbars "vertical"
                        mousewheel True

                        vbox:
                            spacing 10

                            python:
                                discovered = evidence_manager.get_discovered_clues()

                            for clue in discovered:
                                button:
                                    xsize 580
                                    background "#2a2a2acc"
                                    hover_background "#3a3a3acc"
                                    action SetVariable("selected_clue", clue)

                                    hbox:
                                        spacing 10
                                        xalign 0.05
                                        yalign 0.5

                                        text "●":
                                            color evidence_manager.get_reliability_color(clue.reliability)
                                            size 20

                                        vbox:
                                            spacing 5
                                            text "[clue.name]":
                                                size 20
                                                color "#ffffff"
                                            text "Тип: [clue.type]":
                                                size 14
                                                color "#aaaaaa"

                # Right panel - clue details
                vbox:
                    spacing 10
                    xsize 700

                    if selected_clue:
                        text "[selected_clue.name]":
                            size 28
                            color "#ffcc00"

                        text "Тип: [selected_clue.type]":
                            size 18
                            color "#cccccc"

                        text "Надёжность: [selected_clue.reliability]%":
                            size 18
                            color evidence_manager.get_reliability_color(selected_clue.reliability)

                        null height 20

                        text "Описание:":
                            size 20
                            color "#ffffff"

                        text "[selected_clue.description]":
                            size 16
                            color "#cccccc"
                            xsize 680

                        null height 20

                        if selected_clue.tags:
                            text "Теги:":
                                size 18
                                color "#ffffff"
                            hbox:
                                spacing 10
                                for tag in selected_clue.tags:
                                    text "[tag]":
                                        size 14
                                        color "#ffcc00"
                                        background "#333333"
                                        xpadding 10
                                        ypadding 5
                    else:
                        text "Выберите улику для просмотра деталей":
                            size 20
                            color "#888888"
                            xalign 0.5
                            yalign 0.5

            textbutton "Закрыть":
                xalign 0.5
                action Hide("evidence_journal_screen")


## World Map Screen
screen world_map_screen():
    tag menu
    modal True

    add "#000000"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1600
        ysize 900
        background "#0a0a0acc"

        # Map background (placeholder)
        add "#1a3a1a":
            xsize 1600
            ysize 900

        # Region labels and locations
        for loc in map_manager.get_all_locations():
            if loc.is_unlocked:
                button:
                    xpos int(loc.map_position.get("x", 0.5) * 1600)
                    ypos int(loc.map_position.get("y", 0.5) * 900)
                    xsize 200
                    ysize 80
                    background "#2a2a2acc"
                    hover_background "#4a4a4acc"
                    action [
                        Function(map_manager.travel_to_location, loc.id),
                        Hide("world_map_screen"),
                        Jump("location_" + loc.id)
                    ]

                    vbox:
                        xalign 0.5
                        yalign 0.5
                        text "[loc.name]":
                            size 18
                            color "#ffcc00"
                            xalign 0.5
                        text "[loc.region]":
                            size 12
                            color "#aaaaaa"
                            xalign 0.5

        # Top panel with title
        frame:
            xalign 0.5
            ypos 20
            xsize 400
            background "#000000cc"

            text "КАРТА КОРОЛЕВСТВА":
                size 30
                xalign 0.5
                yalign 0.5
                color "#ffffff"

        # Close button
        textbutton "Закрыть":
            xalign 0.95
            yalign 0.95
            action Hide("world_map_screen")


## World Codex Screen (Registries)
screen world_codex_screen():
    tag menu
    modal True

    default selected_tab = "characters"

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "ЖУРНАЛ МИРА":
                size 40
                xalign 0.5
                color "#ffffff"

            # Tab buttons
            hbox:
                spacing 20
                xalign 0.5

                textbutton "Персонажи":
                    action SetScreenVariable("selected_tab", "characters")
                    background ("#ffcc00" if selected_tab == "characters" else "#2a2a2a")

                textbutton "Фракции":
                    action SetScreenVariable("selected_tab", "factions")
                    background ("#ffcc00" if selected_tab == "factions" else "#2a2a2a")

                textbutton "Локации":
                    action SetScreenVariable("selected_tab", "locations")
                    background ("#ffcc00" if selected_tab == "locations" else "#2a2a2a")

                textbutton "Дела":
                    action SetScreenVariable("selected_tab", "cases")
                    background ("#ffcc00" if selected_tab == "cases" else "#2a2a2a")

            # Content area
            viewport:
                xsize 1350
                ysize 700
                scrollbars "vertical"
                mousewheel True

                if selected_tab == "characters":
                    use characters_registry()
                elif selected_tab == "factions":
                    use factions_registry()
                elif selected_tab == "locations":
                    use locations_registry()
                elif selected_tab == "cases":
                    use cases_registry()

            textbutton "Закрыть":
                xalign 0.5
                action Hide("world_codex_screen")


## Character Registry
screen characters_registry():
    vbox:
        spacing 20

        for char in game_state.characters.values():
            frame:
                xsize 1300
                background "#2a2a2acc"

                hbox:
                    spacing 30
                    xalign 0.05
                    yalign 0.5

                    vbox:
                        spacing 10

                        text "[char.name]":
                            size 24
                            color "#ffcc00"

                        text "[char.title]":
                            size 18
                            color "#cccccc"

                        text "[char.description]":
                            size 16
                            color "#aaaaaa"
                            xsize 800

                        hbox:
                            spacing 10
                            text "Отношение:":
                                size 16
                                color "#ffffff"

                            text "[char.current_relationship]":
                                size 16
                                color ("#00ff00" if char.current_relationship > 0 else "#ff0000" if char.current_relationship < 0 else "#ffff00")


## Factions Registry
screen factions_registry():
    vbox:
        spacing 20

        for faction in game_state.factions.values():
            frame:
                xsize 1300
                background "#2a2a2acc"

                hbox:
                    spacing 30
                    xalign 0.05
                    yalign 0.5

                    vbox:
                        spacing 10

                        text "[faction.name]":
                            size 24
                            color "#ffcc00"

                        text "Тип: [faction.type]":
                            size 18
                            color "#cccccc"

                        text "[faction.description]":
                            size 16
                            color "#aaaaaa"
                            xsize 800

                        hbox:
                            spacing 10
                            text "Репутация:":
                                size 16
                                color "#ffffff"

                            text "[faction.current_reputation]":
                                size 16
                                color ("#00ff00" if faction.current_reputation > 0 else "#ff0000" if faction.current_reputation < 0 else "#ffff00")


## Locations Registry
screen locations_registry():
    vbox:
        spacing 20

        for loc in game_state.locations.values():
            frame:
                xsize 1300
                background "#2a2a2acc"

                hbox:
                    spacing 30
                    xalign 0.05
                    yalign 0.5

                    vbox:
                        spacing 10

                        text "[loc.name]":
                            size 24
                            color ("#ffcc00" if loc.is_unlocked else "#888888")

                        text "Регион: [loc.region] | Тип: [loc.type]":
                            size 18
                            color "#cccccc"

                        text "[loc.description]":
                            size 16
                            color "#aaaaaa"
                            xsize 800

                        text ("Доступна" if loc.is_unlocked else "Закрыта"):
                            size 16
                            color ("#00ff00" if loc.is_unlocked else "#ff0000")


## Cases Registry
screen cases_registry():
    vbox:
        spacing 20

        for case in game_state.cases.values():
            frame:
                xsize 1300
                background "#2a2a2acc"

                hbox:
                    spacing 30
                    xalign 0.05
                    yalign 0.5

                    vbox:
                        spacing 10

                        text "[case.name]":
                            size 24
                            color "#ffcc00"

                        text "Сложность: [case.difficulty]":
                            size 18
                            color "#cccccc"

                        text "[case.short_description]":
                            size 16
                            color "#aaaaaa"
                            xsize 800

                        text ("Завершено" if case.completed else "В процессе" if case.current_stage > 0 else "Не начато"):
                            size 16
                            color ("#00ff00" if case.completed else "#ffff00" if case.current_stage > 0 else "#888888")


## Interrogation Screen (Phoenix Wright style)
screen interrogation_screen(scene):
    modal True

    default current_statement_index = 0
    default show_penalty = False

    python:
        if current_statement_index < len(scene.statements):
            current_stmt = scene.statements[current_statement_index]
            char = game_state.get_character(scene.character_id)
        else:
            current_stmt = None
            char = None

    add "#000000"

    # Character portrait
    if char:
        frame:
            xalign 0.5
            ypos 50
            background "#00000000"

            # Placeholder for character sprite
            text char.name:
                size 30
                color "#ffffff"

    # Statement text box
    frame:
        xalign 0.5
        ypos 300
        xsize 1400
        background "#1a1a1acc"

        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5

            if current_stmt:
                text "[current_stmt.text]":
                    size 24
                    color "#ffffff"
                    xsize 1350
                    xalign 0.5

    # Mistakes counter
    frame:
        xpos 50
        ypos 50
        background "#ff0000cc"

        text "Ошибки: [scene.current_mistakes]/[scene.max_mistakes]":
            size 20
            color "#ffffff"
            xpadding 20
            ypadding 10

    # Action buttons
    frame:
        xalign 0.5
        ypos 700
        background "#2a2a2acc"

        hbox:
            spacing 50
            xalign 0.5
            yalign 0.5

            textbutton "Нажать (Press)":
                action [
                    Show("show_press_response", stmt=current_stmt),
                    SetScreenVariable("current_statement_index", current_statement_index + 1)
                ]

            textbutton "Предъявить улику (Present)":
                action Show("evidence_selection_screen", scene=scene, stmt_index=current_statement_index)

            if current_statement_index > 0:
                textbutton "← Назад":
                    action SetScreenVariable("current_statement_index", current_statement_index - 1)

            if current_statement_index < len(scene.statements) - 1:
                textbutton "Далее →":
                    action SetScreenVariable("current_statement_index", current_statement_index + 1)

    # Exit button
    textbutton "Завершить допрос":
        xalign 0.95
        yalign 0.95
        action [
            Hide("interrogation_screen"),
            Return()
        ]


## Evidence Selection for Interrogation
screen evidence_selection_screen(scene, stmt_index):
    modal True

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        ysize 700
        background "#1a1a1acc"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "ВЫБЕРИТЕ УЛИКУ":
                size 30
                xalign 0.5
                color "#ffffff"

            viewport:
                xsize 950
                ysize 550
                scrollbars "vertical"
                mousewheel True

                vbox:
                    spacing 10

                    python:
                        discovered = evidence_manager.get_discovered_clues()
                        current_stmt = scene.statements[stmt_index]

                    for clue in discovered:
                        textbutton "[clue.name]":
                            xsize 900
                            action [
                                Function(present_evidence, scene, stmt_index, clue.id),
                                Hide("evidence_selection_screen")
                            ]

            textbutton "Отмена":
                xalign 0.5
                action Hide("evidence_selection_screen")


## Quick Access Menu (during gameplay)
screen quick_menu():
    zorder 100

    hbox:
        xalign 0.5
        yalign 0.98
        spacing 30

        textbutton "Улики":
            action Show("evidence_journal_screen")

        textbutton "Карта":
            action Show("world_map_screen")

        textbutton "Журнал":
            action Show("world_codex_screen")

        textbutton "Сохранить":
            action ShowMenu("save")

        textbutton "Загрузить":
            action ShowMenu("load")

        textbutton "Меню":
            action ShowMenu("main_menu")
