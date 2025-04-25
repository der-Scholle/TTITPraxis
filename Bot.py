from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest
import asyncio

# Глобальные словари с данными
COUNTRIES_INFO = {
    'germany': {
        'text': "🇩🇪 Нацистская Германия (1933-1945)\n\n"
                "• Официальное название: Третий рейх\n"
                "• Лидер: Адольф Гитлер (фюрер и рейхсканцлер)\n"
                "• Вступила в войну: 1 сентября 1939 (нападение на Польшу)\n"
                "• Капитуляция: 8 мая 1945 (Акт о безоговорочной капитуляции)\n\n"
                "Основные характеристики:\n"
                "- Агрессивная экспансионистская политика\n"
                "- Геноцид евреев и других народов (Холокост)\n"
                "- Развитая военная промышленность\n"
                "- Использование тактики блицкрига",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Bundesarchiv_Bild_183-R24231%2C_Flagge_NSDAP_auf_Kreuzer_%22Deutschland%22.jpg/800px-Bundesarchiv_Bild_183-R24231%2C_Flagge_NSDAP_auf_Kreuzer_%22Deutschland%22.jpg"
    },
    'italy': {
        'text': "🇮🇹 Королевство Италия (1922-1946)\n\n"
                "• Лидер: Бенито Муссолини (дуче)\n"
                "• Вступила в войну: 10 июня 1940\n"
                "• Капитуляция: 8 сентября 1943\n\n"
                "Основные характеристики:\n"
                "- Союзник Германии по Оси\n"
                "- Участвовала в войне в Северной Африке и на Балканах\n"
                "- В 1943 году произошел государственный переворот, Муссолини был арестован\n"
                "- После капитуляции север Италии оккупирован Германией",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Flag_of_Italy_%281861-1946%29_crowned.svg/800px-Flag_of_Italy_%281861-1946%29_crowned.svg.png"
    },
    'japan': {
        'text': "🇯🇵 Японская империя (1868-1945)\n\n"
                "• Лидер: Император Хирохито\n"
                "• Вступила в войну: 7 декабря 1941 (нападение на Пёрл-Харбор)\n"
                "• Капитуляция: 2 сентября 1945\n\n"
                "Основные характеристики:\n"
                "- Агрессивная экспансия в Азии и Тихом океане\n"
                "- Жестокое обращение с военнопленными\n"
                "- Камикадзе - летчики-смертники\n"
                "- Единственная страна, против которой было применено ядерное оружие",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Flag_of_Japan_%281870-1999%29.svg/800px-Flag_of_Japan_%281870-1999%29.svg.png"
    },
    'uk': {
        'text': "🇬🇧 Великобритания (1939-1945)\n\n"
                "• Лидер: Уинстон Черчилль (премьер-министр)\n"
                "• Вступила в войну: 3 сентября 1939\n"
                "• Победа: 8 мая 1945\n\n"
                "Основные характеристики:\n"
                "- Возглавила сопротивление нацизму в Европе\n"
                "- Выстояла в Битве за Британию (1940)\n"
                "- Организовала поставки по ленд-лизу в СССР\n"
                "- Участвовала в высадке в Нормандии (1944)",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Flag_of_the_United_Kingdom.svg/800px-Flag_of_the_United_Kingdom.svg.png"
    },
    'usa': {
        'text': "🇺🇸 США (1941-1945)\n\n"
                "• Лидер: Франклин Рузвельт (президент)\n"
                "• Вступила в войну: 7 декабря 1941 (после Пёрл-Харбора)\n"
                "• Победа: 2 сентября 1945\n\n"
                "Основные характеристики:\n"
                "- Мощная промышленная база\n"
                "- Программа ленд-лиза для союзников\n"
                "- Ядерные бомбардировки Хиросимы и Нагасаки\n"
                "- Главный организатор послевоенного мира",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/800px-Flag_of_the_United_States.svg.png"
    },
    'ussr': {
        'text': "🇷🇺 СССР (1941-1945)\n\n"
                "• Лидер: Иосиф Сталин (генеральный секретарь)\n"
                "• Вступила в войну: 22 июня 1941 (нападение Германии)\n"
                "• Победа: 9 мая 1945\n\n"
                "Основные характеристики:\n"
                "- Основной фронт войны в Европе\n"
                "- Решающие битвы: Москва, Сталинград, Курск\n"
                "- Огромные человеческие потери (около 27 млн)\n"
                "- Взятие Берлина в 1945 году",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Flag_of_the_Soviet_Union.svg/800px-Flag_of_the_Soviet_Union.svg.png"
    }
}

