from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import cv2

from utils import render_badge
from config import Config

config = Config()


def save_user_info_and_show_badges(update, context):
    try:
        # Store user id of forwarded message
        user_id = update.message.forward_from.id
        user_name = update.message.forward_from.first_name
        key = update.message.chat_id
        context.user_data[key] = {'id': user_id, 'name': user_name}

        # Show badges to user
        text = config.messages['choose_badge']
        buttons = [
            InlineKeyboardButton(text=badge['title'],
                                 callback_data=f'badge_{badge["id"]}')
            for badge in config.badges
        ]
        keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

        update.effective_message.reply_text(text,
                                            reply_markup=InlineKeyboardMarkup(
                                                keyboard))

    except Exception as e:
        with open('errors.log', 'a') as f:
            f.write(f'{update.effective_chat.id} - '
                    f'save_user_info_and_show_badges: {e}')

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=config.messages['error'])


def attach_badge(update, context):
    try:
        # Extract user id from context
        key = update.effective_chat.id
        user_id = context.user_data[key]['id']
        user_name = context.user_data[key]['name']
        badge_id = update.callback_query.data.replace('badge_', '')

        # Generate badge and send final photo
        badge_path = render_badge(user_name, user_id, badge_id)
        context.bot.send_photo(chat_id=key,
                               photo=open(badge_path, 'rb'))

    except Exception as e:
        with open('errors.log', 'a') as f:
            f.write(f'{update.effective_chat.id} - attach_badge: {e}')


if __name__ == '__main__':
    updater = Updater(config.token, use_context=True)

    # Define handler for text messages
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, save_user_info_and_show_badges))
    # Define andler for pressing badge buttons
    updater.dispatcher.add_handler(CallbackQueryHandler(attach_badge,
                                                        pattern=r"badge_"))

    updater.start_polling()
    updater.idle()
