# -*- coding: utf-8 -*-
"""
Settings and Preferences System
Управление настройками игры, сохранениями и предпочтениями игрока
"""

init python:
    class GameSettings:
        """Глобальные настройки игры"""

        def __init__(self):
            # Настройки звука
            self.master_volume = 1.0
            self.music_volume = 0.7
            self.sfx_volume = 0.8
            self.voice_volume = 1.0

            # Настройки текста
            self.text_speed = 50  # 0-100
            self.auto_forward_delay = 3.0  # секунды
            self.skip_unread = False
            self.skip_after_choices = True

            # Настройки интерфейса
            self.show_hints = True
            self.show_relationship_changes = True
            self.show_clue_notifications = True
            self.fullscreen = False
            self.language = "ru"

            # Настройки геймплея
            self.difficulty = "normal"  # easy, normal, hard
            self.show_evidence_hints = True
            self.auto_save = True
            self.quick_save_slots = 10

        def apply_volume_settings(self):
            """Применить настройки громкости"""
            preferences.set_volume("music", self.music_volume * self.master_volume)
            preferences.set_volume("sfx", self.sfx_volume * self.master_volume)
            preferences.set_volume("voice", self.voice_volume * self.master_volume)

        def apply_text_speed(self):
            """Применить скорость текста"""
            preferences.text_cps = int(self.text_speed)
            preferences.afm_time = int(self.auto_forward_delay * 1000)

        def toggle_fullscreen(self):
            """Переключить полноэкранный режим"""
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                renpy.display.interface.set_mode("fullscreen")
            else:
                renpy.display.interface.set_mode("windowed")

        def save_settings(self):
            """Сохранить настройки"""
            import json
            settings_dict = {
                "master_volume": self.master_volume,
                "music_volume": self.music_volume,
                "sfx_volume": self.sfx_volume,
                "voice_volume": self.voice_volume,
                "text_speed": self.text_speed,
                "auto_forward_delay": self.auto_forward_delay,
                "skip_unread": self.skip_unread,
                "skip_after_choices": self.skip_after_choices,
                "show_hints": self.show_hints,
                "show_relationship_changes": self.show_relationship_changes,
                "show_clue_notifications": self.show_clue_notifications,
                "fullscreen": self.fullscreen,
                "language": self.language,
                "difficulty": self.difficulty,
                "show_evidence_hints": self.show_evidence_hints,
                "auto_save": self.auto_save,
                "quick_save_slots": self.quick_save_slots
            }

            try:
                with renpy.file("settings.json", "w") as f:
                    f.write(json.dumps(settings_dict, indent=2, ensure_ascii=False))
            except:
                pass

        def load_settings(self):
            """Загрузить настройки"""
            import json
            try:
                with renpy.file("settings.json") as f:
                    settings_dict = json.loads(f.read())

                self.master_volume = settings_dict.get("master_volume", 1.0)
                self.music_volume = settings_dict.get("music_volume", 0.7)
                self.sfx_volume = settings_dict.get("sfx_volume", 0.8)
                self.voice_volume = settings_dict.get("voice_volume", 1.0)
                self.text_speed = settings_dict.get("text_speed", 50)
                self.auto_forward_delay = settings_dict.get("auto_forward_delay", 3.0)
                self.skip_unread = settings_dict.get("skip_unread", False)
                self.skip_after_choices = settings_dict.get("skip_after_choices", True)
                self.show_hints = settings_dict.get("show_hints", True)
                self.show_relationship_changes = settings_dict.get("show_relationship_changes", True)
                self.show_clue_notifications = settings_dict.get("show_clue_notifications", True)
                self.fullscreen = settings_dict.get("fullscreen", False)
                self.language = settings_dict.get("language", "ru")
                self.difficulty = settings_dict.get("difficulty", "normal")
                self.show_evidence_hints = settings_dict.get("show_evidence_hints", True)
                self.auto_save = settings_dict.get("auto_save", True)
                self.quick_save_slots = settings_dict.get("quick_save_slots", 10)

                # Применить настройки
                self.apply_volume_settings()
                self.apply_text_speed()
            except:
                pass

    # Глобальный объект настроек
    game_settings = GameSettings()


    class GameStatistics:
        """Статистика игры"""

        def __init__(self):
            self.total_playtime = 0.0  # секунды
            self.cases_completed = 0
            self.cases_failed = 0
            self.total_choices_made = 0
            self.evidence_collected = 0
            self.interrogations_completed = 0
            self.perfect_interrogations = 0  # без ошибок
            self.relationships_maxed = 0  # персонажей с максимальными отношениями
            self.achievements_unlocked = []
            self.endings_seen = []
            self.characters_met = []
            self.locations_visited = []

        def save_statistics(self):
            """Сохранить статистику"""
            import json
            stats_dict = {
                "total_playtime": self.total_playtime,
                "cases_completed": self.cases_completed,
                "cases_failed": self.cases_failed,
                "total_choices_made": self.total_choices_made,
                "evidence_collected": self.evidence_collected,
                "interrogations_completed": self.interrogations_completed,
                "perfect_interrogations": self.perfect_interrogations,
                "relationships_maxed": self.relationships_maxed,
                "achievements_unlocked": self.achievements_unlocked,
                "endings_seen": self.endings_seen,
                "characters_met": self.characters_met,
                "locations_visited": self.locations_visited
            }

            try:
                with renpy.file("statistics.json", "w") as f:
                    f.write(json.dumps(stats_dict, indent=2, ensure_ascii=False))
            except:
                pass

        def load_statistics(self):
            """Загрузить статистику"""
            import json
            try:
                with renpy.file("statistics.json") as f:
                    stats_dict = json.loads(f.read())

                self.total_playtime = stats_dict.get("total_playtime", 0.0)
                self.cases_completed = stats_dict.get("cases_completed", 0)
                self.cases_failed = stats_dict.get("cases_failed", 0)
                self.total_choices_made = stats_dict.get("total_choices_made", 0)
                self.evidence_collected = stats_dict.get("evidence_collected", 0)
                self.interrogations_completed = stats_dict.get("interrogations_completed", 0)
                self.perfect_interrogations = stats_dict.get("perfect_interrogations", 0)
                self.relationships_maxed = stats_dict.get("relationships_maxed", 0)
                self.achievements_unlocked = stats_dict.get("achievements_unlocked", [])
                self.endings_seen = stats_dict.get("endings_seen", [])
                self.characters_met = stats_dict.get("characters_met", [])
                self.locations_visited = stats_dict.get("locations_visited", [])
            except:
                pass

        def record_choice(self):
            """Записать сделанный выбор"""
            self.total_choices_made += 1

        def record_evidence(self, clue_id):
            """Записать найденную улику"""
            self.evidence_collected += 1

        def record_interrogation(self, perfect=False):
            """Записать завершённый допрос"""
            self.interrogations_completed += 1
            if perfect:
                self.perfect_interrogations += 1

        def record_ending(self, ending_id):
            """Записать увиденную концовку"""
            if ending_id not in self.endings_seen:
                self.endings_seen.append(ending_id)

        def record_character(self, character_id):
            """Записать встреченного персонажа"""
            if character_id not in self.characters_met:
                self.characters_met.append(character_id)

        def record_location(self, location_id):
            """Записать посещённую локацию"""
            if location_id not in self.locations_visited:
                self.locations_visited.append(location_id)

        def get_completion_percentage(self):
            """Получить процент завершения игры"""
            total_content = {
                "endings": 10,  # примерное количество концовок
                "characters": 9,  # текущее количество персонажей
                "locations": 13,  # текущее количество локаций
                "cases": 2  # текущее количество дел
            }

            current_completion = (
                len(self.endings_seen) / total_content["endings"] +
                len(self.characters_met) / total_content["characters"] +
                len(self.locations_visited) / total_content["locations"] +
                self.cases_completed / total_content["cases"]
            ) / 4.0

            return min(100, int(current_completion * 100))

    # Глобальный объект статистики
    game_statistics = GameStatistics()