LEADERS_INFO = {
    'germany': {
        'text': "Адольф Гитлер (1889-1945)\n\n"
                "• Полное имя: Адольф Гитлер\n"
                "• Должность: Фюрер и рейхсканцлер Германии\n"
                "• Годы правления: 1933-1945\n\n"
                "Основные факты:\n"
                "- Инициатор Второй мировой войны\n"
                "- Автор расовой теории и идеи Lebensraum\n"
                "- Организатор Холокоста\n"
                "- Покончил жизнь самоубийством 30 апреля 1945 года",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Hitler_portrait_crop.jpg/800px-Hitler_portrait_crop.jpg"
    },
    'italy': {
        'text': "Бенито Муссолини (1883-1945)\n\n"
                "• Полное имя: Бенито Амилькаре Андреа Муссолини\n"
                "• Должность: Премьер-министр Италии\n"
                "• Годы правления: 1922-1943\n\n"
                "Основные факты:\n"
                "- Основатель итальянского фашизма\n"
                "- Союзник Гитлера по Оси\n"
                "- Свергнут в 1943 году, затем возглавил марионеточное государство\n"
                "- Казнен партизанами 28 апреля 1945 года",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Benito_Mussolini_in_1930.jpg/800px-Benito_Mussolini_in_1930.jpg"
    },
    'japan': {
        'text': "Император Хирохито (1901-1989)\n\n"
                "• Полное имя: Хирохито (император Сёва)\n"
                "• Должность: Император Японии\n"
                "• Годы правления: 1926-1989\n\n"
                "Основные факты:\n"
                "- Символический глава государства во время войны\n"
                "- Подписал капитуляцию Японии 2 сентября 1945\n"
                "- После войны остался на троне как конституционный монарх\n"
                "- Период его правления - самый длинный в истории Японии",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Emperor_Showa_1926.jpg/800px-Emperor_Showa_1926.jpg"
    },
    'ussr': {
        'text': "Иосиф Сталин (1878-1953)\n\n"
                "• Полное имя: Иосиф Виссарионович Сталин\n"
                "• Должность: Генеральный секретарь ЦК ВКП(б)\n"
                "• Годы правления: 1922-1953\n\n"
                "Основные факты:\n"
                "- Верховный главнокомандующий в годы войны\n"
                "- Организатор обороны Москвы и Сталинграда\n"
                "- Участник Тегеранской и Ялтинской конференций\n"
                "- Установил просоветские режимы в Восточной Европе",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/JStalin_Secretary_general_CCCP_1942_flipped.jpg/800px-JStalin_Secretary_general_CCCP_1942_flipped.jpg"
    },
    'usa': {
        'text': "Франклин Рузвельт (1882-1945)\n\n"
                "• Полное имя: Франклин Делано Рузвельт\n"
                "• Должность: 32-й президент США\n"
                "• Годы правления: 1933-1945\n\n"
                "Основные факты:\n"
                "- Единственный президент США, избиравшийся более двух сроков\n"
                "- Автор программы ленд-лиза для СССР\n"
                "- Один из создателей ООН\n"
                "- Умер 12 апреля 1945 года, не дожив до Победы",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/FDR_1944_Color_Portrait.jpg/800px-FDR_1944_Color_Portrait.jpg"
    },
    'uk': {
        'text': "Уинстон Черчилль (1874-1965)\n\n"
                "• Полное имя: Уинстон Леонард Спенсер-Черчилль\n"
                "• Должность: Премьер-министр Великобритании\n"
                "• Годы правления: 1940-1945, 1951-1955\n\n"
                "Основные факты:\n"
                "- Возглавил страну в самые тяжелые моменты войны\n"
                "- Автор термина «железный занавес»\n"
                "- Участник Тегеранской и Ялтинской конференций\n"
                "- Лауреат Нобелевской премии по литературе (1953)",
        'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Sir_Winston_Churchill_-_19086236948.jpg/800px-Sir_Winston_Churchill_-_19086236948.jpg"
    }
}

