from logging import basicConfig, error, INFO
from pathlib import Path
from os import environ
from dotenv import load_dotenv
from random import choice

from telebot import TeleBot, types

from form import PythonDeveloperForm
from user_info import UserInfoManager
from form_dataclasses import Question, Form


BOT_TOKEN: str
PYTHON_DEVELOPER_FORM: Form = PythonDeveloperForm


def set_up() -> bool:

    global BOT_TOKEN, AVATAR_URL

    # Logging:
    basicConfig(level=INFO)

    # Environment variables:

    dotenv_path = Path(__file__).resolve().parent / '.env'

    load_dotenv(dotenv_path)

    BOT_TOKEN = environ.get('BOT_TOKEN', default=None)

    if not BOT_TOKEN:

        error('BOT_TOKEN environment variable is not set!')

        return False

    return True


def run_bot() -> None:

    question_answer_prefix = 'question_answer_'

    bot = TeleBot(BOT_TOKEN)

    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    main_markup.add(types.KeyboardButton(text='/help'))
    main_markup.add(types.KeyboardButton(text='/start_form'))
    main_markup.add(types.KeyboardButton(text='/restart'))

    def _move_user_to_next_question(message_or_callback_query: types.Message | types.CallbackQuery) -> None:

        with UserInfoManager(message_or_callback_query.from_user.id) as user_info_manager:

            user_current_question_index = user_info_manager.get_current_question_index()

            if isinstance(message_or_callback_query, types.CallbackQuery):

                message_to_reply = message_or_callback_query.message

                answer_index = int(message_or_callback_query.data.replace(question_answer_prefix, ''))

                user_answer = PYTHON_DEVELOPER_FORM.questions[user_current_question_index].answers[answer_index]

                user_info_manager.move_user_to_next_question(user_answer.weights)

                user_current_question_index = user_info_manager.get_current_question_index()

            else:
                message_to_reply = message_or_callback_query

        try:

            user_current_question: Question = PYTHON_DEVELOPER_FORM.questions[user_current_question_index]

            question_markup = types.InlineKeyboardMarkup()

            for i, answer in enumerate(user_current_question.answers):
                question_markup.add(types.InlineKeyboardButton(
                    text=answer.text, callback_data=f'{question_answer_prefix}{i}'
                ))

            bot.reply_to(message_to_reply, user_current_question.text, reply_markup=question_markup)

        except IndexError:

            with UserInfoManager(message_or_callback_query.from_user.id) as user_info_manager:
                user_final_weights = user_info_manager.complete_form()

            result_text, result_image_link = PYTHON_DEVELOPER_FORM.calculate_result(user_final_weights)

            bot.send_photo(message_to_reply.chat.id, result_image_link)

            bot.reply_to(
                message_to_reply,
                f'Анкета завершена, ответ:\n{result_text}',
            )

    @bot.message_handler(commands=['start_form'])
    def start_handler(message: types.Message):

        bot.reply_to(message, 'Хорошо, начнём/продолжим:')

        _move_user_to_next_question(message)

    @bot.callback_query_handler(func=lambda call: question_answer_prefix in call.data)
    def question_answer_handler(call: types.CallbackQuery):
        _move_user_to_next_question(call)

    @bot.message_handler(commands=['help', 'start'])
    def help_handler(message: types.Message):

        reply_message = (
            'Привет, я - бот-анкета, вот мой функционал:\n'
            '/help или /start - список всех команд (ты уже тут)\n'
            '/start_form - запуск/продолжение анкеты'
            ' (когда ты ответишь на все вопросы, появиться результат, всё для тебя)\n'
            '/restart - перезапуск анкеты'
        )

        bot.reply_to(message, reply_message, reply_markup=main_markup, parse_mode='HTML')

    @bot.message_handler(commands=['restart'])
    def restart_handler(message: types.Message):

        with UserInfoManager(message.from_user.id) as user_info_manager:
            user_info_manager.complete_form()

        bot.reply_to(message, 'Начинаем заново!')

        _move_user_to_next_question(message)

    @bot.message_handler(content_types=['text'])
    def text_handler(message: types.Message):

        replies = (
            'О, круто!',
            'Верно подмечено!',
            'Как с языка снял',
            'Какой ты всё-таки умный',
            'По-любому что-то умное написал',
            'Как лаконично то!',
        )

        bot.reply_to(message, choice(replies), reply_markup=main_markup)

    bot.infinity_polling()


def main():

    if set_up():
        run_bot()

    else:
        error('Setup cannot be completed, some errors occurred')


if __name__ == '__main__':
    main()
