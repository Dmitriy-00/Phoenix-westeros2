# Этап 4: Полировка - Руководство

## Обзор

Этап 4 добавляет систему полировки и улучшения пользовательского опыта (UX). Включает настройки, звуковую систему, галерею персонажей, достижения и улучшенный интерфейс.

## Новые системы

### 1. Система настроек (`settings_system.rpy`)

**Возможности:**
- Настройки звука (общая громкость, музыка, SFX, голоса)
- Настройки текста (скорость, авто-режим, пропуск)
- Настройки интерфейса (подсказки, уведомления, полноэкранный режим)
- Настройки геймплея (сложность, автосохранение)

**Использование:**
```python
# Доступ к настройкам
game_settings.master_volume  # Общая громкость (0.0-1.0)
game_settings.text_speed  # Скорость текста (0-100)
game_settings.difficulty  # "easy", "normal", "hard"

# Применение настроек
game_settings.apply_volume_settings()
game_settings.save_settings()
game_settings.load_settings()
```

**Экраны:**
- `settings_menu` - главное меню настроек с вкладками
- Вкладки: Звук, Текст, Интерфейс, Геймплей

### 2. Звуковая система (`audio_system.rpy`)

**Треки (плейсхолдеры):**
- `audio.menu_theme` - музыка главного меню
- `audio.investigation_theme` - музыка расследования
- `audio.tension_theme` - напряжённая музыка (допросы)
- `audio.mystery_theme` - мистическая музыка
- `audio.revelation_theme` - музыка открытий
- Локации: `castle_ambient`, `city_ambient`, `church_ambient`, `port_ambient`, `tavern_ambient`

**Звуковые эффекты:**
- `audio.sfx_click` - клик по кнопке
- `audio.sfx_clue_found` - найдена улика
- `audio.sfx_objection` - возражение!
- `audio.sfx_breakthrough` - прорыв в деле
- `audio.sfx_failure` - провал

**Использование:**
```python
# Воспроизведение музыки
audio_manager.play_music(audio.investigation_theme, fadein=1.0)

# Музыка для локации
audio_manager.set_music_for_location("loc_port_city")

# Музыка для сцены
audio_manager.set_music_for_scene("interrogation")

# Звуковой эффект
audio_manager.play_sfx(audio.sfx_clue_found)

# Уведомление со звуком
notify_clue_found("Церковный кинжал")
```

**Замена плейсхолдеров:**
1. Создайте папки `game/audio/music/` и `game/audio/sfx/`
2. Поместите файлы (`.ogg` или `.mp3`)
3. Обновите определения в `audio_system.rpy`:
   ```renpy
   define audio.menu_theme = "audio/music/menu_theme.ogg"
   define audio.sfx_click = "audio/sfx/click.ogg"
   ```

### 3. Галерея персонажей (`character_gallery.rpy`)

**Возможности:**
- Просмотр информации о встреченных персонажах
- Кодекс фракций с репутацией
- Кодекс локаций
- Статистика игры
- Автоматическая разблокировка при встрече

**Экраны:**
- `codex_main_menu` - главное меню кодекса
- `character_gallery_screen` - галерея персонажей
- `faction_codex_screen` - кодекс фракций
- `location_codex_screen` - кодекс локаций
- `statistics_screen` - статистика игрока

**Использование:**
```python
# Разблокировать персонажа
character_gallery.unlock_character("char_lord_north")

# Разблокировать локацию
character_gallery.unlock_location("loc_port_city")

# Проверить, разблокирован ли
if character_gallery.is_character_unlocked("char_lord_north"):
    # ...
```

### 4. Система достижений (`achievements_system.rpy`)

**Типы достижений:**
- **Сюжетные**: Завершение дел, получение концовок
- **Улики**: Сбор доказательств
- **Допросы**: Проведение допросов
- **Отношения**: Дружба и вражда
- **Исследование**: Локации, персонажи, кодекс
- **Специальные**: Скоростное прохождение, перфекционизм
- **Секретные**: Скрытые достижения

**Примеры достижений:**
- `first_case` - "Первое дело"
- `perfect_interrogation` - "Безупречный допрос"
- `first_friend` - "Первый друг" (+50 отношений)
- `church_enemy` - "Враг Церкви" (скрытое)
- `completionist` - "Перфекционист" (100% завершение)

**Использование:**
```python
# Разблокировать достижение
achievements_manager.unlock_achievement("first_case")

# Короткая форма
unlock_ach("perfect_interrogation")

# Проверить условия всех достижений
achievements_manager.check_achievement_conditions(game_state)

# Проверить, получено ли
if achievements_manager.is_unlocked("first_case"):
    # ...
```

**Уведомления:**
При разблокировке автоматически показывается красивое уведомление с анимацией и звуком.

### 5. Статистика игры

**Отслеживаемые параметры:**
- Время игры (total_playtime)
- Завершённые/провалённые дела
- Количество выборов
- Найденные улики
- Проведённые допросы
- Идеальные допросы (без ошибок)
- Встреченные персонажи
- Посещённые локации
- Увиденные концовки

**Использование:**
```python
# Записать событие
game_statistics.record_choice()
game_statistics.record_evidence("clue_id")
game_statistics.record_interrogation(perfect=True)
game_statistics.record_ending("ending_true_justice")

# Получить процент завершения
completion = game_statistics.get_completion_percentage()  # 0-100

# Сохранить/загрузить
game_statistics.save_statistics()
game_statistics.load_statistics()
```

### 6. Улучшенный UI (`improved_ui.rpy`)