COMMANDERS_INFO = {
    'germany': [
        {
            'text': "Эрвин Роммель (1891-1944)\n\n"
                    "• Прозвище: «Лис пустыни»\n"
                    "• Звание: Генерал-фельдмаршал\n"
                    "• Основные операции:\n"
                    "  - Североафриканская кампания (1941-1943)\n"
                    "  - Оборона Атлантического вала (1944)\n\n"
                    "Особенности:\n"
                    "- Мастер манёвренных действий\n"
                    "- Разработал тактику танковых атак\n"
                    "- Участвовал в заговоре против Гитлера",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Bundesarchiv_Bild_146-1971-033-31%2C_Erwin_Rommel.jpg/800px-Bundesarchiv_Bild_146-1971-033-31%2C_Erwin_Rommel.jpg"
        },
        {
            'text': "Гейнц Гудериан (1888-1954)\n\n"
                    "• Прозвище: «Быстрый Гейнц»\n"
                    "• Звание: Генерал-полковник\n"
                    "• Основные операции:\n"
                    "  - Польская кампания (1939)\n"
                    "  - Французская кампания (1940)\n"
                    "  - Операция Барбаросса (1941)\n\n"
                    "Особенности:\n"
                    "- Отец немецких танковых войск\n"
                    "- Автор концепции блицкрига\n"
                    "- После войны консультировал западногерманскую армию",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bundesarchiv_Bild_101I-139-1112-17%2C_Heinz_Guderian.jpg/800px-Bundesarchiv_Bild_101I-139-1112-17%2C_Heinz_Guderian.jpg"
        }
    ],
    'italy': [
        {
            'text': "Родольфо Грациани (1882-1955)\n\n"
                    "• Прозвище: «Мясник Эфиопии»\n"
                    "• Звание: Маршал Италии\n"
                    "• Основные операции:\n"
                    "  - Вторжение в Египет (1940)\n"
                    "  - Военные действия в Северной Африке\n\n"
                    "Особенности:\n"
                    "- Жестокие методы ведения войны\n"
                    "- Потерпел поражение от британцев\n"
                    "- После войны осуждён, но вскоре освобождён",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Rodolfo_Graziani_1936.jpg/800px-Rodolfo_Graziani_1936.jpg"
        },
        {
            'text': "Джованни Мессе (1883-1968)\n\n"
                    "• Звание: Маршал Италии\n"
                    "• Основные операции:\n"
                    "  - Восточный фронт (1941-1943)\n"
                    "  - Оборона Италии (1943-1945)\n\n"
                    "Особенности:\n"
                    "- Командовал итальянским экспедиционным корпусом в СССР\n"
                    "- После капитуляции Италии перешёл на сторону союзников\n"
                    "- После войны занимал высокие государственные посты",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Giovanni_Messe_1942.jpg/800px-Giovanni_Messe_1942.jpg"
        }
    ],
    'japan': [
        {
            'text': "Исороку Ямамото (1884-1943)\n\n"
                    "• Звание: Адмирал\n"
                    "• Основные операции:\n"
                    "  - Нападение на Пёрл-Харбор (1941)\n"
                    "  - Битва за Мидуэй (1942)\n\n"
                    "Особенности:\n"
                    "- Главнокомандующий Объединённым флотом\n"
                    "- Противник войны с США\n"
                    "- Погиб в 1943 году (сбит американцами)",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Isoroku_Yamamoto.jpg/800px-Isoroku_Yamamoto.jpg"
        },
        {
            'text': "Томоюки Ямасита (1885-1946)\n\n"
                    "• Прозвище: «Тигр Малайи»\n"
                    "• Звание: Генерал\n"
                    "• Основные операции:\n"
                    "  - Захват Малайи и Сингапура (1941-1942)\n"
                    "  - Оборона Филиппин (1944-1945)\n\n"
                    "Особенности:\n"
                    "- Один из самых способных японских генералов\n"
                    "- Казнён по приговору трибунала в 1946 году\n"
                    "- Стал символом жестокости японской армии",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Yamashita_Tomoyuki.jpg/800px-Yamashita_Tomoyuki.jpg"
        }
    ],
    'ussr': [
        {
            'text': "Георгий Жуков (1896-1974)\n\n"
                    "• Звание: Маршал Советского Союза\n"
                    "• Основные операции:\n"
                    "  - Битва за Москву (1941)\n"
                    "  - Сталинградская битва (1942-1943)\n"
                    "  - Берлинская операция (1945)\n\n"
                    "Особенности:\n"
                    "- Четырежды Герой Советского Союза\n"
                    "- Принимал капитуляцию Германии\n"
                    "- После войны в опале у Сталина",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Georgy_Zhukov_1945.jpg/800px-Georgy_Zhukov_1945.jpg"
        },
        {
            'text': "Константин Рокоссовский (1896-1968)\n\n"
                    "• Звание: Маршал Советского Союза\n"
                    "• Основные операции:\n"
                    "  - Сталинградская битва\n"
                    "  - Курская битва\n"
                    "  - Операция «Багратион»\n\n"
                    "Особенности:\n"
                    "- Дважды Герой Советского Союза\n"
                    "- Командовал Парадом Победы 1945 года\n"
                    "- После войны министр обороны Польши",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Rokossovsky_portrait.jpg/800px-Rokossovsky_portrait.jpg"
        }
    ],
    'usa': [
        {
            'text': "Дуайт Эйзенхауэр (1890-1969)\n\n"
                    "• Прозвище: «Айк»\n"
                    "• Звание: Генерал армии\n"
                    "• Основные операции:\n"
                    "  - Высадка в Северной Африке (1942)\n"
                    "  - Высадка в Нормандии (1944)\n\n"
                    "Особенности:\n"
                    "- Верховный главнокомандующий союзными войсками в Европе\n"
                    "- После войны 34-й президент США\n"
                    "- Автор доктрины «массированного возмездия»",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Dwight_D._Eisenhower%2C_official_photo_portrait%2C_May_29%2C_1959.jpg/800px-Dwight_D._Eisenhower%2C_official_photo_portrait%2C_May_29%2C_1959.jpg"
        },
        {
            'text': "Дуглас Макартур (1880-1964)\n\n"
                    "• Звание: Генерал армии\n"
                    "• Основные операции:\n"
                    "  - Оборона Филиппин (1941-1942)\n"
                    "  - Освобождение Филиппин (1944-1945)\n"
                    "  - Принятие капитуляции Японии (1945)\n\n"
                    "Особенности:\n"
                    "- Командующий войсками союзников на Тихом океане\n"
                    "- Руководил оккупацией Японии (1945-1951)\n"
                    "- Участник Корейской войны (1950-1953)",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Douglas_MacArthur_%281885-1964%29_-_1950.jpg/800px-Douglas_MacArthur_%281885-1964%29_-_1950.jpg"
        }
    ],
    'uk': [
        {
            'text': "Бернард Монтгомери (1887-1976)\n\n"
                    "• Прозвище: «Монти»\n"
                    "• Звание: Фельдмаршал\n"
                    "• Основные операции:\n"
                    "  - Битва при Эль-Аламейне (1942)\n"
                    "  - Высадка в Нормандии (1944)\n"
                    "  - Операция «Маркет Гарден» (1944)\n\n"
                    "Особенности:\n"
                    "- Разгромил Роммеля в Северной Африке\n"
                    "- Принимал капитуляцию немецких войск в Северной Европе\n"
                    "- После войны заместитель верховного главнокомандующего НАТО",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Bernard_Law_Montgomery.jpg/800px-Bernard_Law_Montgomery.jpg"
        },
        {
            'text': "Харольд Александер (1891-1969)\n\n"
                    "• Звание: Фельдмаршал\n"
                    "• Основные операции:\n"
                    "  - Эвакуация из Дюнкерка (1940)\n"
                    "  - Итальянская кампания (1943-1945)\n\n"
                    "Особенности:\n"
                    "- Командующий союзными войсками в Италии\n"
                    "- После войны генерал-губернатор Канады\n"
                    "- Министр обороны Великобритании (1952-1954)",
            'photo': "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Harold_Alexander_1945.jpg/800px-Harold_Alexander_1945.jpg"
        }
    ]
}


