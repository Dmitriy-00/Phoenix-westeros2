# -*- coding: utf-8 -*-
"""
Achievements System
Система достижений (ачивок)
"""

init python:
    class Achievement:
        """Одно достижение"""

        def __init__(self, ach_id, name, description, icon=None, hidden=False):
            self.id = ach_id
            self.name = name
            self.description = description
            self.icon = icon
            self.hidden = hidden  # Скрытое достижение (не показывается до разблокировки)
            self.unlocked = False
            self.unlock_date = None

        def unlock(self):
            """Разблокировать достижение"""
            if not self.unlocked:
                self.unlocked = True
                import datetime
                self.unlock_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                return True
            return False


    class AchievementsManager:
        """Менеджер достижений"""

        def __init__(self):
            self.achievements = {}
            self.init_achievements()

        def init_achievements(self):
            """Инициализировать список достижений"""

            # СЮЖЕТНЫЕ ДОСТИЖЕНИЯ
            self.add_achievement("first_case", "Первое дело", "Завершите ваше первое расследование")
            self.add_achievement("all_cases", "Мастер-детектив", "Завершите все доступные дела")
            self.add_achievement("true_justice", "Истинное правосудие", "Получите концовку 'Истинное правосудие'")
            self.add_achievement("dark_path", "Тёмный путь", "Получите концовку с моральным компромиссом")

            # ДОСТИЖЕНИЯ ПО УЛИКАМ
            self.add_achievement("first_clue", "Начинающий сыщик", "Найдите первую улику")
            self.add_achievement("clue_collector", "Коллекционер улик", "Найдите 10 улик")
            self.add_achievement("evidence_master", "Мастер улик", "Найдите все улики в одном деле")

            # ДОСТИЖЕНИЯ ПО ДОПРОСАМ
            self.add_achievement("first_interrogation", "Первый допрос", "Проведите первый допрос")
            self.add_achievement("perfect_interrogation", "Безупречный допрос", "Проведите допрос без единой ошибки")
            self.add_achievement("interrogator", "Опытный следователь", "Проведите 5 допросов")

            # ДОСТИЖЕНИЯ ПО ОТНОШЕНИЯМ
            self.add_achievement("first_friend", "Первый друг", "Достигните +50 отношений с персонажем")
            self.add_achievement("first_enemy", "Первый враг", "Достигните -50 отношений с персонажем")
            self.add_achievement("diplomat", "Дипломат", "Имейте положительные отношения со всеми фракциями")
            self.add_achievement("pariah", "Изгой", "Имейте отрицательные отношения со всеми фракциями")

            # ДОСТИЖЕНИЯ ПО ИССЛЕДОВАНИЮ
            self.add_achievement("explorer", "Исследователь", "Посетите все локации")
            self.add_achievement("lore_master", "Знаток истории", "Разблокируйте все записи в кодексе")
            self.add_achievement("people_person", "Человек среди людей", "Встретьте всех персонажей")

            # СПЕЦИАЛЬНЫЕ ДОСТИЖЕНИЯ
            self.add_achievement("speedrun", "Быстрое правосудие", "Завершите дело менее чем за 1 час игрового времени")
            self.add_achievement("completionist", "Перфекционист", "Получите 100% завершение игры")
            self.add_achievement("church_enemy", "Враг Церкви", "Разоблачите заговор Церкви", hidden=True)
            self.add_achievement("church_ally", "Союзник Церкви", "Помогите Церкви скрыть правду", hidden=True)

            # ПАСХАЛКИ И СЕКРЕТЫ
            self.add_achievement("phoenix_wright_fan", "Фанат Phoenix Wright", "Используйте команду 'Objection!' 10 раз")
            self.add_achievement("book_worm", "Книжный червь", "Прочитайте все записи в библиотеке")

        def add_achievement(self, ach_id, name, description, icon=None, hidden=False):
            """Добавить достижение"""
            self.achievements[ach_id] = Achievement(ach_id, name, description, icon, hidden)

        def unlock_achievement(self, ach_id, show_notification=True):
            """Разблокировать достижение"""
            if ach_id in self.achievements:
                achievement = self.achievements[ach_id]
                if achievement.unlock():
                    # Добавить в глобальную статистику
                    if ach_id not in game_statistics.achievements_unlocked:
                        game_statistics.achievements_unlocked.append(ach_id)

                    # Показать уведомление
                    if show_notification:
                        renpy.show_screen("achievement_notification",
                                        name=achievement.name,
                                        description=achievement.description)
                        renpy.pause(4.0, hard=False)
                        renpy.hide_screen("achievement_notification")

                    # Воспроизвести звук
                    renpy.music.play(audio.sfx_breakthrough, channel="sound")

                    return True
            return False

        def is_unlocked(self, ach_id):
            """Проверить, разблокировано ли достижение"""
            if ach_id in self.achievements:
                return self.achievements[ach_id].unlocked
            return False

        def get_unlocked_count(self):
            """Получить количество разблокированных достижений"""
            return sum(1 for ach in self.achievements.values() if ach.unlocked)

        def get_total_count(self):
            """Получить общее количество достижений"""
            return len(self.achievements)

        def get_achievements_list(self, include_hidden=False):
            """Получить список достижений"""
            if include_hidden:
                return list(self.achievements.values())
            else:
                return [ach for ach in self.achievements.values() if not ach.hidden or ach.unlocked]

        def check_achievement_conditions(self, game_state):
            """Проверить условия получения достижений"""

            # Первая улика
            if len(game_state.discovered_clues) >= 1 and not self.is_unlocked("first_clue"):
                self.unlock_achievement("first_clue")

            # Коллекционер улик
            if game_statistics.evidence_collected >= 10 and not self.is_unlocked("clue_collector"):
                self.unlock_achievement("clue_collector")

            # Первый допрос
            if game_statistics.interrogations_completed >= 1 and not self.is_unlocked("first_interrogation"):
                self.unlock_achievement("first_interrogation")

            # Опытный следователь
            if game_statistics.interrogations_completed >= 5 and not self.is_unlocked("interrogator"):
                self.unlock_achievement("interrogator")

            # Первое дело
            if game_statistics.cases_completed >= 1 and not self.is_unlocked("first_case"):
                self.unlock_achievement("first_case")

            # Мастер-детектив
            if game_statistics.cases_completed >= 2 and not self.is_unlocked("all_cases"):
                self.unlock_achievement("all_cases")

            # Исследователь
            if len(game_statistics.locations_visited) >= 13 and not self.is_unlocked("explorer"):
                self.unlock_achievement("explorer")

            # Человек среди людей
            if len(game_statistics.characters_met) >= 9 and not self.is_unlocked("people_person"):
                self.unlock_achievement("people_person")

            # Перфекционист
            if game_statistics.get_completion_percentage() >= 100 and not self.is_unlocked("completionist"):
                self.unlock_achievement("completionist")

            # Проверка отношений
            for char in game_state.characters.values():
                if char.current_relationship >= 50 and not self.is_unlocked("first_friend"):
                    self.unlock_achievement("first_friend")
                if char.current_relationship <= -50 and not self.is_unlocked("first_enemy"):
                    self.unlock_achievement("first_enemy")

    # Глобальный менеджер достижений
    achievements_manager = AchievementsManager()