## Экран настроек
screen settings_menu():
    tag menu
    modal True

    style_prefix "game_menu"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 800

        vbox:
            spacing 20
            xfill True

            # Заголовок
            text "НАСТРОЙКИ" size 48 xalign 0.5 color "#ffcc00"

            # Табы
            hbox:
                spacing 20
                xalign 0.5

                textbutton "Звук" action SetVariable("settings_tab", "audio")
                textbutton "Текст" action SetVariable("settings_tab", "text")
                textbutton "Интерфейс" action SetVariable("settings_tab", "interface")
                textbutton "Геймплей" action SetVariable("settings_tab", "gameplay")

            null height 20

            # Содержимое вкладок
            if settings_tab == "audio":
                use settings_audio_tab
            elif settings_tab == "text":
                use settings_text_tab
            elif settings_tab == "interface":
                use settings_interface_tab
            elif settings_tab == "gameplay":
                use settings_gameplay_tab

            null height 40

            # Кнопки управления
            hbox:
                spacing 30
                xalign 0.5

                textbutton "Применить" action [
                    Function(game_settings.apply_volume_settings),
                    Function(game_settings.apply_text_speed),
                    Function(game_settings.save_settings)
                ]

                textbutton "По умолчанию" action [
                    SetField(game_settings, "master_volume", 1.0),
                    SetField(game_settings, "music_volume", 0.7),
                    SetField(game_settings, "sfx_volume", 0.8),
                    SetField(game_settings, "text_speed", 50),
                    Function(game_settings.apply_volume_settings),
                    Function(game_settings.apply_text_speed)
                ]

                textbutton "Назад" action Return()