**Новое главное меню:**
- Красивый дизайн с фоном
- Быстрый доступ к кодексу
- Кнопка помощи
- Информация о игре

**Система помощи:**
- Вкладки: Основы, Расследование, Допросы, Отношения, Интерфейс
- Подробные инструкции для новичков
- Быстрая справка (клавиша H)

**Экраны:**
- `main_menu` - главное меню
- `help_menu` - полная справка
- `about_menu` - информация об игре
- `quick_help` - быстрая справка (H)

**Горячие клавиши:**
- H - быстрая справка
- S - быстрое сохранение
- L - быстрая загрузка
- F - полноэкранный режим
- ESC - меню

## Интеграция с игрой

### Инициализация при старте

Добавьте в начало игры (script.rpy):

```renpy
label start:
    # Загрузка настроек и статистики
    call init_settings

    # Ваша игра...
    # ...
```

### Автоматическая разблокировка

При встрече персонажа:
```python
auto_unlock_character("char_lord_north")
```

При посещении локации:
```python
auto_unlock_location("loc_port_city")
play_location_music("loc_port_city")
```

При смене типа сцены:
```python
play_scene_music("interrogation")
```

### Проверка достижений

В конце важных сцен:
```python
check_achievements()
```

### Уведомления

Улика найдена:
```python
notify_clue_found("Церковный кинжал")
```

Отношения изменились:
```python
notify_relationship_change("Лорд Стормхолд", +10)
```

## Настройка и кастомизация

### Добавление новых достижений

В `achievements_system.rpy`, метод `init_achievements()`:

```python
self.add_achievement(
    "achievement_id",
    "Название достижения",
    "Описание достижения",
    icon=None,
    hidden=False  # True для скрытых
)
```

### Добавление звуковых файлов

1. Создайте папки:
   ```
   game/audio/music/
   game/audio/sfx/
   ```

2. Положите файлы (рекомендуется .ogg)

3. Обновите `audio_system.rpy`:
   ```renpy
   define audio.investigation_theme = "audio/music/investigation.ogg"
   define audio.sfx_clue_found = "audio/sfx/clue_found.ogg"
   ```

### Настройка уровней сложности

В `settings_system.rpy` можно использовать `game_settings.difficulty`:

```python
if game_settings.difficulty == "easy":
    interrogation_patience = 150  # Больше терпения
elif game_settings.difficulty == "normal":
    interrogation_patience = 100
else:  # hard
    interrogation_patience = 75   # Меньше терпения
```

## Лучшие практики

### 1. Звук
- Используйте фоновую музыку для атмосферы
- Меняйте музыку при смене настроения сцены
- Добавляйте звуковые эффекты для важных моментов
- Не злоупотребляйте звуками - они должны дополнять, а не отвлекать

### 2. Достижения
- Давайте достижения за значимые события
- Балансируйте лёгкие и сложные достижения
- Используйте скрытые достижения для спойлерных моментов
- Проверяйте условия достижений регулярно

### 3. Галерея
- Разблокируйте персонажей автоматически при первой встрече
- Обновляйте информацию при изменении отношений
- Используйте галерею для энциклопедии мира

### 4. Настройки
- Применяйте настройки сразу при изменении
- Сохраняйте настройки автоматически
- Предоставьте разумные значения по умолчанию

### 5. Уведомления
- Уведомления должны быть краткими
- Используйте цвета для различных типов (улики - золотой, отношения - зелёный/красный)
- Не показывайте слишком много уведомлений одновременно

## Отладка

### Тестирование звука
```python
# В консоли Ren'Py
renpy.music.play(audio.investigation_theme, channel="music")
renpy.music.play(audio.sfx_clue_found, channel="sound")
```

### Разблокировка всех достижений (для тестирования)
```python
for ach_id in achievements_manager.achievements:
    achievements_manager.unlock_achievement(ach_id, show_notification=False)
```

### Проверка статистики
```python
print("Персонажей встречено:", len(game_statistics.characters_met))
print("Локаций посещено:", len(game_statistics.locations_visited))
print("Процент завершения:", game_statistics.get_completion_percentage())
```

## Рекомендуемые ресурсы

### Бесплатная музыка
- **incompetech.com** - Kevin MacLeod (CC-BY)
- **opengameart.org** - музыка для игр
- **freepd.com** - Public Domain музыка
- **ccmixter.org** - Creative Commons ремиксы

### Звуковые эффекты
- **freesound.org** - огромная библиотека SFX
- **zapsplat.com** - бесплатные звуки
- **sonniss.com** - GDC звуковые пакеты

### Форматы
- **Музыка**: .ogg, 128-192 kbps, mono или stereo
- **SFX**: .ogg или .wav, 44.1kHz, короткие (<2 сек)

## Что дальше?

После Этапа 4 игра имеет полный набор функций:
- ✅ Базовый визуал
- ✅ Богатый контент (2 дела)
- ✅ Полная система настроек
- ✅ Звук и музыка (с плейсхолдерами)
- ✅ Галерея и кодекс
- ✅ Достижения
- ✅ Улучшенный UI

**Следующие шаги для финализации:**
1. Замените визуальные плейсхолдеры на реальную графику
2. Добавьте музыку и звуки
3. Создайте дополнительные дела
4. Проведите тестирование и балансировку
5. Добавьте озвучку (опционально)
6. Создайте финальную сборку для релиза

---

**Версия:** 0.3.0 Alpha
**Дата:** Этап 4 завершён
**Статус:** Полностью играбельная игра с системами полировки
