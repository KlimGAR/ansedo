import logging
import sqlite3

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
# ---------------- tools ----------------
logger = logging.getLogger(__name__)
TOKEN = '6693149081:AAEoLL-E4KTBBPMrccPoa_vysJeZVi4unVg'
TAG_BOT = '@Ansedo_Bot'
ASK_NAME, ASK_GAME, ASK_COOP, ASK_HOURS, ASK_DESC = range(1, 6)
SEARCH = 1
con: sqlite3
cur: sqlite3.Connection.cursor


def __open_data_base() -> None:
    global con, cur
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()


# ---------------- Commands ----------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"<b>Привет {user.mention_html()}! Я бот, который поможет найти команду или сокомадника."
        f" Cначала ознакомьтесь с командами ( /help ).</b>",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html("<b>🠖</b> /new - <i>создать или обновить свою анкету</i>\n"
                                    "   <b>▼</b>\n"
                                    "   <b>🠖</b> /cancel - <i>отменить создание анкеты</i>\n"
                                    "<b>🠖</b> /view - <i>перейти к поиску</i>\n"
                                    "   <b>▼</b>\n"
                                    "   <b>🠖</b> /s - <i>прекратить поиск</i>\n"
                                    "<b>🠖</b> /stop - <i>!редакнуть!</i>\n"
                                    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("soon..")


async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    __open_data_base()
    user_id = update.effective_user.id
    res = cur.execute(f"""SELECT user_id FROM profile""").fetchall()
    if res and user_id in [i[0] for i in res]:
        await update.message.reply_text('adsasdasd')
        print('\n\n\n\n ВЫЗОВ РАБОТЫ \n\n\n')
        return SEARCH
    else:
        await update.message.reply_html("Без вашей анкеты, я бессилен (...")


async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    __open_data_base()
    data = context.user_data
    user_id = update.effective_user.id
    res = cur.execute(f"""SELECT user_id FROM profile""").fetchall()
    if res and user_id in [i[0] for i in res]:
        cur.execute(f"""DELETE FROM profile WHERE user_id = '{user_id}'""").fetchall()
        con.commit()
    data['user_id'] = user_id
    await update.message.reply_text("Как мне тебя называть ?")
    return ASK_NAME


# --- Search ---

async def _work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_game = cur.execute(f"""SELECT game FROM profile WHERE user_id = '{user_id}'""").fetchall()
    res1 = cur.execute(
        f"""SELECT name, st, hours, description, user_id FROM profile WHERE game = '{user_game[0][0]}' AND user_id != '{user_id}'""").fetchall()
    keyboard_games = [['👍', '👎']]
    reply_markup = ReplyKeyboardMarkup(keyboard_games, one_time_keyboard=True, resize_keyboard=True)
    for i in res1:
        one = list(map(str, list(i[:-1])))
        id = i[-1]
        one = '|'.join(one)
        await update.message.reply_html(f"{one}", reply_markup=reply_markup)
        user_message = update.message.text
        if user_message == '👍':
            await _picked(update, context, id)
        elif user_message != '👎':
            await update.message.reply_text(f"Нет такого варинта ответа.")
    await update.message.reply_text(f"Анкет на вашу игру не осталось. ˙ᵕ˙")
    return ConversationHandler.END


async def _picked(update: Update, context: ContextTypes.DEFAULT_TYPE, id: str | int):
    print('\n\n\n\n\n____________________________________________')
    chat = context.bot.get_chat(id)
    nickname = chat.username
    await update.message.reply_text(f"{nickname}")
    return SEARCH


# --- Profile ---

async def _name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    data = context.user_data
    data['name'] = user_message

    # ----SAVED!

    keyboard_games = [['CS2', 'Dota 2',
                       'Pubg', 'Roblox'], ['Fortnite', 'Valorant',
                                           'Minecraft', 'Terarria']]
    reply_markup = ReplyKeyboardMarkup(keyboard_games, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("По какой игре ?", reply_markup=reply_markup)

    return ASK_GAME


async def _game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_games = [['CS2', 'Dota 2',
                       'Pubg', 'Roblox'], ['Fortnite', 'Valorant',
                                           'Minecraft', 'Terarria']]

    user_message = update.message.text

    if user_message not in keyboard_games[0] and user_message not in keyboard_games[1]:
        return ASK_GAME

    data = context.user_data
    data['game'] = user_message
    # ----SAVED!
    keyboard_games = [['Команду', 'Сокомадника']]
    reply_markup = ReplyKeyboardMarkup(keyboard_games, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Кого ищешь ?", reply_markup=reply_markup)

    return ASK_COOP


async def _coop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_games = [['Команду', 'Сокомадника']]

    user_message = update.message.text

    if user_message not in keyboard_games[0]:
        return ASK_COOP

    data = context.user_data
    data['coop'] = user_message
    # ----SAVED!
    await update.message.reply_text("Сколько часов в твоей игре ?")

    return ASK_HOURS


async def _hours(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if not user_message.isdigit():
        return ASK_HOURS

    data = context.user_data
    data['hours'] = user_message
    # ----SAVED!

    await update.message.reply_text("Расскажи о себе и кого хочешь найти. Это поможет лучше подобрать тебе компанию.",
                                    reply_markup=ReplyKeyboardRemove())

    return ASK_DESC


async def _description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    data = context.user_data
    data['desc'] = user_message

    with open('user_data.txt', 'a') as file:
        file.write(
            '\n' + f'''{data['game']}, {data['name']}, {data['coop']}, {data['hours']}, {data['desc']}, {data['user_id']}''')

    # ----SAVED!
    sql = """
        INSERT INTO profile (game, name, st, hours, description, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cur.execute(sql, (
        data['game'],
        data['name'],
        data['coop'],
        data['hours'],
        data['desc'],
        data['user_id']
    ))
    con.commit()
    con.close()
    await update.message.reply_text('⌞ Ваша анкета была сохранена, можем начать поиск людей. (/view) ⌝')

    return ConversationHandler.END


# ---------------- Handle ----------------

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text_received: str = update.message.text
    await update.message.reply_text("-о-", )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    data.clear()
    await update.message.reply_text("Анкета была отменена.")
    return ConversationHandler.END


async def stop_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Подождем пока кто-то увидит твою анкету", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# ---------------- Main functions ----------------


def main() -> None:
    app = Application.builder().token(TOKEN).build()

    # Connecting commands...
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler('stop', stop))

    # Init scenarios...

    search_people = ConversationHandler(
        entry_points=[CommandHandler('view', view)],
        states={
            SEARCH: [MessageHandler(filters.ALL, _work)],
        },
        fallbacks=[CommandHandler('s', stop_search)]
    )

    make_profile = ConversationHandler(
        entry_points=[CommandHandler('new', new)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, _name)],

            ASK_GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, _game)],

            ASK_COOP: [MessageHandler(filters.TEXT & ~filters.COMMAND, _coop)],

            ASK_HOURS: [MessageHandler(filters.TEXT & ~filters.COMMAND, _hours)],

            ASK_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, _description)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(search_people)
    app.add_handler(make_profile)

    # Connecting messages...
    # app.add_handler(MessageHandler(filters.TEXT, handle_text_message)) - Этот обработчик реагирует на пользовательские сообщения, создан чисто для тестов

    # |Starting|
    app.run_polling()
