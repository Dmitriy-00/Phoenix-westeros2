# -*- coding: utf-8 -*-
"""
Main Game Script - Integration of All Systems
Главный игровой скрипт с интеграцией всех систем
"""

## Глобальные переменные
default game_state = None
default data_loader = None
default dialogue_manager = None
default evidence_manager = None
default case_manager = None


## Инициализация при старте игры
label start:
    # Показать логотип/заставку (опционально)
    scene bg black with fade

    # Инициализация всех систем
    call initialize_game_systems

    # Показать главное меню или сразу начать игру
    call show_intro

    # Запуск первого дела
    call start_first_case

    return


## Инициализация систем
label initialize_game_systems:
    python:
        # Загрузка настроек
        game_settings.load_settings()

        # Загрузка статистики
        game_statistics.load_statistics()

        # Применение настроек
        game_settings.apply_volume_settings()
        game_settings.apply_text_speed()

        # Создание менеджеров данных
        data_loader = DataLoader()

        # Создание игрового состояния
        game_state = GameState()

        # Загрузка всех игровых данных
        data_loader.load_all_game_data(game_state)

        # Создание менеджеров систем
        dialogue_manager = DialogueManager(game_state)
        evidence_manager = EvidenceManager(game_state)
        case_manager = CaseManager(game_state)

        # Разблокировка стартовых элементов
        character_gallery.unlock_location("loc_stormhold_keep")
        character_gallery.unlock_faction("fact_house_stormhold")

    return


## Вступление
label show_intro:
    # Воспроизведение музыки меню
    python:
        audio_manager.play_music(audio.menu_theme, fadein=2.0)

    scene bg black with fade

    centered "{size=60}{color=#ffcc00}ТЕНИ НАД КОРОЛЕВСТВОМ{/color}{/size}\n\n{size=30}Shadows Over the Kingdom{/size}"

    pause 2.0

    centered "Детективная визуальная новелла\nв стиле Phoenix Wright: Ace Attorney"

    pause 2.0

    # Выбор: новая игра или продолжить
    menu:
        "Начать новую игру":
            jump new_game_setup

        "Загрузить игру":
            call screen load
            return

        "Настройки":
            call screen settings_menu
            jump show_intro

    return


## Настройка новой игры
label new_game_setup:
    scene bg black with fade

    # Опциональный выбор сложности
    if game_settings.difficulty == "normal":
        menu:
            "Выберите уровень сложности:"

            "Лёгкий (Больше подсказок, больше терпения в допросах)":
                python:
                    game_settings.difficulty = "easy"
                    game_settings.show_evidence_hints = True

            "Нормальный (Рекомендуется)":
                python:
                    game_settings.difficulty = "normal"

            "Сложный (Для опытных детективов)":
                python:
                    game_settings.difficulty = "hard"
                    game_settings.show_evidence_hints = False

    # Сохранение настроек
    python:
        game_settings.save_settings()

    return


## Запуск первого дела
label start_first_case:
    # Остановка музыки меню
    python:
        audio_manager.stop_music(fadeout=1.0)

    scene bg black with fade

    # Пролог
    centered "{size=40}Королевство на грани войны.{/size}"

    pause 1.5

    centered "{size=40}Убийство благородного гостя\nгрозит разжечь конфликт между Севером и Югом.{/size}"

    pause 1.5

    centered "{size=40}Вы - детектив,\nи только вы можете найти истину.{/size}"

    pause 2.0

    # Запуск музыки расследования
    python:
        audio_manager.set_music_for_scene("investigation")

    # Переход к первому делу
    jump case_01_start


