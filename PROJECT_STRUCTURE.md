# Структура проекта "Тени над Королевством"

## Основные файлы игры

### game/main.rpy
Главный файл игры, точка входа. Содержит:
- Инициализацию игровых систем
- Основной игровой цикл
- Обработку расследований
- Диалоги и допросы

### game/screens.rpy  
Все UI экраны:
- Главное меню
- Выбор дела
- Журнал улик
- Карта мира
- Реестры (персонажи, фракции, локации)
- Экран допроса (Phoenix Wright style)

### game/options.rpy
Конфигурация Ren'Py

### game/gui.rpy
Настройки GUI (шрифты, цвета, размеры)

## Основные системы (game/core/)

### models.rpy
Классы данных:
- GameEntity (базовый класс)
- Character (персонажи)
- Faction (фракции)
- Location (локации)
- Clue (улики)
- DialogueNode (узлы диалога)
- InterrogationScene (допросы)
- Case (дела/расследования)
- WorldMap (карта мира)
- GameState (главное состояние игры)

### data_loader.rpy
Загрузка и сохранение JSON данных

### systems_dialogue.rpy
DialogueManager - управление диалогами:
- Ветвление
- Условия
- Эффекты

### systems_relationships.rpy
RelationshipManager - отношения и репутация:
- С персонажами
- С фракциями

### systems_evidence.rpy
EvidenceManager - управление уликами:
- Обнаружение
- Организация
- Предъявление в допросах

### systems_map.rpy
MapManager - карта мира:
- Перемещение между локациями
- Разблокировка локаций

### systems_cases.rpy
CaseManager - управление делами:
- Запуск расследований
- Стадии
- Концовки

## Редакторы (game/editors/)

### editor_main.rpy
Инструменты для разработчиков:
- Редактор персонажей
- Редактор фракций
- Редактор локаций
- Редактор улик
- Редактор дел

## Данные (game/data/)

### characters.json
5 персонажей с описаниями, фракциями, отношениями

### factions.json
6 фракций с отношениями между собой

### locations.json
8 локаций с описаниями и координатами на карте

### clues.json
7 улик для тестового дела

### cases.json
2 дела (1 полное, 1 заготовка)

### world_map.json
Карта мира с регионами

### case_north_murder_01_dialogues.json
Дерево диалогов для первого дела

### case_north_murder_01_interrogation.json
Допрос мейстера для первого дела

## Структура директорий

```
Phoenix-westeros2/
├── README.md                   # Основная документация
├── PROJECT_STRUCTURE.md        # Этот файл
├── game/
│   ├── main.rpy
│   ├── screens.rpy
│   ├── options.rpy
│   ├── gui.rpy
│   ├── core/
│   │   ├── models.rpy
│   │   ├── data_loader.rpy
│   │   ├── systems_dialogue.rpy
│   │   ├── systems_relationships.rpy
│   │   ├── systems_evidence.rpy
│   │   ├── systems_map.rpy
│   │   └── systems_cases.rpy
│   ├── editors/
│   │   └── editor_main.rpy
│   ├── data/
│   │   ├── characters.json
│   │   ├── factions.json
│   │   ├── locations.json
│   │   ├── clues.json
│   │   ├── cases.json
│   │   ├── world_map.json
│   │   ├── case_north_murder_01_dialogues.json
│   │   └── case_north_murder_01_interrogation.json
│   ├── images/
│   │   ├── characters/
│   │   ├── backgrounds/
│   │   └── ui/
│   └── audio/
│       ├── music/
│       └── sfx/
```

## Статистика

- **Файлов кода**: 12 .rpy файлов
- **Файлов данных**: 9 JSON файлов
- **Персонажей**: 5
- **Фракций**: 6
- **Локаций**: 8
- **Улик**: 7
- **Дел**: 2 (1 полное)
- **Строк кода**: ~2500+

## Основные механики

1. **Система диалогов** - JSON-управляемые диалоги с ветвлением
2. **Система допросов** - Phoenix Wright style с предъявлением улик
3. **Система отношений** - Отслеживание отношений и репутации
4. **Система улик** - Сбор и анализ доказательств
5. **Карта мира** - Перемещение между локациями
6. **Система дел** - Расследования с множественными концовками

## Расширение

Для добавления нового контента:
1. Создайте JSON-данные в `game/data/`
2. Система автоматически загрузит их при запуске
3. Используйте редактор (dev mode) для просмотра

Для новых механик:
1. Добавьте в `game/core/`
2. Интегрируйте с GameState
3. Добавьте UI в `game/screens.rpy`
