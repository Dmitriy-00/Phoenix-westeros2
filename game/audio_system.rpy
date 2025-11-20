# -*- coding: utf-8 -*-
"""
Audio System - Sound Effects and Music
Система звука и музыки с плейсхолдерами
"""

## МУЗЫКАЛЬНЫЕ ТРЕКИ (плейсхолдеры - заменить на реальные файлы)
## Для замены: положите .mp3 или .ogg файлы в папку game/audio/music/

# Главное меню
define audio.menu_theme = "<silence 1.0>"  # Placeholder

# Тема расследования
define audio.investigation_theme = "<silence 1.0>"  # Placeholder

# Напряжённая музыка (допросы, конфронтации)
define audio.tension_theme = "<silence 1.0>"  # Placeholder

# Мистическая/зловещая музыка
define audio.mystery_theme = "<silence 1.0>"  # Placeholder

# Драматическая музыка (важные открытия)
define audio.revelation_theme = "<silence 1.0>"  # Placeholder

# Грустная музыка
define audio.sad_theme = "<silence 1.0>"  # Placeholder

# Победная музыка
define audio.victory_theme = "<silence 1.0>"  # Placeholder

# Музыка для локаций
define audio.castle_ambient = "<silence 1.0>"  # Placeholder
define audio.city_ambient = "<silence 1.0>"  # Placeholder
define audio.church_ambient = "<silence 1.0>"  # Placeholder
define audio.port_ambient = "<silence 1.0>"  # Placeholder
define audio.tavern_ambient = "<silence 1.0>"  # Placeholder


## ЗВУКОВЫЕ ЭФФЕКТЫ (плейсхолдеры)
## Для замены: положите .wav или .ogg файлы в папку game/audio/sfx/

# UI звуки
define audio.sfx_click = "<silence 0.1>"  # Клик по кнопке
define audio.sfx_select = "<silence 0.1>"  # Выбор опции
define audio.sfx_cancel = "<silence 0.1>"  # Отмена
define audio.sfx_page_turn = "<silence 0.3>"  # Перелистывание страницы

# Игровые звуки
define audio.sfx_clue_found = "<silence 0.5>"  # Найдена улика
define audio.sfx_objection = "<silence 0.8>"  # Возражение!
define audio.sfx_breakthrough = "<silence 1.0>"  # Прорыв в деле
define audio.sfx_revelation = "<silence 1.0>"  # Откровение
define audio.sfx_failure = "<silence 0.5>"  # Провал

# Звуки локаций
define audio.sfx_door_open = "<silence 0.5>"  # Открытие двери
define audio.sfx_door_close = "<silence 0.5>"  # Закрытие двери
define audio.sfx_footsteps = "<silence 1.0>"  # Шаги
define audio.sfx_crowd_murmur = "<silence 2.0>"  # Шум толпы

# Атмосферные звуки
define audio.sfx_wind = "<silence 2.0>"  # Ветер
define audio.sfx_rain = "<silence 2.0>"  # Дождь
define audio.sfx_fire = "<silence 2.0>"  # Огонь
define audio.sfx_waves = "<silence 2.0>"  # Волны (для порта)
define audio.sfx_bells = "<silence 1.0>"  # Колокола (для церкви)


init python:
    class AudioManager:
        """Управление музыкой и звуками"""

        def __init__(self):
            self.current_music = None
            self.current_ambient = None
            self.music_volume = 0.7
            self.sfx_volume = 0.8

        def play_music(self, track, fadein=1.0, fadeout=1.0, loop=True):
            """Воспроизвести музыку"""
            if self.current_music != track:
                if loop:
                    renpy.music.play(track, channel="music", fadein=fadein, fadeout=fadeout, loop=True)
                else:
                    renpy.music.play(track, channel="music", fadein=fadein, fadeout=fadeout, loop=False)
                self.current_music = track

        def stop_music(self, fadeout=1.0):
            """Остановить музыку"""
            renpy.music.stop(channel="music", fadeout=fadeout)
            self.current_music = None

        def play_ambient(self, track, fadein=2.0, loop=True):
            """Воспроизвести фоновый звук"""
            if self.current_ambient != track:
                if loop:
                    renpy.music.play(track, channel="ambient", fadein=fadein, loop=True)
                else:
                    renpy.music.play(track, channel="ambient", fadein=fadein, loop=False)
                self.current_ambient = track

        def stop_ambient(self, fadeout=2.0):
            """Остановить фоновый звук"""
            renpy.music.stop(channel="ambient", fadeout=fadeout)
            self.current_ambient = None

        def play_sfx(self, sound, delay=0.0):
            """Воспроизвести звуковой эффект"""
            if delay > 0:
                renpy.music.play(sound, channel="sound", delay=delay)
            else:
                renpy.music.play(sound, channel="sound")

        def set_music_for_location(self, location_id):
            """Установить музыку для локации"""
            location_music = {
                "loc_stormhold_keep": audio.castle_ambient,
                "loc_capital_city": audio.city_ambient,
                "loc_light_cathedral": audio.church_ambient,
                "loc_port_city": audio.port_ambient,
                "loc_salty_mermaid": audio.tavern_ambient,
                "loc_grand_library": audio.mystery_theme
            }

            music = location_music.get(location_id, None)
            if music:
                self.play_ambient(music)

        def set_music_for_scene(self, scene_type):
            """Установить музыку для типа сцены"""
            scene_music = {
                "investigation": audio.investigation_theme,
                "interrogation": audio.tension_theme,
                "revelation": audio.revelation_theme,
                "confrontation": audio.tension_theme,
                "sad": audio.sad_theme,
                "victory": audio.victory_theme,
                "mystery": audio.mystery_theme
            }

            music = scene_music.get(scene_type, None)
            if music:
                self.play_music(music)

    # Глобальный менеджер аудио
    audio_manager = AudioManager()