## Начало дела 1: Тень над Стормхолдом
label case_01_start:
    # Установка текущего дела
    python:
        current_case = game_state.get_case("case_north_murder_01")
        case_manager.start_case("case_north_murder_01")

    # Разблокировка достижений и галереи
    python:
        character_gallery.unlock_location("loc_stormhold_keep")
        auto_unlock_character("char_lord_north")

    # Фон крепости
    scene bg_stormhold_keep with fade
    python:
        audio_manager.set_music_for_location("loc_stormhold_keep")

    # Вступительная сцена
    "Крепость Стормхолд. Серые каменные стены возвышаются над ледяными полями Севера."

    "Вы прибываете по вызову лорда Эйдена Стормхолда. Дело срочное - убийство высокопоставленного гостя с Юга."

    show char_lord_north_neutral at slide_in_left with dissolve

    "Лорд Стормхолд" "Наконец-то! Детектив, я рад, что вы прибыли так быстро."

    "Лорд Стормхолд" "Прошлой ночью был убит посланник дома Золотой Гребень. Это может начать войну!"

    menu:
        "Расскажите мне о произошедшем.":
            jump case_01_lord_dialogue

        "Где находится тело?":
            "Лорд Стормхолд" "В гостевых покоях. Но сначала позвольте объяснить ситуацию..."
            jump case_01_lord_dialogue

        "Кто мог совершить убийство?":
            show char_lord_north_angry
            "Лорд Стормхолд" "Если бы я знал, я бы не вызывал детектива! Но подозреваю... впрочем, не будем спешить с выводами."
            jump case_01_lord_dialogue

    return


## Диалог с лордом (начало расследования)
label case_01_lord_dialogue:
    # Здесь можно подключить систему диалогов из JSON
    # Или написать диалог напрямую в script

    show char_lord_north_neutral

    "Лорд Стормхолд" "Посланник прибыл три дня назад для обсуждения торгового соглашения."

    "Лорд Стормхолд" "Вчера вечером был пир. Все присутствующие могут подтвердить - он был жив и здоров."

    "Лорд Стормхолд" "Утром его нашла горничная. Отравлен. Редкий яд, судя по симптомам."

    # Разблокировка первой улики
    python:
        evidence_manager.discover_clue("clue_poisoned_wine")
        notify_clue_found("Отравленное вино")
        game_statistics.record_evidence("clue_poisoned_wine")

        # Проверка достижений
        check_achievements()

    "Лорд Стормхолд" "У вас полный доступ к крепости. Допрашивайте кого угодно. Но найдите убийцу быстро!"

    # Переход к фазе расследования
    jump investigation_phase


## Фаза расследования (главный цикл)
label investigation_phase:
    # Показать карту с доступными локациями и действиями
    call screen investigation_menu

    return


## Экран меню расследования
screen investigation_menu():
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a2aee"

        vbox:
            spacing 30
            xalign 0.5
            yalign 0.5

            text "ЧТО ВЫ ХОТИТЕ СДЕЛАТЬ?" size 36 xalign 0.5 color "#ffcc00"

            vbox:
                spacing 15
                xalign 0.5

                textbutton "Блокнот (улики)" action ShowMenu("evidence_notebook") xsize 500
                textbutton "Карта (локации)" action ShowMenu("world_map_screen") xsize 500
                textbutton "Персонажи" action ShowMenu("character_gallery_screen") xsize 500
                textbutton "Кодекс" action ShowMenu("codex_main_menu") xsize 500

                null height 20

                textbutton "Продолжить расследование" action Return() xsize 500

                null height 20

                textbutton "Сохранить игру" action ShowMenu("save") xsize 500
                textbutton "Загрузить игру" action ShowMenu("load") xsize 500
                textbutton "Настройки" action ShowMenu("settings_menu") xsize 500


## Автосохранение
label autosave_checkpoint:
    python:
        if game_settings.auto_save:
            renpy.take_screenshot()
            renpy.save("auto-1", "Автосохранение")

            # Сохранение статистики
            game_statistics.save_statistics()

            # Сохранение настроек
            game_settings.save_settings()

    return


## Конец дела (вызывается при завершении расследования)
label case_complete:
    python:
        # Получение текущего дела
        current_case = case_manager.get_current_case()

        # Определение концовки на основе собранных улик и выборов
        ending = case_manager.determine_ending(current_case)

        # Применение эффектов концовки
        case_manager.apply_ending_effects(ending)

        # Запись статистики
        game_statistics.cases_completed += 1
        game_statistics.record_ending(ending.id)

        # Проверка достижений
        check_achievements()

        # Сохранение
        game_statistics.save_statistics()

    # Показ концовки
    scene bg black with fade

    centered "{size=48}{color=#ffcc00}ДЕЛО ЗАКРЫТО{/color}{/size}"

    pause 2.0

    # Показать описание концовки
    python:
        ending_text = ending.description if ending else "Расследование завершено."

    "[ending_text]"

    pause 3.0

    # Показать статистику дела
    call show_case_statistics

    # Переход к следующему делу или главному меню
    menu:
        "Продолжить игру":
            jump next_case_or_menu

        "Вернуться в главное меню":
            return

    return


