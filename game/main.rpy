# -*- coding: utf-8 -*-
"""
Main entry point for the detective visual novel.
Initializes game systems, loads data, and starts the game flow.
"""

## Game Configuration
define config.name = "Тени над Королевством"
define config.version = "0.1.0"
define config.save_directory = "shadows_over_kingdom"

## Developer mode flag
define dev_mode = True

## GUI Configuration
define gui.show_name = True
define gui.text_size = 22
define gui.name_text_size = 30
define gui.interface_text_size = 18
define gui.button_text_size = 24

## Colors
define gui.accent_color = "#ffcc00"
define gui.idle_color = "#888888"
define gui.hover_color = "#ffffff"
define gui.selected_color = "#ffcc00"

## Note: Images are now defined in images.rpy


## Initialization
init python:
    # Create global game state
    game_state = GameState()

    # Create system managers
    dialogue_manager = DialogueManager(game_state)
    relationship_manager = RelationshipManager(game_state)
    evidence_manager = EvidenceManager(game_state)
    map_manager = MapManager(game_state)
    case_manager = CaseManager(game_state)

    # Load all game data
    data_loader.load_all_game_data(game_state)

    # Global variables
    selected_case_id = None
    selected_clue = None
    current_interrogation = None


## Start label - game entry point
label start:
    scene bg black with fade

    # Show quick menu during game
    show screen quick_menu

    # Check if a case was selected
    if selected_case_id:
        # Start the selected case
        $ case_manager.start_case(selected_case_id)
        jump case_start
    else:
        # Default: start first available case
        python:
            if game_state.cases:
                first_case = list(game_state.cases.values())[0]
                case_manager.start_case(first_case.id)

        jump case_start


## Case Start
label case_start:
    python:
        current_case = case_manager.get_current_case()

    if not current_case:
        "Ошибка: Дело не найдено!"
        return

    # Show case introduction
    scene bg black with fade

    centered "{size=40}[current_case.name]{/size}"
    centered "{size=20}[current_case.short_description]{/size}"

    pause 3.0

    # Travel to starting location
    python:
        if current_case.starting_location_id:
            map_manager.travel_to_location(current_case.starting_location_id)

    # Load intro dialogue
    python:
        # Load dialogue nodes for this case
        intro_dialogue = data_loader.load_dialogue_nodes("case_north_murder_01_dialogues.json")
        game_state.dialogue_nodes = intro_dialogue
        dialogue_manager.start_dialogue("case_01_intro", "start")

    # Jump to intro dialogue
    jump dialogue_scene


## Dialogue Scene
label dialogue_scene:
    python:
        current_node = dialogue_manager.get_current_node()

    if not current_node:
        "Диалог завершён."
        hide expression current_speaker_sprite
        jump investigation_phase

    # Get speaker character
    python:
        speaker = game_state.get_character(current_node.speaker_id)
        speaker_name = speaker.name if speaker else "???"

        # Get sprite for current emotion
        if speaker:
            current_speaker_sprite = speaker.get_sprite(current_node.emotion)
        else:
            current_speaker_sprite = None

    # Show character sprite with emotion
    if current_speaker_sprite:
        show expression current_speaker_sprite at slide_in_left with dissolve

    # Display text
    "[speaker_name]" "[current_node.text]"

    # Apply node effects
    python:
        dialogue_manager.apply_effects(current_node.effects)

    # Show choices
    python:
        available_choices = dialogue_manager.get_available_choices(current_node)

    if available_choices:
        menu:
            python:
                for choice in available_choices:
                    renpy.menu_item(choice.get("text", "..."), "dialogue_choice", choice)

    else:
        # No choices, dialogue ends
        jump investigation_phase

    jump dialogue_scene


## Dialogue Choice Handler
label dialogue_choice(choice):
    python:
        dialogue_manager.execute_choice(choice)

    jump dialogue_scene


## Investigation Phase
label investigation_phase:
    # Hide any character sprites
    hide expression current_speaker_sprite

    # Show appropriate background based on current location
    python:
        current_location = map_manager.get_current_location()
        location_name = current_location.name if current_location else "Неизвестно"

        # Map location IDs to background images
        location_bg_map = {
            "loc_stormhold_keep": "bg_stormhold_keep",
            "loc_north_village": "bg_north_village",
            "loc_capital_city": "bg_capital_city",
            "loc_light_cathedral": "bg_light_cathedral",
            "loc_port_city": "bg_port_city",
            "loc_grand_library": "bg_grand_library",
            "loc_holy_monastery": "bg_holy_monastery",
            "loc_trade_hub": "bg_trade_hub"
        }

        if current_location and current_location.id in location_bg_map:
            current_bg = location_bg_map[current_location.id]
        else:
            current_bg = "bg_stormhold_keep"

    scene expression current_bg with fade

    "Вы находитесь: [location_name]"

    menu investigation_menu:
        "Что вы хотите сделать?"

        "Осмотреть локацию":
            jump examine_location

        "Поговорить с персонажем":
            jump talk_to_character

        "Просмотреть улики":
            call screen evidence_journal_screen
            jump investigation_phase

        "Перейти в другую локацию":
            call screen world_map_screen
            jump investigation_phase

        "Начать допрос":
            jump start_interrogation

        "Завершить расследование":
            jump case_conclusion


