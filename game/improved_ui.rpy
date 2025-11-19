# -*- coding: utf-8 -*-
"""
Improved UI - Enhanced Main Menu and Help System
Улучшенный интерфейс - главное меню и система помощи
"""

## Улучшенный главный экран меню
screen main_menu():
    tag menu

    # Фоновая музыка
    on "show" action Play("music", audio.menu_theme, fadein=1.0)

    # Фон
    add "gui/main_menu.png"

    # Главное меню
    frame:
        xalign 0.5
        yalign 0.6
        background None

        vbox:
            spacing 20
            xalign 0.5

            # Логотип/заголовок уже на фоне

            null height 50

            # Кнопки меню
            vbox:
                spacing 15
                xalign 0.5

                textbutton "НОВАЯ ИГРА" action Start() style "main_menu_button"
                textbutton "ПРОДОЛЖИТЬ" action ShowMenu("load") style "main_menu_button"
                textbutton "КОДЕКС" action ShowMenu("codex_main_menu") style "main_menu_button"
                textbutton "НАСТРОЙКИ" action ShowMenu("settings_menu") style "main_menu_button"
                textbutton "ПОМОЩЬ" action ShowMenu("help_menu") style "main_menu_button"
                textbutton "О ИГРЕ" action ShowMenu("about_menu") style "main_menu_button"
                textbutton "ВЫХОД" action Quit(confirm=True) style "main_menu_button"

    # Версия игры
    text "v0.3.0 Alpha":
        xalign 0.98
        yalign 0.98
        size 18
        color "#ffffff66"


## Стиль для кнопок главного меню
style main_menu_button:
    xsize 400
    ysize 60
    background "#000000aa"
    hover_background "#ffcc0033"
    padding (20, 15)

style main_menu_button_text:
    size 28
    color "#ffffff"
    hover_color "#ffcc00"
    xalign 0.5
    yalign 0.5
    outlines [(2, "#000000", 0, 0)]


## Экран помощи
screen help_menu():
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
            text "ПОМОЩЬ И РУКОВОДСТВО" size 48 xalign 0.5 color "#ffcc00"

            null height 10

            # Табы
            hbox:
                spacing 15
                xalign 0.5

                textbutton "Основы" action SetVariable("help_tab", "basics")
                textbutton "Расследование" action SetVariable("help_tab", "investigation")
                textbutton "Допросы" action SetVariable("help_tab", "interrogation")
                textbutton "Отношения" action SetVariable("help_tab", "relationships")
                textbutton "Интерфейс" action SetVariable("help_tab", "interface")

            null height 10

            # Содержимое
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 1350
                ysize 650

                vbox:
                    spacing 20

                    if help_tab == "basics":
                        use help_basics_tab
                    elif help_tab == "investigation":
                        use help_investigation_tab
                    elif help_tab == "interrogation":
                        use help_interrogation_tab
                    elif help_tab == "relationships":
                        use help_relationships_tab
                    elif help_tab == "interface":
                        use help_interface_tab

            # Кнопка возврата
            textbutton "Назад" action Return() xalign 0.5


## Вкладки помощи
screen help_basics_tab():
    vbox:
        spacing 30
        xsize 1300

        # Основы игры
        frame:
            padding (30, 20)
            background "#2a2a3a"

            vbox:
                spacing 15

                text "ОСНОВЫ ИГРЫ" size 32 color "#ffcc00"

                text """
'Тени над Королевством' - детективная визуальная новелла в стиле Phoenix Wright, действие которой происходит в оригинальном мире тёмного фэнтези.

Вы играете за детектива, расследующего преступления в мире политических интриг, религиозных конфликтов и древних тайн. Каждое ваше решение влияет на сюжет, отношения с персонажами и возможные концовки.
                """ size 18 color "#ffffff"

        # Геймплей
        frame:
            padding (30, 20)
            background "#2a2a3a"

            vbox:
                spacing 15

                text "ГЕЙМПЛЕЙ" size 28 color "#ffcc00"

                text """
• РАССЛЕДОВАНИЕ - исследуйте локации, собирайте улики, беседуйте с персонажами
• ДОПРОСЫ - используйте Phoenix Wright-подобную механику для разоблачения лжи
• ВЫБОРЫ - ваши решения влияют на отношения, репутацию и возможные концовки
• УЛИКИ - собирайте доказательства и используйте их в допросах
• ОТНОШЕНИЯ - развивайте отношения с персонажами и фракциями
                """ size 18 color "#ffffff"