## Показать статистику дела
label show_case_statistics:
    scene bg black

    python:
        # Подсчёт статистики
        clues_found = len(game_state.discovered_clues)
        total_clues = len(game_state.clues)

    centered "{size=40}СТАТИСТИКА ДЕЛА{/size}\n\n"
    centered "Найдено улик: [clues_found]/[total_clues]\n"
    centered "Проведено допросов: [game_statistics.interrogations_completed]\n"

    pause 3.0

    return


## Следующее дело или меню
label next_case_or_menu:
    # Проверка наличия следующего дела
    python:
        next_case_available = len([c for c in game_state.cases.values() if not c.completed]) > 0

    if next_case_available:
        # Запуск следующего дела
        jump case_02_start
    else:
        # Все дела завершены
        jump game_complete

    return


## Начало дела 2: Заговор в Нептаре
label case_02_start:
    scene bg black with fade

    centered "{size=40}НОВОЕ ДЕЛО{/size}\n\n{size=30}Заговор в Нептаре{/size}"

    pause 2.0

    # Установка дела
    python:
        case_manager.start_case("case_port_conspiracy")
        character_gallery.unlock_location("loc_port_city")

    # Переход к порту
    scene bg_port_city with fade
    python:
        audio_manager.set_music_for_location("loc_port_city")

    "Портовый город Нептара. Шумные доки, запах моря и рыбы."

    "Вас вызвали расследовать серию загадочных убийств богатых торговцев."

    # Встреча с капитаном стражи
    python:
        auto_unlock_character("char_captain_ironhand")

    show char_captain_neutral at slide_in_left with dissolve

    "Капитан Железная Длань" "Детектив! Наконец-то! Три убийства за неделю - город в панике!"

    # Загрузка диалога из JSON
    python:
        dialogue_manager.load_dialogue("dialogue_captain_intro")
        dialogue_manager.start_dialogue()

    # Переход к диалоговой сцене
    jump dialogue_scene

    return


## Завершение игры (все дела пройдены)
label game_complete:
    scene bg black with fade

    python:
        audio_manager.play_music(audio.victory_theme, fadein=2.0)

    centered "{size=60}{color=#ffcc00}ПОЗДРАВЛЯЕМ!{/color}{/size}"

    pause 2.0

    centered "Вы завершили все доступные дела!"

    pause 1.5

    centered "Процент завершения: [game_statistics.get_completion_percentage()]%%"

    pause 2.0

    # Проверка финальных достижений
    python:
        check_achievements()

        # Сохранение финальной статистики
        game_statistics.save_statistics()

    menu:
        "Посмотреть достижения":
            call screen achievements_screen
            jump game_complete

        "Посмотреть галерею":
            call screen character_gallery_screen
            jump game_complete

        "Вернуться в главное меню":
            return

    return


## Обработчик выхода из игры
label quit:
    # Сохранение статистики и настроек
    python:
        game_statistics.save_statistics()
        game_settings.save_settings()

    return


## Интеграционные метки для вызова из других скриптов

# Запуск диалога с персонажем
label talk_to_character(character_id):
    python:
        auto_unlock_character(character_id)

    # Здесь загружается соответствующий диалог
    # jump dialogue_scene

    return


# Осмотр локации
label investigate_location(location_id):
    python:
        auto_unlock_location(location_id)
        play_location_music(location_id)

    # Здесь логика осмотра локации

    return


# Запуск допроса
label start_interrogation(character_id, interrogation_id):
    python:
        play_scene_music("interrogation")

    # Загрузка данных допроса
    # jump interrogation_scene

    return
