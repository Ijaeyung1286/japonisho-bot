from typing import Final
import os
from telegram import (Update , InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ReplyKeyboardMarkup)
from telegram.ext import (Application ,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler, ContextTypes, filters)

TOKEN: Final = os.getenv("API_KEY")
print(TOKEN)
BOTNAME: Final = "@japonisho_bot"
backup_id: Final = 5271088482


keyboards = [
        ["پشتیبانی", "ثبت نام"],  ["راهنما ثبت نام"]
    ]

# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"chat id = {update.message.chat.id}")
    context.user_data["chat_id"] = update.message.chat.id
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

    global hire_message, form
    button = [
        ["بازگشت"]
    ]
    reply_markup2 = ReplyKeyboardMarkup(button, resize_keyboard=True)
    form =  await context.bot.send_message(text="""🇯🇵🇯🇵🇯🇵فرم ثبت نام🇯🇵🇯🇵🇯🇵
نام و نام خانوادگی:
سن:
شماره تماس:

وقت های آزاد پیشنهادی برای کلاس:""",
                                   chat_id=chat_id ,
                                   reply_markup=reply_markup2)

    hire_message = await context.bot.send_message(text="پیام بالا رو کپی کنید و با مشخصات خودتون ارسال کنید",
                                                  chat_id=chat_id)
    context.user_data["form"] = True

async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

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

    if "محمد فیروزی" in text:
        return True
    elif "محمد فيروزي" in text:
        return True
    else:
        return False

