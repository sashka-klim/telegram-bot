import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

ADMIN_ID = 5885452017
users_set = set()  # Множество для хранения уникальных пользователей
total_users = 0  # Счётчик пользователей
stats = {}



# ========== 🔐 Вставь сюда токен ==========
import os
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ========== 🔢 Тесты ==========
test_data = {
    'Тест на кибербуллинг': {
        'description': "Оцени свой опыт травли в интернете.",
        'questions': [
            {'question': "Мне писали оскорбительные сообщения или комментарии.", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "Мои личные фото/данные использовали без разрешения, чтобы унизить меня.", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "Меня исключали из чатов/групп специально, чтобы обидеть.", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "Мне угрожали или шантажировали в сети.", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "Я боялся(-ась) заходить в соцсети из-за травли.", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
        ]
    },
    'Тест на суицидальные мысли (адаптация SHPS)': {
        'description': "Оценка наличия суицидальных мыслей сейчас (или в прошлом).",
         'questions': [
            {'question': "У меня был период, когда я думал о смерти", 'answers': ['Да', 'Нет'], 'scores': [2, 0]},
            {'question': "У меня был период, когда мне казалось, что жизнь не имеет смысла", 'answers': ['Да', 'Нет'], 'scores': [2, 0]},
            {'question': "Я представлял(-а), как могу причинить себе вред", 'answers': ['Да', 'Нет'], 'scores': [2, 0]},
            {'question': "У меня был план уйти из жизни", 'answers': ['Да', 'Нет'], 'scores': [2, 0]},
            {'question': "У меня был период, когда я чувствовал, что никому не могу рассказать о своих переживаниях", 'answers': ['Да', 'Нет'], 'scores': [2, 0]},
         ]
    },
     'Шкала тревоги (GAD-7, сокращенная версия)': {
        'description': "Оценка наличия тревоги сейчас (или в прошлом).",
        'questions': [
            {'question': "Я чувствую/чувствовал(-а) беспокойство без причины", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "У меня был период, когда мне было трудно контролировать свои страхи", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "Я избегаю/избегал(-а) ситуаций, которые вызывают тревогу", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
            {'question': "У меня бывают/были панические атаки", 'answers': ['Никогда', 'Редко','Иногда', 'Часто'], 'scores': [0, 1, 2, 3]},
        ]
    },
    'Тест на депрессию (PHQ-9, упрощенный)': {
        'description': "Оценка наличия депрессии сейчас (или в прошлом).",
        'questions': [
            {'question': "У меня был период, когда мне ничего не приносило радость", 'answers': ['Редко','Иногда','Часто','Постоянно'], 'scores': [0, 1, 2, 3]},
            {'question': "У меня был период, когда я чувствовал(-а) усталость, даже когда ничего не делал(-а)", 'answers': ['Редко','Иногда','Часто','Постоянно'], 'scores': [0, 1, 2, 3]},
            {'question': "У меня был период, когда мне было трудно сосредоточиться", 'answers': ['Редко','Иногда','Часто','Постоянно'], 'scores': [0, 1, 2, 3]},
            {'question': "У меня был период, когда думал(-а), что я неудачник(-ца)", 'answers': ['Редко','Иногда','Часто','Постоянно'], 'scores': [0, 1, 2, 3]},
            {'question': "У меня бывают/были мысли о самоповреждении", 'answers': ['Редко','Иногда','Часто','Постоянно'], 'scores': [0, 1, 2, 3]},
        ]
    },
    'Тест на предрасположенность к агрессии в интернете (адаптация CBPS)': {
        'description': "Проверяет частоту и формы враждебности в интернете (напоминаю, тест абсолютно анонимный).",
        'questions': [
            {'question': "Ты когда-нибудь писал(а) грубые/оскорбительные комментарии под чужими постами?", 'answers': ['Никогда', 'Один-два раза', 'Регулярно'], 'scores': [0, 1, 2]},
            {'question': "Ты распространял(а) личные фото/переписки человека без его согласия?", 'answers': ['Нет', 'Да, но «просто так»', 'Да, чтобы унизить'], 'scores': [0, 1, 2]},
            {'question': "Создавал(а) ли ты фейковые аккаунты для троллинга?", 'answers': ['Нет', 'Да, ради шутки', 'Да, чтобы задеть'], 'scores': [0, 1, 2]},
            {'question': "Ты участвовал(а) в групповом троллинге (например, в чатах класса)?", 'answers': ['Нет', 'Был(а) наблюдателем', 'Да, писал(а) гадости'], 'scores': [0, 1, 2]},
            {'question': "Ты угрожал(а) кому-то в сети (даже «в шутку»)?", 'answers': ['Нет', 'Да, но не всерьёз', 'Да, чтобы напугать'], 'scores': [0, 1, 2]},
        ]
    }
}
# ========== 🧠 Интерпретация ==========
def interpret_result(test_name, score):
    if test_name == 'Тест на кибербуллинг':
        if score <= 5:
            return "Низкий риск"
        elif score <= 10:
            return "Умеренный опыт кибербуллинга"
        else:
            return "Высокий уровень травли"

    elif test_name == 'Тест на суицидальные мысли (адаптация SHPS)':
        if score <= 4:
            return "У вас низкий уровень суицидального поведения."
        else:
            return (
                "Даже если вам кажется, что выхода нет, он есть.\n"
                "Обратитесь к специалисту (психологу) или по телефону доверия: 8-800-2000-122, не стесняйтесь просить о помощи, это нормально."
            )
    elif test_name == 'Шкала тревоги (GAD-7, сокращенная версия)':
        if score <= 4:
            return "У вас минимальный уровень тревоги."
        elif score <= 9:
            return "Умеренный уровень тревоги."
        else:
            return "Высокий уровень тревоги. Рекомендуется обратиться к специалисту (психологу), не стесняйтесь просить о помощи, это нормально."

    elif test_name == 'Тест на депрессию (PHQ-9, упрощенный)':
        if score <= 6:
            return "Нет признаков депрессии."
        elif score <= 12:
            return "Легкая/умеренная депрессия."
        else:
            return "Тяжелая депрессия. Обратитесь за поддержкой к специалисту (психологу),не стесняйтесь просить о помощи, это нормально."

    elif test_name == 'Тест на предрасположенность к агрессии в интернете (адаптация CBPS)':
        if score <= 4:
            return "Низкая склонность к агрессивному поведению в интернете."

        else:
            return "Высокая склонность к агрессивному поведению в интернете. Рекомендуется обратиться к специалисту (психологу)."
    else:
        return "Результат вне шкалы"

def update_stats(test_name, result_text):
    if test_name not in stats:
        stats[test_name] = {}
    if result_text not in stats[test_name]:
        stats[test_name][result_text] = 0
    stats[test_name][result_text] += 1

# ========== 📊 Состояние пользователя ==========
user_states = {}

# ========== 🚀 Старт ==========
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        'test_names': list(test_data.keys()),
        'current_test': 0,
        'current_question': 0,
        'score': 0
    }

    # Приветственное сообщение
    greeting_message = (
        f"Здравствуйте,! 👋\n\n"
        "Далее вам будет предложено пройти 5 тестов на тему кибербуллинга. Это не займет у вас много времени, постарайтесь отвечать максимально честно, тестирование абсолютно анонимное и проводится в рамках исследования 'Влияние кибербуллинга на суицидальное поведение подростков'.\n"
        "Обращаю Ваше внимание, что результаты — не диагноз. Если вас что-то беспокоит, поговорите со специалистом (психологом).\n\n"
        "Если готовы, нажмите 'Начать тестирование', чтобы приступить к первому тесту!"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Начать тестирование", callback_data="start_tests"))

    bot.send_message(chat_id, greeting_message, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == 'start_tests')
def handle_start_tests(call):
    chat_id = call.message.chat.id
    send_question(chat_id)

def send_question(chat_id):
    state = user_states[chat_id]
    test_name = state['test_names'][state['current_test']]
    test = test_data[test_name]
    q_index = state['current_question']
    question_data = test['questions'][q_index]

    markup = InlineKeyboardMarkup()
    for i, ans in enumerate(question_data['answers']):
        callback_data = f"answer:{i}"
        markup.add(InlineKeyboardButton(ans, callback_data=callback_data))

    bot.send_message(chat_id, f"*{test_name}*\n_{test['description']}_\n\n{question_data['question']}",
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('answer:'))
def handle_answer(call):
    global total_users
    chat_id = call.message.chat.id
    index = int(call.data.split(":")[1])
    state = user_states[chat_id]
    test_name = state['test_names'][state['current_test']]
    test = test_data[test_name]
    q_index = state['current_question']

    score = test['questions'][q_index]['scores'][index]
    state['score'] += score
    state['current_question'] += 1

    if state['current_question'] < len(test['questions']):
        send_question(chat_id)
    else:
        result_text = interpret_result(test_name, state['score'])
        update_stats(test_name, result_text)

        # Отправляем результат по тесту
        bot.send_message(chat_id, f"✅ *Результат по тесту «{test_name}»:*\n\n{result_text}", parse_mode="Markdown")

        # Дополнительный вопрос после определенных тестов в зависимости от баллов
        if test_name in ['Тест на суицидальные мысли (адаптация SHPS)', 'Шкала тревоги (GAD-7, сокращенная версия)', 'Тест на депрессию (PHQ-9, упрощенный)']:
            if state['score'] >= 4:  # Если балл выше определенного порога
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("Да", callback_data="additional_yes"))
                markup.add(InlineKeyboardButton("Нет", callback_data="additional_no"))
                bot.send_message(
                    chat_id,
                    "Дополнительный вопрос: Данное состояние было после кибербуллинга?",
                    reply_markup=markup
                )

                # Отмечаем, что дополнительный вопрос был задан
                state['additional_question_asked'] = True
            else:
                # Переходим к следующему тесту, если баллы не превышают порог
                if state['current_test'] < len(state['test_names']) - 1:
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("▶️ Перейти к следующему тесту", callback_data="next_test"))
                    bot.send_message(chat_id, "Нажми 'Перейти к следующему тесту', чтобы продолжить тестирование", reply_markup=markup)
                else:
                    # Завершаем тестирование, если это последний тест
                    bot.send_message(chat_id, "🎉 Вы прошли все тесты! Спасибо за участие в исследовании.")
                    user_states.pop(chat_id)
                    users_set.add(chat_id)

        else:
            # Если это не тот тест, который требует дополнительного вопроса, просто переходим к следующему
            if state['current_test'] < len(state['test_names']) - 1:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("▶️ Перейти к следующему тесту", callback_data="next_test"))
                bot.send_message(chat_id, "Нажми 'Перейти к следующему тесту', чтобы продолжить тестирование", reply_markup=markup)
            else:
                bot.send_message(chat_id, "🎉 Вы прошли все тесты! Спасибо за участие в исследовании.")
                user_states.pop(chat_id)
                users_set.add(chat_id)

