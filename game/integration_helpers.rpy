# -*- coding: utf-8 -*-
"""
Integration Helpers
Вспомогательные функции для интеграции систем
"""

## Автосохранение при выборах
init python:
    def after_choice_callback():
        """Вызывается после каждого выбора игрока"""
        # Записать выбор в статистику
        game_statistics.record_choice()

        # Автосохранение
        if game_settings.auto_save:
            renpy.save("auto-1")

        # Проверить достижения
        check_achievements()


## Автосохранение в ключевых точках
label checkpoint(checkpoint_name="Checkpoint"):
    python:
        if game_settings.auto_save:
            renpy.save("auto-1", checkpoint_name)
            game_statistics.save_statistics()

    return


## Интеграция находки улики
label discover_clue_integrated(clue_id):
    python:
        # Добавить улику
        evidence_manager.discover_clue(clue_id)

        # Получить информацию об улике
        clue = game_state.get_clue(clue_id)
        clue_name = clue.name if clue else "Неизвестная улика"

        # Показать уведомление
        if game_settings.show_clue_notifications:
            notify_clue_found(clue_name)

        # Записать в статистику
        game_statistics.record_evidence(clue_id)

        # Проверить достижения
        check_achievements()

        # Автосохранение
        if game_settings.auto_save:
            renpy.save("auto-1", "Улика: {}".format(clue_name))

    return


## Интеграция изменения отношений
init python:
    def modify_relationship_integrated(character_id, amount):
        """Изменить отношения и показать уведомление"""
        # Получить персонажа
        char = game_state.get_character(character_id)
        if not char:
            return

        old_relationship = char.current_relationship

        # Изменить отношения
        char.modify_relationship(amount)

        # Показать уведомление
        if game_settings.show_relationship_changes and amount != 0:
            notify_relationship_change(char.name, amount)

        # Проверить достижения (новые друзья/враги)
        new_relationship = char.current_relationship

        if old_relationship < 50 and new_relationship >= 50:
            unlock_ach("first_friend")
        elif old_relationship > -50 and new_relationship <= -50:
            unlock_ach("first_enemy")

        check_achievements()


## Начало допроса (интегрированная версия)
label start_interrogation_integrated(interrogation_id):
    python:
        # Установить музыку
        play_scene_music("interrogation")

        # Загрузить данные допроса
        # (здесь код загрузки из JSON)

        # Автосохранение перед допросом
        if game_settings.auto_save:
            renpy.save("auto-interrogation", "Перед допросом")

    # Переход к сцене допроса
    call interrogation_scene

    python:
        # После допроса - записать статистику
        # perfect определяется в зависимости от количества ошибок
        perfect = False  # Заменить на реальную проверку

        game_statistics.record_interrogation(perfect)

        if perfect:
            unlock_ach("perfect_interrogation")

        check_achievements()

        # Автосохранение после допроса
        if game_settings.auto_save:
            renpy.save("auto-1", "После допроса")

    return


## Завершение дела (интегрированная версия)
label complete_case_integrated(case_id, ending_id):
    python:
        # Получить дело
        current_case = game_state.get_case(case_id)
        if not current_case:
            return

        # Пометить как завершённое
        current_case.completed = True

        # Записать статистику
        game_statistics.cases_completed += 1
        game_statistics.record_ending(ending_id)

        # Разблокировать достижения
        unlock_ach("first_case")

        # Специфичные достижения по концовкам
        if ending_id == "ending_true_justice":
            unlock_ach("true_justice")
        elif "compromise" in ending_id or "coverup" in ending_id:
            unlock_ach("dark_path")

        if ending_id.startswith("case_port") and "church" in ending_id:
            unlock_ach("church_enemy")

        # Проверить все достижения
        check_achievements()

        # Финальное сохранение
        game_statistics.save_statistics()
        renpy.save("auto-case-complete", "Дело завершено")

    # Показать концовку
    jump show_case_ending

    return


## Показ концовки дела
label show_case_ending:
    scene bg black with fade

    python:
        audio_manager.play_music(audio.revelation_theme, fadein=2.0)

    centered "{size=60}{color=#ffcc00}ДЕЛО ЗАКРЫТО{/color}{/size}"

    pause 2.0

    # Здесь показывается текст концовки
    # ...

    pause 3.0

    return


## Быстрые функции для интеграции в диалогах