async def safe_send_photo(context, chat_id, photo_url, caption):
    """Безопасная отправка фото с обработкой ошибок"""
    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=caption[:1000]  # Ограничение длины подписи
        )
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{caption}\n\n[Изображение временно недоступно]"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu_buttons = [
        [InlineKeyboardButton("🌍 Основные страны", callback_data='countries')],
        [InlineKeyboardButton("👤 Известные личности", callback_data='persons')],
        [InlineKeyboardButton("⚔️ Крупные сражения", callback_data='battles')],
        [InlineKeyboardButton("📜 Важные договоры", callback_data='treaties')],
        [InlineKeyboardButton("🧪 Тестовый режим", callback_data='test')]
    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📚 Выберите раздел о Второй мировой войне:",
        reply_markup=InlineKeyboardMarkup(menu_buttons)
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Обработка кнопок в разработке
    if query.data in ['battles', 'treaties', 'test']:
        back_button = [[InlineKeyboardButton("🔙 Выход", callback_data='exit')]]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⏳ Этот раздел находится в разработке. Скоро здесь появится больше информации!",
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return

    if query.data == 'exit':
        await query.delete_message()
        await start(update, context)
        return

    # Основные страны
    if query.data == 'countries':
        side_buttons = [
            [InlineKeyboardButton("🟥 Страны Оси", callback_data='axis')],
            [InlineKeyboardButton("🟦 Союзники", callback_data='allies')],
            [InlineKeyboardButton("🔙 Выход", callback_data='exit')]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите военно-политический блок:",
            reply_markup=InlineKeyboardMarkup(side_buttons)
        )

    elif query.data == 'persons':
        side_buttons = [
            [InlineKeyboardButton("🟥 Личности Оси", callback_data='axis_persons')],
            [InlineKeyboardButton("🟦 Личности Союзников", callback_data='allies_persons')],
            [InlineKeyboardButton("🔙 Выход", callback_data='exit')]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите сторону:",
            reply_markup=InlineKeyboardMarkup(side_buttons)
        )

    # Страны Оси
    elif query.data == 'axis':
        country_buttons = [
            [InlineKeyboardButton("🇩🇪 Германия", callback_data='germany')],
            [InlineKeyboardButton("🇮🇹 Италия", callback_data='italy')],
            [InlineKeyboardButton("🇯🇵 Япония", callback_data='japan')],
            [InlineKeyboardButton("🔙 Назад", callback_data='countries')]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🔴 Страны Оси (1940-1945):\n\n"
                 "Военно-политический союз Германии, Италии и Японии, "
                 "сформированный для совместных действий во Второй мировой войне.",
            reply_markup=InlineKeyboardMarkup(country_buttons)
        )

    # Страны Союзников
    elif query.data == 'allies':
        country_buttons = [
            [InlineKeyboardButton("🇬🇧 Великобритания", callback_data='uk')],
            [InlineKeyboardButton("🇺🇸 США", callback_data='usa')],
            [InlineKeyboardButton("🇷🇺 СССР", callback_data='ussr')],
            [InlineKeyboardButton("🔙 Назад", callback_data='countries')]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🔵 Антигитлеровская коалиция:\n\n"
                 "Военный союз государств, противостоявших странам Оси "
                 "во время Второй мировой войны.",
            reply_markup=InlineKeyboardMarkup(country_buttons)
        )

    # Информация о странах
    elif query.data in COUNTRIES_INFO:
        info = COUNTRIES_INFO[query.data]
        await safe_send_photo(
            context,
            query.message.chat_id,
            info['photo'],
            info['text']
        )

    # Личности Оси
    elif query.data == 'axis_persons':
        person_buttons = [
            [InlineKeyboardButton("🇩🇪 Немецкие", callback_data='germany_persons')],
            [InlineKeyboardButton("🇮🇹 Итальянские", callback_data='italy_persons')],
            [InlineKeyboardButton("🇯🇵 Японские", callback_data='japan_persons')],
            [InlineKeyboardButton("🔙 Назад", callback_data='persons')]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🟥 Ключевые личности стран Оси:",
            reply_markup=InlineKeyboardMarkup(person_buttons)
        )

    # Личности Союзников
    elif query.data == 'allies_persons':
        person_buttons = [
            [InlineKeyboardButton("🇬🇧 Британские", callback_data='uk_persons')],
            [InlineKeyboardButton("🇺🇸 Американские", callback_data='usa_persons')],
            [InlineKeyboardButton("🇷🇺 Советские", callback_data='ussr_persons')],
            [InlineKeyboardButton("🔙 Назад", callback_data='persons')]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🟦 Ключевые личности стран Союзников:",
            reply_markup=InlineKeyboardMarkup(person_buttons)
        )

    # Выбор типа личности
    elif query.data.endswith('_persons'):
        country = query.data.replace('_persons', '')

        type_buttons = [
            [InlineKeyboardButton("👑 Правители", callback_data=f'{country}_leaders')],
            [InlineKeyboardButton("🎖️ Военачальники", callback_data=f'{country}_commanders')],
            [InlineKeyboardButton("🔙 Назад", callback_data='axis_persons' if country in ['germany', 'italy',
                                                                                         'japan'] else 'allies_persons')]
        ]

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Выберите категорию для {country}:",
            reply_markup=InlineKeyboardMarkup(type_buttons)
        )

    # Правители стран
    elif query.data.endswith('_leaders'):
        country = query.data.replace('_leaders', '')
        if country in LEADERS_INFO:
            info = LEADERS_INFO[country]
            await safe_send_photo(
                context,
                query.message.chat_id,
                info['photo'],
                info['text']
            )

    # Военачальники стран
    elif query.data.endswith('_commanders'):
        country = query.data.replace('_commanders', '')
        if country in COMMANDERS_INFO:
            for commander in COMMANDERS_INFO[country]:
                await safe_send_photo(
                    context,
                    query.message.chat_id,
                    commander['photo'],
                    commander['text']
                )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Информация о военачальниках этой страны пока недоступна."
            )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Ошибка: {context.error}")
    if isinstance(update, Update) and update.callback_query:
        await update.callback_query.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")


def main() -> None:
    bot_token = "7415942764:AAGNRyPO94uUHrsf1Ie9XstZx-lTHa5k_fY"

    # Создаем новый event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(bot_token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_error_handler(error_handler)

    print("Бот успешно запущен!")

    try:
        loop.run_until_complete(application.run_polling())
    except KeyboardInterrupt:
        print("Бот остановлен")
    finally:
        loop.close()


if __name__ == '__main__':
    main()