@bot.callback_query_handler(func=lambda call: call.data in ['additional_yes', 'additional_no'])
def handle_additional_question_response(call):
    chat_id = call.message.chat.id
    state = user_states.get(chat_id)

    if not state or not state.get('additional_question_asked'):
        return  # Если вопрос не был задан или пользователь не находится в процессе тестирования, выходим

    # Сохраняем ответ на дополнительный вопрос в статистике
    user_response = "Да" if call.data == 'additional_yes' else "Нет"
    update_additional_stat(state['test_names'][state['current_test']], user_response)  # Используем test_name

    # Снимаем отметку о том, что вопрос был задан
    state['additional_question_asked'] = False

    # Переходим к следующему тесту
    if state['current_test'] < len(state['test_names']) - 1:  # Если это не последний тест
        state['current_test'] += 1
        state['current_question'] = 0
        state['score'] = 0
        send_question(chat_id)
    else:
        # Если все тесты завершены
        bot.send_message(chat_id, "🎉 Вы прошли все тесты! Спасибо за участие в исследовании.")
        user_states.pop(chat_id)  # Удаляем пользователя из состояния
        users_set.add(chat_id)  # Добавляем в список завершивших тестирование

def update_additional_stat(test_name, response):
    # Эта функция обновляет статистику с учетом дополнительных вопросов
    key = f"Доп. вопрос после «{test_name}»"

    # Проверяем, существует ли уже такой раздел в статистике, если нет — создаем
    if key not in stats:
        stats[key] = {}

    # Если ответ на вопрос еще не был учтен, добавляем его в статистику
    if response not in stats[key]:
        stats[key][response] = 0

    # Увеличиваем количество ответов на выбранный вариант (Да или Нет)
    stats[key][response] += 1