## Вкладка звука
screen settings_audio_tab():
    vbox:
        spacing 30
        xsize 1000
        xalign 0.5

        # Общая громкость
        hbox:
            text "Общая громкость:" xsize 400
            bar value FieldValue(game_settings, "master_volume", 1.0) xsize 500
            text "{:.0f}%".format(game_settings.master_volume * 100) xsize 100

        # Музыка
        hbox:
            text "Музыка:" xsize 400
            bar value FieldValue(game_settings, "music_volume", 1.0) xsize 500
            text "{:.0f}%".format(game_settings.music_volume * 100) xsize 100

        # Звуковые эффекты
        hbox:
            text "Звуковые эффекты:" xsize 400
            bar value FieldValue(game_settings, "sfx_volume", 1.0) xsize 500
            text "{:.0f}%".format(game_settings.sfx_volume * 100) xsize 100

        # Голоса
        hbox:
            text "Голоса:" xsize 400
            bar value FieldValue(game_settings, "voice_volume", 1.0) xsize 500
            text "{:.0f}%".format(game_settings.voice_volume * 100) xsize 100


## Вкладка текста
screen settings_text_tab():
    vbox:
        spacing 30
        xsize 1000
        xalign 0.5

        # Скорость текста
        hbox:
            text "Скорость текста:" xsize 400
            bar value FieldValue(game_settings, "text_speed", 100) xsize 500
            text str(game_settings.text_speed) xsize 100

        # Задержка авто-режима
        hbox:
            text "Задержка авто-режима (сек):" xsize 400
            bar value FieldValue(game_settings, "auto_forward_delay", 10.0) xsize 500
            text "{:.1f}".format(game_settings.auto_forward_delay) xsize 100

        # Пропуск непрочитанного
        hbox:
            text "Пропускать непрочитанное:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "skip_unread", True):
                selected game_settings.skip_unread
            textbutton "ВЫКЛ" action SetField(game_settings, "skip_unread", False):
                selected not game_settings.skip_unread

        # Пропуск после выборов
        hbox:
            text "Продолжать пропуск после выборов:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "skip_after_choices", True):
                selected game_settings.skip_after_choices
            textbutton "ВЫКЛ" action SetField(game_settings, "skip_after_choices", False):
                selected not game_settings.skip_after_choices


## Вкладка интерфейса
screen settings_interface_tab():
    vbox:
        spacing 30
        xsize 1000
        xalign 0.5

        # Показывать подсказки
        hbox:
            text "Показывать подсказки:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "show_hints", True):
                selected game_settings.show_hints
            textbutton "ВЫКЛ" action SetField(game_settings, "show_hints", False):
                selected not game_settings.show_hints

        # Показывать изменения отношений
        hbox:
            text "Показывать изменения отношений:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "show_relationship_changes", True):
                selected game_settings.show_relationship_changes
            textbutton "ВЫКЛ" action SetField(game_settings, "show_relationship_changes", False):
                selected not game_settings.show_relationship_changes

        # Уведомления об уликах
        hbox:
            text "Уведомления о новых уликах:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "show_clue_notifications", True):
                selected game_settings.show_clue_notifications
            textbutton "ВЫКЛ" action SetField(game_settings, "show_clue_notifications", False):
                selected not game_settings.show_clue_notifications

        # Полноэкранный режим
        hbox:
            text "Полноэкранный режим:" xsize 400
            textbutton "ВКЛ" action Function(game_settings.toggle_fullscreen):
                selected game_settings.fullscreen
            textbutton "ВЫКЛ" action Function(game_settings.toggle_fullscreen):
                selected not game_settings.fullscreen


## Вкладка геймплея
screen settings_gameplay_tab():
    vbox:
        spacing 30
        xsize 1000
        xalign 0.5

        # Сложность
        hbox:
            text "Сложность:" xsize 400
            textbutton "Лёгкая" action SetField(game_settings, "difficulty", "easy"):
                selected game_settings.difficulty == "easy"
            textbutton "Нормальная" action SetField(game_settings, "difficulty", "normal"):
                selected game_settings.difficulty == "normal"
            textbutton "Сложная" action SetField(game_settings, "difficulty", "hard"):
                selected game_settings.difficulty == "hard"

        # Подсказки по уликам
        hbox:
            text "Подсказки по уликам:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "show_evidence_hints", True):
                selected game_settings.show_evidence_hints
            textbutton "ВЫКЛ" action SetField(game_settings, "show_evidence_hints", False):
                selected not game_settings.show_evidence_hints

        # Автосохранение
        hbox:
            text "Автосохранение:" xsize 400
            textbutton "ВКЛ" action SetField(game_settings, "auto_save", True):
                selected game_settings.auto_save
            textbutton "ВЫКЛ" action SetField(game_settings, "auto_save", False):
                selected not game_settings.auto_save


## Инициализация при старте игры
label init_settings:
    python:
        game_settings.load_settings()
        game_statistics.load_statistics()
    return


## Переменная для текущей вкладки настроек
default settings_tab = "audio"