## Examine Location
label examine_location:
    python:
        current_location = map_manager.get_current_location()

    if current_location:
        "[current_location.description]"

        # Example: discover clue at location
        python:
            # Auto-discover some clues based on location
            if current_location.id == "loc_stormhold_keep":
                if "clue_bloody_letter" not in game_state.discovered_clues:
                    evidence_manager.discover_clue("clue_bloody_letter")
                    "Вы нашли кровавое письмо среди бумаг в покоях!"

    jump investigation_phase


## Talk to Character
label talk_to_character:
    "С кем вы хотите поговорить?"

    menu:
        "Лорд Эйден Стормхолд":
            $ target_char = "char_lord_north"

        "Леди Айрис Стормхолд":
            $ target_char = "char_heir_north"

        "Мейстер Корвин":
            $ target_char = "char_maester_tower"

        "Назад":
            jump investigation_phase

    python:
        character = game_state.get_character(target_char)

    if character:
        # Show character sprite
        python:
            char_sprite = character.get_sprite("neutral")

        show expression char_sprite at slide_in_left with dissolve

        "[character.name]" "Чем могу помочь?"

        # Simple conversation
        menu:
            "Расскажите о себе":
                show expression character.get_sprite("neutral") with dissolve
                "[character.name]" "[character.description]"

            "Что вы знаете об убийстве?":
                show expression character.get_sprite("sad") with dissolve
                "[character.name]" "Это ужасная трагедия..."

            "Назад":
                hide expression char_sprite with dissolve

    jump investigation_phase


## Start Interrogation
label start_interrogation:
    "Кого вы хотите допросить?"

    menu:
        "Мейстер Корвин":
            python:
                interrogation_data = data_loader.load_interrogation_scene(
                    "case_north_murder_01_interrogation.json"
                )
                if interrogation_data:
                    current_interrogation = interrogation_data
                    game_state.interrogation_scenes[interrogation_data.id] = interrogation_data

        "Отмена":
            jump investigation_phase

    if current_interrogation:
        call screen interrogation_screen(current_interrogation)

        python:
            # Check if interrogation was successful
            if current_interrogation.current_mistakes < current_interrogation.max_mistakes:
                # Apply success effects
                dialogue_manager.apply_effects(current_interrogation.success_effects)
                renpy.notify("Допрос успешен!")
            else:
                # Apply failure effects
                dialogue_manager.apply_effects(current_interrogation.failure_effects)
                renpy.notify("Допрос провален!")

    jump investigation_phase


## Case Conclusion
label case_conclusion:
    scene bg throne_hall with fade

    python:
        current_case = case_manager.get_current_case()
        available_endings = case_manager.get_available_endings()

    "Расследование подходит к концу. Пришло время вынести вердикт."

    if available_endings:
        menu:
            "Кого вы обвините в убийстве?"

            "Мейстер Корвин - действовал по приказу Юга":
                $ case_manager.set_case_flag("correct_accusation", True)
                $ case_manager.set_case_flag("accused_character", "char_maester_tower")
                $ chosen_ending = "ending_true_justice"

            "Это был несчастный случай":
                $ case_manager.set_case_flag("wrong_accusation", True)
                $ chosen_ending = "ending_scapegoat"

            "Скрыть правду ради мира":
                $ case_manager.set_case_flag("accusation_hidden", True)
                $ chosen_ending = "ending_political_compromise"

        # Complete case with chosen ending
        $ case_manager.complete_case(chosen_ending)

        # Show ending
        python:
            for ending in current_case.endings:
                if ending.id == chosen_ending:
                    ending_desc = ending.description
                    break
            else:
                ending_desc = "Конец расследования."

        centered "{size=30}[ending_desc]{/size}"

    else:
        "У вас недостаточно улик для вынесения вердикта!"
        jump investigation_phase

    pause 3.0

    "КОНЕЦ ДЕЛА"

    # Return to main menu
    return


## Splash Screen (optional)
label splashscreen:
    scene bg black
    centered "{size=50}Тени над Королевством{/size}"
    pause 2.0
    return


## After Load (restore state)
label after_load:
    return
