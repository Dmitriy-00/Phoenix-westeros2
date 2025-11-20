# -*- coding: utf-8 -*-
"""
Character Gallery / Codex
Галерея персонажей и кодекс игрового мира
"""

init python:
    class CharacterGallery:
        """Галерея персонажей"""

        def __init__(self):
            self.unlocked_characters = []
            self.unlocked_factions = []
            self.unlocked_locations = []
            self.unlocked_lore = []

        def unlock_character(self, character_id):
            """Разблокировать персонажа в галерее"""
            if character_id not in self.unlocked_characters:
                self.unlocked_characters.append(character_id)
                game_statistics.record_character(character_id)

        def unlock_faction(self, faction_id):
            """Разблокировать фракцию в галерее"""
            if faction_id not in self.unlocked_factions:
                self.unlocked_factions.append(faction_id)

        def unlock_location(self, location_id):
            """Разблокировать локацию в галерее"""
            if location_id not in self.unlocked_locations:
                self.unlocked_locations.append(location_id)
                game_statistics.record_location(location_id)

        def is_character_unlocked(self, character_id):
            """Проверить, разблокирован ли персонаж"""
            return character_id in self.unlocked_characters

        def get_character_info(self, character_id, game_state):
            """Получить информацию о персонаже"""
            char = game_state.get_character(character_id)
            if char and self.is_character_unlocked(character_id):
                return {
                    "name": char.name,
                    "title": char.title,
                    "description": char.description,
                    "faction": char.faction_id,
                    "relationship": char.current_relationship,
                    "traits": char.traits
                }
            return None

    # Глобальная галерея
    character_gallery = CharacterGallery()


## Экран галереи персонажей
screen character_gallery_screen():
    tag menu
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a2a"

        vbox:
            spacing 20

            # Заголовок
            text "ГАЛЕРЕЯ ПЕРСОНАЖЕЙ" size 48 xalign 0.5 color "#ffcc00"

            null height 20

            # Список персонажей
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 1350
                ysize 700

                vbox:
                    spacing 15

                    # Перебор всех персонажей
                    for char_id in ["char_lord_north", "char_heir_north", "char_maester_tower",
                                   "char_cardinal_south", "char_merchant_prince",
                                   "char_captain_ironhand", "char_lady_isabella",
                                   "char_brother_theodore", "char_alex_swiftblade"]:

                        $ unlocked = character_gallery.is_character_unlocked(char_id)

                        hbox:
                            spacing 30

                            # Портрет
                            if unlocked:
                                add "{}_neutral".format(char_id) zoom 0.4
                            else:
                                frame:
                                    xysize (160, 240)
                                    background "#000000"
                                    text "???" size 48 xalign 0.5 yalign 0.5 color "#666666"

                            # Информация
                            vbox:
                                spacing 10

                                if unlocked:
                                    $ char = game_state.get_character(char_id)
                                    if char:
                                        text "[char.name]" size 32 color "#ffcc00"
                                        text "[char.title]" size 20 color "#cccccc" italic True
                                        text "[char.description]" size 18 color "#ffffff" xsize 900

                                        # Отношения
                                        hbox:
                                            spacing 10
                                            text "Отношения:" size 18
                                            $ rel = char.current_relationship
                                            $ rel_color = "#00ff00" if rel > 0 else "#ff0000" if rel < 0 else "#ffffff"
                                            text "{:+d}".format(rel) size 18 color rel_color

                                        # Черты характера
                                        if char.traits:
                                            text "Черты: {}".format(", ".join(char.traits)) size 16 color "#aaaaaa"
                                else:
                                    text "???" size 32 color "#666666"
                                    text "Персонаж ещё не встречен" size 20 color "#666666" italic True

            # Кнопка возврата
            textbutton "Назад" action Return() xalign 0.5


## Экран фракций
screen faction_codex_screen():
    tag menu
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a2a"

        vbox:
            spacing 20

            text "КОДЕКС ФРАКЦИЙ" size 48 xalign 0.5 color "#ffcc00"

            null height 20

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 1350
                ysize 700

                vbox:
                    spacing 20

                    for faction_id in ["fact_house_stormhold", "fact_house_goldcrest",
                                       "fact_crown", "fact_eternal_light",
                                       "fact_merchants_guild", "fact_scholars_circle",
                                       "fact_city_guard"]:

                        $ unlocked = faction_id in character_gallery.unlocked_factions
                        $ faction_bg = "#2a2a3a" if unlocked else "#1a1a1a"

                        frame:
                            padding (30, 20)
                            xsize 1300
                            background faction_bg

                            vbox:
                                spacing 10

                                if unlocked:
                                    $ faction = game_state.get_faction(faction_id)
                                    if faction:
                                        text "[faction.name]" size 28 color "#ffcc00"
                                        text "[faction.description]" size 18 color "#ffffff"

                                        hbox:
                                            spacing 10
                                            text "Репутация:" size 18
                                            $ rep = faction.current_reputation
                                            $ rep_color = "#00ff00" if rep > 0 else "#ff0000" if rep < 0 else "#ffffff"
                                            text "{:+d}".format(rep) size 18 color rep_color
                                else:
                                    text "???" size 28 color "#666666"
                                    text "Фракция ещё не открыта" size 18 color "#666666"

            textbutton "Назад" action Return() xalign 0.5