## Экран уведомления о достижении
screen achievement_notification(name, description):
    zorder 200

    frame:
        xalign 0.5
        yalign 0.2
        padding (40, 30)
        background "#1a1a2aee"

        at transform:
            alpha 0.0 yoffset -50
            ease 0.5 alpha 1.0 yoffset 0
            pause 3.0
            ease 0.5 alpha 0.0 yoffset -50

        vbox:
            spacing 15

            text "🏆 ДОСТИЖЕНИЕ ПОЛУЧЕНО! 🏆":
                size 24
                color "#ffcc00"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[name]":
                size 32
                color "#ffffff"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[description]":
                size 18
                color "#cccccc"
                xalign 0.5
                outlines [(1, "#000000", 0, 0)]


## Экран списка достижений
screen achievements_screen():
    tag menu
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 900
        background "#1a1a2a"

        vbox:
            spacing 20

            # Заголовок
            hbox:
                spacing 20
                xalign 0.5

                text "ДОСТИЖЕНИЯ" size 48 color "#ffcc00"

                $ unlocked = achievements_manager.get_unlocked_count()
                $ total = achievements_manager.get_total_count()
                text "{}/{}".format(unlocked, total) size 32 color "#ffffff"

            # Прогресс-бар
            frame:
                xsize 1100
                xalign 0.5
                background "#2a2a3a"
                padding (20, 10)

                vbox:
                    spacing 5

                    text "Общий прогресс:" size 20 color "#cccccc"

                    $ progress = (unlocked / float(total)) if total > 0 else 0.0

                    bar:
                        value progress
                        range 1.0
                        xsize 1060
                        style "achievement_progress_bar"

            null height 10

            # Список достижений
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 1150
                ysize 650

                vbox:
                    spacing 10

                    for ach in achievements_manager.get_achievements_list():
                        frame:
                            padding (20, 15)
                            xsize 1100
                            background "#2a2a3a" if ach.unlocked else "#1a1a1a"

                            hbox:
                                spacing 20

                                # Иконка
                                frame:
                                    xysize (60, 60)
                                    background "#ffcc00" if ach.unlocked else "#666666"

                                    text "🏆" if ach.unlocked else "🔒":
                                        size 36
                                        xalign 0.5
                                        yalign 0.5

                                # Информация
                                vbox:
                                    spacing 5

                                    if ach.unlocked or not ach.hidden:
                                        text "[ach.name]":
                                            size 24
                                            color "#ffcc00" if ach.unlocked else "#666666"

                                        text "[ach.description]":
                                            size 18
                                            color "#ffffff" if ach.unlocked else "#666666"

                                        if ach.unlocked and ach.unlock_date:
                                            text "Получено: [ach.unlock_date]":
                                                size 14
                                                color "#aaaaaa"
                                    else:
                                        text "???":
                                            size 24
                                            color "#666666"

                                        text "Скрытое достижение":
                                            size 18
                                            color "#666666"

            # Кнопка возврата
            textbutton "Назад" action Return() xalign 0.5


## Стиль для прогресс-бара достижений
style achievement_progress_bar:
    xsize 1060
    ysize 20

style achievement_progress_bar_full:
    background "#00ff00"

style achievement_progress_bar_empty:
    background "#333333"


## Функции для вызова из скриптов
init python:
    def unlock_ach(ach_id):
        """Разблокировать достижение (короткая форма)"""
        achievements_manager.unlock_achievement(ach_id)

    def check_achievements():
        """Проверить условия достижений"""
        achievements_manager.check_achievement_conditions(game_state)
