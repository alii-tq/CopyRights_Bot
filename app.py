from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.error import BadRequest
import os
from os import environ
from time import sleep as s
import json


def paste_CopyRights(raw, type):
    if type == 1:
        bg_top = Image.open("bg_top_light.png")
        bg_bottom = Image.open("bg_bottom_light.png")
    if type == 2:
        bg_top = Image.open("bg_top_dark.png")
        bg_bottom = Image.open("bg_bottom_dark.png")
    img = Image.open(raw)
    x, y = img.size
    width_t, height_t = bg_top.size
    width_b, height_b = bg_bottom.size
    max_size = (1000,1000)
    bg_top.thumbnail(max_size)
    bg_bottom.thumbnail(max_size)

    img.paste(bg_bottom, (round((x/2)-500), (y-1000)), bg_bottom.convert('RGBA'))
    img.paste(bg_top, (round((x/2)-500), (0)), bg_top.convert('RGBA'))
    os.remove("img.jpg")
    img.save("img_out.jpg")

def isEnglish(s):
  return s.isascii()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send Me Your Image ...')

def ask(update, context) -> None:
    keyboard = [[ InlineKeyboardButton("Light", callback_data='Light'), InlineKeyboardButton("Dark", callback_data='Dark'),],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select one ?!', reply_markup = reply_markup)
    

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    global ans
    ans = query.data   
    seending(upp, conn)

def seending(update: Update, context: CallbackContext) -> None:
    if ans is not None:
        try:
            context.bot.sendChatAction(chat_id=update.message.chat_id , action = telegram.ChatAction.UPLOAD_PHOTO)
            s(3) 
            img = "img.jpg"
            if ans == "Light":
                paste_CopyRights(img, 1)
            elif ans == "Dark":
                paste_CopyRights(img, 2)
            else:
                context.bot.send_message(update.effective_chat.id,"Sorry, Try again...")
            output_img = "img_out.jpg"
            context.bot.send_photo(chat_id = update.message.chat_id, photo = open(output_img, 'rb'))
            s(3)
            os.remove(output_img)

        except(BadRequest, TimeoutError,RuntimeError, TypeError, NameError) as err:
            context.bot.send_message(update.effective_chat.id,"Sorry, Try again...")
            print(err)
                
def photo_handler(update: Update, context: CallbackContext) -> None:  
    global upp
    global conn
    upp = update
    conn = context

    try:    
        context.bot.sendChatAction(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
        s(2)
        global file_id
        file_id = update.message.photo[-1].file_id
        img = context.bot.getFile(file_id)
        img.download("img.jpg")
        ask(update, context)
    except(BadRequest, TimeoutError,RuntimeError, TypeError, NameError) as err:
        context.bot.send_message(update.effective_chat.id,"Sorry, Try again...")
        print(err)

def main():
    # img = Image.open("2.jpg")

    bg_top_dark = Image.open("bg_top_dark.png")
    bg_bottom_dark = Image.open("bg_bottom_dark.png")

    bg_top_light = Image.open("bg_top_light.png")
    bg_bottom_light = Image.open("bg_bottom_light.png")

    # paste_CopyRights(img, bg_top_dark, bg_bottom_dark)

    global dp
    global updater
    updater = Updater("{}".format(environ['API_VALUE']), use_context=True, request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    with open('api.json') as jsonF:
        data = json.load(jsonF)
    # updater = Updater("{}".format(data['botApiKey']), use_context=True, request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    #calling video_handler function
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()