## Экран локаций
screen location_codex_screen():
    tag menu
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        background "#1a1a2a"

        vbox:
            spacing 20

            text "КОДЕКС ЛОКАЦИЙ" size 48 xalign 0.5 color "#ffcc00"

            null height 20

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 1350
                ysize 700

                vbox:
                    spacing 15

                    for location_id in ["loc_stormhold_keep", "loc_north_village",
                                        "loc_capital_city", "loc_light_cathedral",
                                        "loc_port_city", "loc_grand_library",
                                        "loc_holy_monastery", "loc_trade_hub",
                                        "loc_marcus_house", "loc_selina_warehouse",
                                        "loc_golden_sail", "loc_salty_mermaid",
                                        "loc_guard_station"]:

                        $ unlocked = location_id in character_gallery.unlocked_locations

                        hbox:
                            spacing 30

                            # Фон локации (миниатюра)
                            if unlocked:
                                $ bg_name = location_id.replace("loc_", "bg_")
                                add bg_name zoom 0.15
                            else:
                                frame:
                                    xysize (288, 162)
                                    background "#000000"
                                    text "???" size 36 xalign 0.5 yalign 0.5 color "#666666"

                            # Информация
                            vbox:
                                spacing 10

                                if unlocked:
                                    $ location = game_state.world_map.get_location(location_id)
                                    if location:
                                        text "[location.name]" size 28 color "#ffcc00"
                                        text "[location.description]" size 18 color "#ffffff" xsize 950
                                        text "Регион: [location.region]" size 16 color "#aaaaaa"
                                else:
                                    text "???" size 28 color "#666666"
                                    text "Локация ещё не посещена" size 18 color "#666666"

            textbutton "Назад" action Return() xalign 0.5


## Главное меню кодекса
screen codex_main_menu():
    tag menu
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a2a"

        vbox:
            spacing 40
            xalign 0.5
            yalign 0.5

            text "КОДЕКС" size 60 xalign 0.5 color "#ffcc00"

            vbox:
                spacing 20
                xalign 0.5

                textbutton "Персонажи" action Show("character_gallery_screen") xsize 400
                textbutton "Фракции" action Show("faction_codex_screen") xsize 400
                textbutton "Локации" action Show("location_codex_screen") xsize 400
                textbutton "Достижения" action Show("achievements_screen") xsize 400
                textbutton "Статистика" action Show("statistics_screen") xsize 400

            textbutton "Назад" action Return() xalign 0.5


## Экран статистики
screen statistics_screen():
    tag menu
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        ysize 700
        background "#1a1a2a"

        vbox:
            spacing 30

            text "СТАТИСТИКА" size 48 xalign 0.5 color "#ffcc00"

            null height 20

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 950
                ysize 500

                vbox:
                    spacing 20

                    # Общая статистика
                    frame:
                        padding (20, 15)
                        xsize 900
                        background "#2a2a3a"

                        vbox:
                            spacing 10

                            text "ОБЩЕЕ" size 24 color "#ffcc00"

                            $ hours = int(game_statistics.total_playtime // 3600)
                            $ minutes = int((game_statistics.total_playtime % 3600) // 60)
                            text "Время игры: {}ч {}м".format(hours, minutes) size 18

                            text "Завершено дел: {}".format(game_statistics.cases_completed) size 18
                            text "Провалено дел: {}".format(game_statistics.cases_failed) size 18
                            text "Процент завершения: {}%".format(game_statistics.get_completion_percentage()) size 18

                    # Детективная работа
                    frame:
                        padding (20, 15)
                        xsize 900
                        background "#2a2a3a"

                        vbox:
                            spacing 10

                            text "ДЕТЕКТИВНАЯ РАБОТА" size 24 color "#ffcc00"

                            text "Найдено улик: {}".format(game_statistics.evidence_collected) size 18
                            text "Проведено допросов: {}".format(game_statistics.interrogations_completed) size 18
                            text "Идеальных допросов: {}".format(game_statistics.perfect_interrogations) size 18

                    # Выборы и отношения
                    frame:
                        padding (20, 15)
                        xsize 900
                        background "#2a2a3a"

                        vbox:
                            spacing 10

                            text "ВЫБОРЫ И ОТНОШЕНИЯ" size 24 color "#ffcc00"

                            text "Сделано выборов: {}".format(game_statistics.total_choices_made) size 18
                            text "Максимальных отношений: {}".format(game_statistics.relationships_maxed) size 18

                    # Исследование мира
                    frame:
                        padding (20, 15)
                        xsize 900
                        background "#2a2a3a"

                        vbox:
                            spacing 10

                            text "ИССЛЕДОВАНИЕ МИРА" size 24 color "#ffcc00"

                            text "Встречено персонажей: {}/9".format(len(game_statistics.characters_met)) size 18
                            text "Посещено локаций: {}/13".format(len(game_statistics.locations_visited)) size 18
                            text "Увидено концовок: {}/10".format(len(game_statistics.endings_seen)) size 18

            textbutton "Назад" action Return() xalign 0.5


## Функции автоматической разблокировки
init python:
    def auto_unlock_character(character_id):
        """Автоматически разблокировать персонажа при встрече"""
        character_gallery.unlock_character(character_id)

    def auto_unlock_location(location_id):
        """Автоматически разблокировать локацию при посещении"""
        character_gallery.unlock_location(location_id)

    def auto_unlock_faction(faction_id):
        """Автоматически разблокировать фракцию"""
        character_gallery.unlock_faction(faction_id)