async def message_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.user_data["text"] = update.message.text
    global prush_message
    #backup_id: Final = 110729511
    if context.user_data.get("text")== "بازگشت":
        if context.user_data.get("backup"):
            context.user_data["backup"] = False
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            await context.bot.send_message(text="پیام به پشتیبانی لغو شد.",
                                           chat_id=chat_id, reply_markup=reply_markup)
        elif context.user_data.get("check") or context.user_data.get("form"):
            context.user_data["check"] = False
            context.user_data["form"] = False
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            try:
                await context.bot.deleteMessage(chat_id=chat_id, message_id=form.message_id)
                await context.bot.deleteMessage(chat_id=chat_id, message_id=hire_message.message_id)
                await context.bot.deleteMessage(chat_id=chat_id, message_id=prush_message.message_id)
            except Exception as e :
                print(f"error caused: {e}")
            await context.bot.send_message(chat_id=chat_id,
                                           text="پرداخت لغو شد",
                                           reply_markup=reply_markup)
        else:
            context.user_data["an"] = False
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            await context.bot.send_message(text="پاسخ به کاربر لغو شد",
                                           chat_id=backup_id, reply_markup=reply_markup)


    if context.user_data.get("backup"):
        message_id = update.message
        text = message_id.text
        button = [
            [InlineKeyboardButton(text="پاسخ",callback_data=f"answer____{chat_id}____{update.message.chat.username}____{message_id.message_id}")]
        ]
        reply_markup1= InlineKeyboardMarkup(button)
        send_text = f"کاربر با یوزر نیم :  {update.message.chat.username} و id: {chat_id}  گفت: {text}"
        print(send_text)
        if await context.bot.send_message(text=send_text, chat_id=backup_id, reply_markup=reply_markup1):
            reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
            await context.bot.send_message(text="پیام ارسال شد", chat_id=chat_id,
                                           reply_markup=reply_markup)
        context.user_data["backup"] = False
    elif context.user_data.get("form"):
        context.user_data["check"] = True

        buttons = [
            [InlineKeyboardButton("تکمیل پرداخت", callback_data="ready_to_check")],
            [InlineKeyboardButton("انصراف از پرداخت", callback_data="cancel")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        prush_message = await context.bot.send_message(text="""
لطفاً مبلغ را به شماره کارت زیر واریز کرده و رسید خود را ارسال کنید:
6104337805724044
احسان فیروزی (شماره کارت جعلی است)
    """, chat_id=chat_id, reply_markup=reply_markup)

        context.user_data["form_text"] = update.message.text
    elif context.user_data.get("check"):
        if response_to_message(context.user_data.get("text")):
            button = [
                [InlineKeyboardButton(text="پاسخ",callback_data=f"answer____{chat_id}____{update.message.chat.username}____{message_id.message_id}")]
            ]
            reply_markup1 = InlineKeyboardMarkup(button)
            if await context.bot.send_message(text=f"""💵🤑--------🤑💵\nپیام پرداخت کاربر: 
{context.user_data.get("text")}
 با یوزر نیم:
{update.message.chat.username} و id: {chat_id}"""
                                           , chat_id=backup_id,reply_markup=reply_markup1) and await context.bot.send_message(text=context.user_data.get("form_text"),
                                                                                                   chat_id=backup_id):
                reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
                await context.bot.send_message(text="پیام پرداخت ارسال شد و رفت برای چک شدن",
                                               chat_id=chat_id, reply_markup=reply_markup)
                context.user_data["check"] = False
        else:
            await context.bot.send_message(text="لطفا پیامک پرداخت رو ارسال کنید", chat_id=chat_id)
    elif context.user_data.get("text") == "ثبت نام":
        await prush_command(update,context)
    elif context.user_data.get("text") == "پشتیبانی":
        context.user_data["backup"] = True
        button = [
            ["بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
        await context.bot.send_message(text="پیام خود را ارسال کنید",
                                       chat_id=chat_id, reply_markup=reply_markup)
    elif context.user_data.get("text") == "راهنما ثبت نام":
        await help_command(update, context)
    elif context.user_data.get("an"):
         answer = f"""👩‍💻 پشتیبانی👩‍💻:

{update.message.text}"""
         if await context.bot.send_message(text=answer,
                                           chat_id=context.user_data.get("reply_to"),
                                           reply_to_message_id=context.user_data.get("sms")):
             reply_markup = ReplyKeyboardMarkup(keyboards,resize_keyboard=True)
             await context.bot.send_message(text="پیام با موفقیت ارسال شد😊" ,
                                            chat_id=backup_id,reply_markup=reply_markup)
             context.user_data["an"] = False

# pic handler

async def picture_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pic = update.message.photo[-1].file_id
    print(pic)
    chat_id = update.message.chat.id



    if context.user_data.get("check"):
        button = [
            [InlineKeyboardButton(text="پاسخ",callback_data=f"answer____{chat_id}____{update.message.chat.username}____{update.message.message_id}")]
        ]
        reply_markup1 = InlineKeyboardMarkup(button)
        if await context.bot.send_photo(photo=pic, chat_id=backup_id,reply_markup=reply_markup1):
            if await context.bot.send_message(text=f"عکس پرداخت کاربر با یوزر نیم : {update.message.chat.username} و id: {chat_id}",
                                       chat_id=backup_id) and await context.bot.send_message(text=context.user_data.get("form_text"),
                                                                                                   chat_id=backup_id):
                reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
                await context.bot.send_message(text="عکس پرداخت با موفقیت ارسال شد",
                                               chat_id=chat_id, reply_markup=reply_markup)
                context.user_data["check"] = False
                context.user_data["form"] = False
            else:
                await context.bot.send_message(text="تاسفانه مشخصات ارسال نشد", chat_id=chat_id)
        else:
            await context.bot.send_message(text="متاسفانه عکس ارسال نشد", chat_id=chat_id)
# button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
        context.user_data["form"] = False
        await context.bot.send_message(text="پیامک یا عکس پردخت رو ارسال کنید", chat_id=chat_id)
    elif query.data == "cancel":
        context.user_data["check"] = False
        context.user_data["form"] = False
        reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
        try:
            await context.bot.deleteMessage(chat_id=chat_id, message_id=form.message_id)
            await context.bot.deleteMessage(chat_id=chat_id, message_id=hire_message.message_id)
            await context.bot.deleteMessage(chat_id=chat_id, message_id=prush_message.message_id)

        except Exception as e:
            print(f"error caused : {e}")
        await context.bot.send_message(chat_id=chat_id,
                                       text="پرداخت لغو شد",
                                       reply_markup=reply_markup)
    elif query.data =="help":
        await help_command(update,context)
    elif query.data.startswith("answer"):
        button = [["بازگشت"]]
        reply_markup  = ReplyKeyboardMarkup(button,resize_keyboard=True)
        user_id = int(query.data.split("____")[1])
        user_name= query.data.split("____")[2]
        message = query.data.split("____")[3]
        await context.bot.send_message(
            text=f"پاسخ خود را به کاربر: {user_id} با ایدی: {user_name} را ارسال کنید:",
            chat_id=backup_id, reply_markup=reply_markup)
        context.user_data["reply_to"] = user_id
        context.user_data["sms"] = message
        context.user_data["an"] = True

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



