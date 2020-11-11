import logging
import os
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                        ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import CallbackContext, ConversationHandler
from tools.validators import logger_factory, link_validators
from tools.resources import (question1, question2, question3, question4,
                            question5, question6, question7, question8,
                            question9, question10)


logger = logging.getLogger(__name__)
debug_requests = logger_factory(logger=logger)

GROUP = os.getenv("GROUP")

(NAME, NICHE, VERTICAL, GEO, SPEND, CASES,
CASE_DETAILS, FINISH) = range(8)


@debug_requests
def start_buttons_handler(update: Update, context: CallbackContext):
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q1_'+name)
                                    for name in question1['answers']]
        ],
    )
    update.message.reply_text(
        parse_mode='HTML',
        text=question1['title']
    )
    update.message.reply_text(
        text=question1['title2'],
        reply_markup=inline_buttons,
    )
    return NAME


@debug_requests
def name_handler(update: Update, context: CallbackContext):
    if update.callback_query.data == 'q1_Нет':
        update.callback_query.message.reply_text(
            text=question2['title2']
        )
        return ConversationHandler.END
    update.callback_query.message.reply_text(
        text=question2['title']
    )
    return NICHE


@debug_requests
def niche_handler(update: Update, context: CallbackContext):
    context.user_data[NAME] = update.message.text
    logger.info('user_data: %s', context.user_data)

    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q4_'+name)
                                    for name in question4['answers'][:2]],
            [InlineKeyboardButton(text=name, callback_data='q4_'+name)
                                    for name in question4['answers'][2:]]
        ],
    )
    update.message.reply_text(
        text=question4['title'],
        reply_markup=inline_buttons,
    )
    return VERTICAL


@debug_requests
def vertical_handler(update: Update, context: CallbackContext):
    context.user_data[NICHE] = update.callback_query.data.split('_')[1]
    logger.info('user_data: %s', context.user_data)

    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q5_'+name)
                                    for name in question5['answers'][:2]],
            [InlineKeyboardButton(text=name, callback_data='q5_'+name)
                                    for name in question5['answers'][2:4]],
            [InlineKeyboardButton(text=name, callback_data='q5_'+name)
                                    for name in question5['answers'][4:]],
        ],
    )
    update.callback_query.edit_message_text(
        text=question5['title'],
        reply_markup=inline_buttons,
    )
    return GEO


@debug_requests
def geo_handler(update: Update, context: CallbackContext):
    context.user_data[VERTICAL] = update.callback_query.data.split('_')[1]
    logger.info('user_data: %s', context.user_data)

    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q6_'+name)
                                    for name in question6['answers']]
        ],
    )
    update.callback_query.edit_message_text(
        text=question6['title'],
        reply_markup=inline_buttons,
    )
    return SPEND


@debug_requests
def spend_handler(update: Update, context: CallbackContext):

    context.user_data[GEO] = update.callback_query.data.split('_')[1]
    logger.info('user_data: %s', context.user_data)

    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q7_'+name)
                                    for name in question7['answers'][:2]],
            [InlineKeyboardButton(text=name, callback_data='q7_'+name)
                                    for name in question7['answers'][2:4]],
            [InlineKeyboardButton(text=name, callback_data='q7_'+name)
                                    for name in question7['answers'][4:]],
        ],
    )
    update.callback_query.edit_message_text(
        text=question7['title'],
        reply_markup=inline_buttons,
    )
    return CASES


@debug_requests
def cases_handler(update: Update, context: CallbackContext):
    context.user_data[SPEND] = update.callback_query.data.split('_')[1]
    logger.info('user_data: %s', context.user_data)

    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q8_'+name)
                                    for name in question8['answers']]
        ],
    )
    update.callback_query.edit_message_text(
        text=question8['title'],
        reply_markup=inline_buttons,
    )
    return CASE_DETAILS


@debug_requests
def case_details_handler(update: Update, context: CallbackContext):
    context.user_data[CASES] = update.callback_query.data.split('_')[1]
    logger.info('user_data: %s', context.user_data)
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data='q9_'+name)
                                    for name in question9['answers']]
        ],
    )
    if update.callback_query.data == 'q8_Нет':
        update.callback_query.edit_message_text(
            text=question9['title2'],
            reply_markup=inline_buttons
        )
    else:
        update.callback_query.edit_message_text(
            text=question9['title']
        )
    return FINISH


@debug_requests
def finish_handler(update: Update, context: CallbackContext):
    try:
        request = update.callback_query.message
        context.user_data[CASE_DETAILS] = f'Готовность к тестовому заданию: '\
                                f'{update.callback_query.data.split("_")[1]}'

    except AttributeError:
        request = update.message
        link = link_validators(request.text)
        while link is not True:
            update.message.reply_text(
                text='Некорректный ссылка! Пожалуйста повторите попытку.',
            )
            return FINISH
        context.user_data[CASE_DETAILS] = f'Ссылки на успешные '\
                                        f'кейсы:\n{request.text}'
    current_user = request.chat.username
    logger.info('user_data: %s', context.user_data)
    request.reply_text(
        text=question10['title']
    )
    context.bot.send_message(chat_id=GROUP,
                            text=f'Новый отклик! От @{current_user}\n'\
                            f'Имя: {context.user_data[NAME]}\n'\
                            f'Работает c {context.user_data[NICHE]}\n'\
                            f'Вертикаль: {context.user_data[VERTICAL]}\n'\
                            f'ГЕО: {context.user_data[GEO]}\n'\
                            f'Кейсы: {context.user_data[CASES]}\n'\
                            f'{context.user_data[CASE_DETAILS]}\n')
    return ConversationHandler.END
