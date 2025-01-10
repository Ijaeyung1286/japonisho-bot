import os
from dotenv import load_dotenv
from typing import Final
from telegram import (Update , InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ReplyKeyboardMarkup)
from telegram.ext import (Application ,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler, ContextTypes, filters)

load_dotenv()
TOKEN: Final = os.getenv("BOT_TOKEN")
print(TOKEN)
BOTNAME: Final = "@japonisho_bot"


keyboards = [
        ["پشتیبانی", "ثبت نام"],  ["راهنما ثبت نام"]
    ]

# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"chat id = {update.message.chat.id}")
    global keyboards

    reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
    await update.message.reply_text("""سلام به ربات japonisho خوش آمدید!""",
                                    reply_markup=reply_markup,)
    buttons = [
        [InlineKeyboardButton("ثبت نام", callback_data="prush"),
         InlineKeyboardButton("اینستاگرام",
                              url="https://www.instagram.com/japonisho?igsh=MXQ0OGg1czA0MDlrZA==")],
        [InlineKeyboardButton("پشتیبانی", callback_data="backup"),
         InlineKeyboardButton("راهنمای ثبت نام", callback_data="help")]
    ]
    btmarkup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("""
شما از طریق این ربات میتونید در کلاس های آنلاین ما شرکت کنید ، هر جلسه 220 هزار تومان است که برای ثبت نام پنج جلسه (برای ثبت نام حتما باید پنج جلسه یا بیشتر تهیه کنید ) 1,100,000 (یک میلیون و صد هزار تومان) پرداخت کنید.

پیج ما  https://www.instagram.com/japonisho?igsh=MXQ0OGg1czA0MDlrZA==

 """,reply_markup=btmarkup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(text="""برای ثبت نام اول شما به شماره کارتی که ما برای شما ارسال میکنیم هزینه رو واریز میکنید 
و بعد از تایید (ممکن که تا یک روز طول بکشه)
استاد به شما پیام میدن و به شما میگن که که چطور در کلاس ها شرکت کنید.""", chat_id=chat_id)
    button = [
        [InlineKeyboardButton("ثبت نام", callback_data="prush")]
    ]
    reply_markup = InlineKeyboardMarkup(button)

    await context.bot.send_message(text="برای شروع ثبت نام روی دکمه زیر کلیک کنید",
                                    reply_markup=reply_markup, chat_id=chat_id)

async def prush_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("تکمیل پرداخت", callback_data="ready_to_check")],
        [InlineKeyboardButton("انصراف از پرداخت", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    global prush_message, hire_message
    button = [
        ["بازگشت"]
    ]
    reply_markup2 = ReplyKeyboardMarkup(button, resize_keyboard=True)
    hire_message = await context.bot.send_message(text="ثبت نام",
                                   chat_id=chat_id ,
                                   reply_markup=reply_markup2)
    prush_message = await context.bot.send_message(text="""به شماره کارت زیر به مقدار هر چند جلسه که میخواهید پول واریز کنید و سپس روی دکمه تکمیل پرداخت کلیک کنید.


6104337805724044
                                                                     احسان فیروزی 
 


این پیام تست است لطفاً چیزی واریز نکنید و همینطور شماره حساب دروغین است""",
                                                   reply_markup=reply_markup, chat_id=chat_id)

async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    backup_id: Final = 110729511
    context.user_data["backup"] = True

    button = [
        ["بازگشت"]
    ]
    reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
    await context.bot.send_message(text="پیام خود را ارسال کنید",
                                   chat_id=chat_id,
                                   reply_markup=reply_markup)

# message handler

def response_to_message(text):
    global check
    if "محمد فیروزی" in text:
        if check:
            return True
    elif "محمد فيروزي" in text:
        if check:
            return True
    else:
        return False

async def message_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    backup_id: Final = 110729511
    global check , keyboards, hire_message
    backup = context.user_data.get("backup")
    check = context.user_data.get("check")
    print(backup)
    if text== "بازگشت":
        if backup:
            backup = context.user_data["backup"] = False
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            await context.bot.send_message(text="پیام به پشتیبانی لغو شد.",
                                           chat_id=chat_id, reply_markup=reply_markup)
        else:
            check = context.user_data["check"] = False
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            await context.bot.deleteMessage(chat_id=chat_id, message_id=hire_message.message_id)
            await context.bot.deleteMessage(chat_id=chat_id, message_id=prush_message.message_id)
            await context.bot.send_message(chat_id=chat_id,
                                           text="پرداخت لغو شد",
                                           reply_markup=reply_markup)

    if backup:
        text = update.message.text
        send_text = f"کاربر با یوزر نیم :  {update.message.chat.username} و id: {chat_id}  گفت: {text}"
        print(send_text)
        if await context.bot.send_message(text=send_text, chat_id=backup_id):
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            await context.bot.send_message(text="پیام ارسال شد", chat_id=chat_id,
                                           reply_markup=reply_markup)
        backup = context.user_data["backup"] = False
    elif check:
        if response_to_message(text):
            if await context.bot.send_message(text=f"""پیام پرداخت کاربر: 
{text}
 با یوزر نیم:
{update.message.chat.username} و id: {chat_id}"""
                                           , chat_id=backup_id):
                reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
                await context.bot.send_message(text="پیام پرداخت ارسال شد و رفت برای چک شدن",
                                               chat_id=chat_id, reply_markup=reply_markup)
                check = context.user_data["check"] = False
        else:
            await context.bot.send_message(text="لطفا پیامک پرداخت رو ارسال کنید", chat_id=chat_id)
    elif text == "ثبت نام":
        await prush_command(update,context)
    elif text == "پشتیبانی":
        context.user_data["backup"] = True
        button = [
            ["بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
        await context.bot.send_message(text="پیام خود را ارسال کنید",
                                       chat_id=chat_id, reply_markup=reply_markup)

    elif text == "راهنما ثبت نام":
        await help_command(update, context)
    elif response_to_message(text):
        pass
# pic handler

async def picture_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pic = update.message.photo[-1].file_id
    print(pic)
    chat_id = update.message.chat.id
    backup_id: Final = 110729511
    global check
    check = context.user_data.get("check")
    if check:
        if await context.bot.send_photo(photo=pic, chat_id=backup_id):
            if await context.bot.send_message(text=f"عکس پرداخت کاربر با یوزر نیم : {update.message.chat.username} و id: {chat_id}",
                                       chat_id=backup_id):
                reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
                await context.bot.send_message(text="عکس پرداخت با موفقیت ارسال شد",
                                               chat_id=chat_id, reply_markup=reply_markup)
                check = context.user_data["check"] = False
            else:
                await context.bot.send_message(text="تاسفانه مشخصات ارسال نشد", chat_id=chat_id)
        else:
            await context.bot.send_message(text="متاسفانه عکس ارسال نشد", chat_id=chat_id)
# button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global prush_messag
    chat_id = update.effective_chat.id
    query = update.callback_query
    if query.data == "prush":
        await prush_command(update,context)
    elif query.data == "backup":
        context.user_data["backup"] = True
        button = [
            ["بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
        await context.bot.send_message(text="پیام خود را ارسال کنید",
                                       chat_id=chat_id, reply_markup=reply_markup)
        print(f"back up = {context.user_data["backup"]}")
    elif query.data == "ready_to_check":
        context.user_data["check"] = True
        await context.bot.send_message(text="پیامک یا عکس پردخت رو ارسال کنید", chat_id=chat_id)
    elif query.data == "cancel":
        context.user_data["backup"] = False
        reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
        await context.bot.deleteMessage(chat_id=chat_id, message_id=hire_message.message_id)
        await context.bot.deleteMessage(chat_id=chat_id, message_id=prush_message.message_id)

        await context.bot.send_message(chat_id=chat_id,
                                       text="پرداخت لغو شد",
                                       reply_markup=reply_markup)
    elif query.data =="help":
        await help_command(update,context)

if __name__ == "__main__":
    print("starting app...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("prush", prush_command))
    app.add_handler(CommandHandler("poshtibani", backup_command))
    app.add_handler(MessageHandler(filters.PHOTO, picture_handler))
    app.add_handler(MessageHandler(filters.TEXT, message_text_handler))

    app.add_handler(CallbackQueryHandler(button_handler))
    print("polling ...")
    app.run_polling(poll_interval=0.5)