## Макросы для удобного использования

# Воспроизвести звук находки улики
define play_clue_found = Play("sound", audio.sfx_clue_found)

# Воспроизвести звук возражения
define play_objection = Play("sound", audio.sfx_objection)

# Воспроизвести звук прорыва
define play_breakthrough = Play("sound", audio.sfx_breakthrough)

# Воспроизвести звук провала
define play_failure = Play("sound", audio.sfx_failure)


## Аудио каналы
init python:
    # Канал для музыки
    renpy.music.register_channel("music", mixer="music", loop=True, stop_on_mute=True, tight=True, buffer_queue=True)

    # Канал для фоновых звуков
    renpy.music.register_channel("ambient", mixer="music", loop=True, stop_on_mute=True, tight=True)

    # Канал для звуковых эффектов
    renpy.music.register_channel("sound", mixer="sfx", loop=False, stop_on_mute=True)

    # Канал для голосов
    renpy.music.register_channel("voice", mixer="voice", loop=False, stop_on_mute=True)


## Уведомление с звуком
screen notification_with_sound(message, sound=None):
    zorder 100

    frame:
        xalign 0.5
        yalign 0.1
        padding (30, 20)
        background "#000000cc"

        text message:
            size 28
            color "#ffcc00"
            outlines [(2, "#000000", 0, 0)]

    if sound:
        on "show" action Play("sound", sound)

    timer 3.0 action Hide("notification_with_sound")


## Функции для вызова из скриптов

init python:
    def notify_clue_found(clue_name):
        """Показать уведомление о найденной улике со звуком"""
        if game_settings.show_clue_notifications:
            renpy.show_screen("notification_with_sound",
                            message="УЛИКА НАЙДЕНА: {}".format(clue_name),
                            sound=audio.sfx_clue_found)
            renpy.pause(3.0, hard=False)
            renpy.hide_screen("notification_with_sound")

    def notify_relationship_change(character_name, amount):
        """Показать уведомление об изменении отношений"""
        if game_settings.show_relationship_changes:
            if amount > 0:
                message = "{} +{}".format(character_name, amount)
                color = "#00ff00"
            else:
                message = "{} {}".format(character_name, amount)
                color = "#ff0000"

            renpy.show_screen("simple_notification", message=message, color=color)
            renpy.pause(2.0, hard=False)
            renpy.hide_screen("simple_notification")

    def play_location_music(location_id):
        """Воспроизвести музыку для локации"""
        audio_manager.set_music_for_location(location_id)

    def play_scene_music(scene_type):
        """Воспроизвести музыку для сцены"""
        audio_manager.set_music_for_scene(scene_type)


## Простое уведомление
screen simple_notification(message, color="#ffffff"):
    zorder 100

    frame:
        xalign 0.9
        yalign 0.1
        padding (20, 10)
        background "#000000aa"

        text message:
            size 24
            color color
            outlines [(1, "#000000", 0, 0)]

    timer 2.0 action Hide("simple_notification")


## ИНСТРУКЦИИ ПО ЗАМЕНЕ ПЛЕЙСХОЛДЕРОВ
##
## Чтобы добавить реальные аудиофайлы:
##
## 1. Создайте папки:
##    - game/audio/music/ (для музыки)
##    - game/audio/sfx/ (для звуковых эффектов)
##
## 2. Поместите аудиофайлы в соответствующие папки:
##    - Форматы: .mp3, .ogg, .opus (рекомендуется .ogg для лучшей совместимости)
##    - Музыка: обычно 128-192 kbps, ~3-5 минут с зацикливанием
##    - SFX: обычно 44.1kHz, короткие (<2 сек)
##
## 3. Обновите определения выше, например:
##    define audio.menu_theme = "audio/music/menu_theme.ogg"
##    define audio.sfx_click = "audio/sfx/click.ogg"
##
## 4. Тестируйте звуки в игре!
##
## Рекомендуемые источники бесплатной музыки:
## - freesound.org (звуковые эффекты)
## - incompetech.com (музыка Kevin MacLeod, CC-BY)
## - opengameart.org (музыка и SFX для игр)
## - freepd.com (музыка public domain)