@bot.callback_query_handler(func=lambda call: call.data == 'next_test')
def handle_next_test(call):
    chat_id = call.message.chat.id
    state = user_states.get(chat_id)

    if not state:
        return  # Если нет данных о пользователе, выходим из функции


    state['current_test'] += 1
    state['current_question'] = 0
    state['score'] = 0

    if state['current_test'] < len(state['test_names']):
        send_question(chat_id)
    else:
        # Отправляем финальное сообщение о завершении всех тестов
        bot.send_message(chat_id, "🎉 Вы прошли тестирование! Спасибо за участие в исследовании.")

        # Удаляем пользователя из user_states после завершения тестов
        user_states.pop(chat_id)

        # Если завершены все тесты, добавляем в статистику
        users_set.add(chat_id)

@bot.message_handler(commands=['stats'])
def handle_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "У вас нет доступа к статистике.")
        return

    if not stats:
        bot.send_message(message.chat.id, "Статистика пока пуста.")
        return

    response = f"📊 *Общее количество уникальных пользователей, завершивших все тесты:* {len(users_set)}\n\n"
    response += "📊 *Статистика прохождения тестов:*\n"

    for test, results in stats.items():
        if test.startswith("Доп. вопрос"):  # Эти блоки вставим после нужных тестов отдельно
            continue

        response += f"\n*{test}*\n"
        for result, count in results.items():
            response += f"— {result}: {count} чел.\n"

        # Добавим дополнительный блок, если есть
        extra_key = f"Доп. вопрос после «{test}»"
        if extra_key in stats:
            response += f"\n_Доп. вопрос после «{test}»: «Данное состояние было после кибербуллинга?»_\n"
            for answer, count in stats[extra_key].items():
                response += f"— {answer}: {count} чел.\n"

    bot.send_message(message.chat.id, response, parse_mode="Markdown")


# ========== 🔁 Запуск ==========
bot.polling(none_stop=True)
