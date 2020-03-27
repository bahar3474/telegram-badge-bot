import os

from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import cv2

from utils import check_id_and_save_image, overlay
from config import Config

config = Config()


def mark(update, context):
    try:
        id = update.message.forward_from.id
        key = update.message.chat_id
        check_id_and_save_image(id, config.token, f'images/{key}_org.jpg')
        context.user_data[key] = {
            'status': 'id',
            'id': id,
            'badge_id': None
        }
        print(id)

        text = 'بدج مورد نظر خود را انتخاب کنید.'
        buttons = [
            InlineKeyboardButton(text=badge['title'], callback_data=f'badge_{badge["id"]}')
            for badge in config.badges
        ]
        keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

        update.effective_message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text='اهدای بدج به این کاربر امکان‌پذیر نیست.')


def badge(update, context):
    try:
        key = update.effective_chat.id
        badge_id = update.callback_query.data.replace('badge_', '')
        context.user_data[key] = {
            'status': 'badge',
            'id': context.user_data[key]['id'],
            'badge_id': badge_id
        }

        image = cv2.imread(f'images/{key}_org.jpg')
        badge_img = cv2.imread('badges/badge.png', -1)
        badge_img = badge_img[:, (badge_img.shape[1] // 4):(badge_img.shape[1] // 4 * 3)]
        badge_img = cv2.resize(badge_img, None, fx=0.1, fy=0.1)
        image = overlay(badge_img, image)

        cv2.imwrite(f'images/{key}_edited.png', image)
        context.bot.send_photo(chat_id=key, photo=open(f'images/{key}_edited.png', 'rb'))
        print(context.user_data[key])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    os.makedirs('images', exist_ok=True)

    updater = Updater(config.token, use_context=True)

    updater.dispatcher.add_handler(MessageHandler(Filters.text, mark))
    updater.dispatcher.add_handler(CallbackQueryHandler(badge, pattern=r"badge_"))

    updater.start_polling()
    updater.idle()