init python:
    def quick_clue(clue_id):
        """Быстрое добавление улики"""
        renpy.call("discover_clue_integrated", clue_id)

    def quick_relationship(character_id, amount):
        """Быстрое изменение отношений"""
        modify_relationship_integrated(character_id, amount)

    def quick_unlock_location(location_id):
        """Быстрая разблокировка локации"""
        auto_unlock_location(location_id)
        play_location_music(location_id)

    def quick_unlock_character(character_id):
        """Быстрая разблокировка персонажа"""
        auto_unlock_character(character_id)


## Обработчик начала каждой сцены
label scene_start(scene_type="normal"):
    python:
        # Автосохранение в начале сцены
        if game_settings.auto_save:
            renpy.save("auto-1")

        # Установить музыку для типа сцены
        if scene_type in ["interrogation", "revelation", "tension"]:
            play_scene_music(scene_type)

    return


## Обработчик конца каждой сцены
label scene_end:
    python:
        # Проверить достижения
        check_achievements()

        # Сохранить статистику
        game_statistics.save_statistics()

    return


## Система подсказок для игрока
screen hint_system(hint_text):
    """Показать подсказку игроку"""
    if game_settings.show_hints:
        frame:
            xalign 0.5
            yalign 0.1
            padding (30, 20)
            background "#1a1a2acc"

            hbox:
                spacing 15

                text "💡" size 28

                text hint_text:
                    size 20
                    color "#ffcc00"
                    xsize 600

        timer 5.0 action Hide("hint_system")


## Показать подсказку
label show_hint(hint_text):
    if game_settings.show_hints:
        show screen hint_system(hint_text)
        pause 0.5 hard False

    return


## Интеграция с системой сложности
init python:
    def get_difficulty_multiplier():
        """Получить множитель сложности"""
        difficulty_map = {
            "easy": 1.5,
            "normal": 1.0,
            "hard": 0.75
        }
        return difficulty_map.get(game_settings.difficulty, 1.0)

    def get_interrogation_patience():
        """Получить терпение для допроса в зависимости от сложности"""
        base_patience = 100

        if game_settings.difficulty == "easy":
            return int(base_patience * 1.5)  # 150
        elif game_settings.difficulty == "hard":
            return int(base_patience * 0.75)  # 75
        else:
            return base_patience  # 100


## Система отслеживания времени игры
init python:
    import time

    class PlaytimeTracker:
        """Отслеживание времени игры"""

        def __init__(self):
            self.session_start = time.time()
            self.total_playtime = 0.0

        def start_session(self):
            """Начать сессию"""
            self.session_start = time.time()

        def end_session(self):
            """Закончить сессию и обновить общее время"""
            session_time = time.time() - self.session_start
            self.total_playtime += session_time
            game_statistics.total_playtime += session_time
            game_statistics.save_statistics()

    playtime_tracker = PlaytimeTracker()


## Автоматическое отслеживание времени
label before_game_starts:
    python:
        playtime_tracker.start_session()

    return


label before_game_ends:
    python:
        playtime_tracker.end_session()

    return


## Периодическое сохранение (каждые 10 минут)
init python:
    def periodic_autosave():
        """Периодическое автосохранение"""
        if game_settings.auto_save:
            renpy.save("auto-periodic")
            game_statistics.save_statistics()

        # Запланировать следующее сохранение через 10 минут
        renpy.timeout(600.0, periodic_autosave)

    # Запустить периодическое сохранение
    config.start_callbacks.append(lambda: renpy.timeout(600.0, periodic_autosave))


## Обработчик выхода из игры
init python:
    def on_quit():
        """Вызывается при выходе из игры"""
        # Сохранить время игры
        playtime_tracker.end_session()

        # Сохранить статистику и настройки
        game_statistics.save_statistics()
        game_settings.save_statistics()

        return True

    config.quit_callbacks.append(on_quit)


## Debug команды (только для разработки)
# Раскомментируйте для тестирования

# label debug_unlock_all:
#     python:
#         # Разблокировать все достижения
#         for ach_id in achievements_manager.achievements:
#             achievements_manager.unlock_achievement(ach_id, show_notification=False)
#
#         # Разблокировать всех персонажей
#         for char_id in game_state.characters:
#             character_gallery.unlock_character(char_id)
#
#         # Разблокировать все локации
#         for loc in game_state.world_map.locations:
#             character_gallery.unlock_location(loc.id)
#
#     return
