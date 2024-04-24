import logging

from telegram import ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
TOKEN = '6693149081:AAEoLL-E4KTBBPMrccPoa_vysJeZVi4unVg'
TAG_BOT = '@Ansedo_Bot'
ASK_NAME, ASK_GAME, ASK_COOP, ASK_HOURS, ASK_DESC = range(1, 6)


# ---------------- Commands ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"<b>Привет {user.mention_html()}! Я бот, который поможет найти команду или сокомадника."
        f" Cначала ознакомьтесь с командами ( /help ).</b>",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html("<b>🠖</b> /new - <i>создать или обновить свою анкету</i>\n"
                                    "<b>🠖</b> /view - <i>перейти к поиску</i>\n"
                                    "<b>🠖</b> /stop - <i>!редакнуть!</i>\n"
                                    )


async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("soon..")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("soon..")


async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как мне тебя называть ?")
    return ASK_GAME


# --- Profile ---


async def _game(update, context):
    keyboard_games = [['CS2', 'Dota 2',
                       'Pubg', 'Roblox'], ['Fortnite', 'Valorant',
                                           'Minecraft', 'Terarria']]
    reply_markup = ReplyKeyboardMarkup(keyboard_games, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("По какой игре ?", reply_markup=reply_markup)
    return ASK_COOP


async def _coop(update, context):
    keyboard_games = [['Команду', 'Сокомадника']]
    reply_markup = ReplyKeyboardMarkup(keyboard_games, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Кого ищешь ?", reply_markup=reply_markup)
    return ASK_HOURS


async def _hours(update, context):
    await update.message.reply_text("Сколько часов в твоей игре ?")
    return ASK_DESC


async def _description(update, context):
    await update.message.reply_text("Расскажи о себе и кого хочешь найти. Это поможет лучше подобрать тебе компанию.",
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# ---------------- Handle ----------------

async def handle_text_message(update, context):
    message_type: str = update.message.chat.type
    text_received: str = update.message.text

    # user_data = context.user_data
    # if


async def cancel(update, context):
    update.message.reply_text("Диалог отменен.")
    return ConversationHandler.END


# ---------------- Main functions ----------------


def main() -> None:
    app = Application.builder().token(TOKEN).build()

    # Connecting commands...
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('view', view))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', new)],
        states={
            ASK_GAME: [MessageHandler(~filters.ALL, _game)],

            ASK_COOP: [MessageHandler(~filters.ALL, _coop)],

            ASK_HOURS: [MessageHandler(filters.TEXT & ~filters.COMMAND, _hours)],

            ASK_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, _description)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conv_handler)

    # Hundle messages...

    app.add_handler(MessageHandler(filters.TEXT, handle_text_message))

    app.run_polling()