screen help_investigation_tab():
    vbox:
        spacing 30
        xsize 1300

        # Расследование
        frame:
            padding (30, 20)
            background "#2a2a3a"

            vbox:
                spacing 15

                text "РАССЛЕДОВАНИЕ" size 32 color "#ffcc00"

                text """
Во время расследования вы можете:

• ОСМАТРИВАТЬ ЛОКАЦИИ - найдите и изучите важные детали места преступления
• СОБИРАТЬ УЛИКИ - все найденные улики сохраняются в вашем блокноте
• РАЗГОВАРИВАТЬ С СВИДЕТЕЛЯМИ - получайте информацию от NPC
• ПЕРЕМЕЩАТЬСЯ ПО КАРТЕ - исследуйте различные локации города

Улики делятся на типы:
• ВЕЩЕСТВЕННЫЕ - физические объекты (оружие, документы)
• СВИДЕТЕЛЬСКИЕ - показания очевидцев
• КОСВЕННЫЕ - обстоятельственные доказательства

Каждая улика имеет уровень надёжности (1-5 звёзд).
                """ size 18 color "#ffffff"


screen help_interrogation_tab():
    vbox:
        spacing 30
        xsize 1300

        # Допросы
        frame:
            padding (30, 20)
            background "#2a2a3a"

            vbox:
                spacing 15

                text "СИСТЕМА ДОПРОСОВ" size 32 color "#ffcc00"

                text """
Допросы работают в стиле Phoenix Wright:

1. СЛУШАЙТЕ ПОКАЗАНИЯ - свидетель даёт серию утверждений
2. НАЖИМАЙТЕ (PRESS) - требуйте больше информации по утверждению
3. ПРЕДЪЯВЛЯЙТЕ УЛИКИ (PRESENT) - укажите на противоречие в показаниях

ТЕРПЕНИЕ:
У свидетеля есть шкала терпения (100 очков)
• PRESS снижает терпение на 10-20
• Неправильное предъявление улики снижает на 20-30
• При 0 терпения допрос провален!

УСПЕХ:
• Предъявите правильную улику к противоречивому утверждению
• Сломайте все ключевые утверждения
• Получите признание или важную информацию

НАГРАДЫ:
• Идеальный допрос (без ошибок) даёт бонусы к репутации
• Признание открывает новые улики и пути расследования
                """ size 18 color "#ffffff"


screen help_relationships_tab():
    vbox:
        spacing 30
        xsize 1300

        # Отношения
        frame:
            padding (30, 20)
            background "#2a2a3a"

            vbox:
                spacing 15

                text "СИСТЕМА ОТНОШЕНИЙ" size 32 color "#ffcc00"

                text """
Отношения с персонажами и фракциями влияют на:
• Доступность информации
• Помощь и препятствия в расследовании
• Возможные концовки

ШКАЛА ОТНОШЕНИЙ: -100 до +100

• +75 до +100: ПРЕДАННЫЙ СОЮЗНИК
• +50 до +74: ДОВЕРИЕ
• +25 до +49: ДРУЖЕЛЮБИЕ
• -24 до +24: НЕЙТРАЛЬНОСТЬ
• -25 до -49: НЕДОВЕРИЕ
• -50 до -74: ВРАЖДА
• -75 до -100: ЗАКЛЯТЫЙ ВРАГ

ИЗМЕНЕНИЕ ОТНОШЕНИЙ:
• Выборы в диалогах
• Успехи и провалы в допросах
• Обвинения и защита персонажей
• Раскрытие или сокрытие информации

РЕПУТАЦИЯ ФРАКЦИЙ:
Работает аналогично личным отношениям, но влияет на всю организацию. Высокая репутация с фракцией открывает новые возможности.
                """ size 18 color "#ffffff"


screen help_interface_tab():
    vbox:
        spacing 30
        xsize 1300

        # Интерфейс
        frame:
            padding (30, 20)
            background "#2a2a3a"

            vbox:
                spacing 15

                text "ИНТЕРФЕЙС" size 32 color "#ffcc00"

                text """
ОСНОВНЫЕ ЭКРАНЫ:

• БЛОКНОТ (N) - просмотр собранных улик
• КАРТА (M) - перемещение между локациями
• ПЕРСОНАЖИ (C) - информация о встреченных NPC
• СОХРАНЕНИЕ (S) - сохранить прогресс
• НАСТРОЙКИ (ESC) - параметры игры

БЫСТРЫЕ ДЕЙСТВИЯ:

• ПКМ - открыть меню
• Колёсико мыши - история текста
• CTRL - пропуск текста
• SPACE - скрыть/показать интерфейс

ИНДИКАТОРЫ:

• Зелёный текст - улучшение отношений
• Красный текст - ухудшение отношений
• Золотой блеск - найдена улика
• Восклицательный знак - важный выбор
                """ size 18 color "#ffffff"


## Экран "О игре"
screen about_menu():
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
            xalign 0.5

            text "О ИГРЕ" size 48 xalign 0.5 color "#ffcc00"

            null height 20

            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 950
                ysize 500

                vbox:
                    spacing 25

                    # Информация об игре
                    frame:
                        padding (30, 20)
                        background "#2a2a3a"
                        xsize 900

                        vbox:
                            spacing 15

                            text "ТЕНИ НАД КОРОЛЕВСТВОМ" size 28 color "#ffcc00" xalign 0.5
                            text "Shadows Over the Kingdom" size 20 color "#cccccc" italic True xalign 0.5

                            null height 10

                            text """
Детективная визуальная новелла в жанре тёмного фэнтези, вдохновлённая серией Phoenix Wright: Ace Attorney.

Расследуйте преступления в мире политических интриг, религиозных конфликтов и древних тайн. Собирайте улики, допрашивайте свидетелей, разоблачайте ложь и раскрывайте заговоры.
                            """ size 18 color "#ffffff"

                    # Кредиты
                    frame:
                        padding (30, 20)
                        background "#2a2a3a"
                        xsize 900

                        vbox:
                            spacing 10

                            text "РАЗРАБОТКА" size 24 color "#ffcc00"

                            text "Дизайн и сценарий: [Ваше имя]" size 18
                            text "Программирование: Ren'Py Engine" size 18
                            text "Вдохновение: Phoenix Wright: Ace Attorney" size 18

                    # Технология
                    frame:
                        padding (30, 20)
                        background "#2a2a3a"
                        xsize 900

                        vbox:
                            spacing 10

                            text "ТЕХНОЛОГИИ" size 24 color "#ffcc00"

                            text "Движок: Ren'Py [renpy.version()]" size 18
                            text "Язык: Python" size 18
                            text "Формат данных: JSON" size 18

                    # Благодарности
                    frame:
                        padding (30, 20)
                        background "#2a2a3a"
                        xsize 900

                        vbox:
                            spacing 10

                            text "ОСОБАЯ БЛАГОДАРНОСТЬ" size 24 color "#ffcc00"

                            text "• Capcom за создание Phoenix Wright: Ace Attorney" size 18
                            text "• Сообществу Ren'Py за отличный движок" size 18
                            text "• Всем игрокам и тестерам" size 18

            textbutton "Назад" action Return() xalign 0.5


## Быстрая справка (можно вызвать в любой момент)
screen quick_help():
    zorder 100
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#000000ee"

        vbox:
            spacing 20

            text "БЫСТРАЯ СПРАВКА" size 36 xalign 0.5 color "#ffcc00"

            null height 10

            vbox:
                spacing 15
                xsize 750

                text "УПРАВЛЕНИЕ:" size 24 color "#ffcc00"
                text "• ЛКМ / ENTER - продолжить диалог" size 18
                text "• ПКМ / ESC - открыть меню" size 18
                text "• CTRL - пропуск текста" size 18
                text "• SPACE - скрыть интерфейс" size 18

                null height 10

                text "ГОРЯЧИЕ КЛАВИШИ:" size 24 color "#ffcc00"
                text "• H - эта справка" size 18
                text "• S - быстрое сохранение" size 18
                text "• L - быстрая загрузка" size 18
                text "• F - полноэкранный режим" size 18

            textbutton "Закрыть" action Hide("quick_help") xalign 0.5


## Переменная для вкладки помощи
default help_tab = "basics"


## Клавиатурные сочетания
screen keyboard_help():
    key "h" action Show("quick_help")
    key "H" action Show("quick_help")
