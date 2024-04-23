import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ContextTypes, Application, ConversationHandler, CommandHandler, MessageHandler, \
    CallbackQueryHandler

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
        f'<b>Привет {user.mention_html()}! Я бот, который поможет найти команду или сокомадника. Cначала ознакомьтесь с командами ( /help ).</b>')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("soon..")


async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("soon..")


async def new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    games: list[list[InlineKeyboardButton]] = [
        [
         InlineKeyboardButton("CS2", callback_data=1),
         InlineKeyboardButton("Dota 2", callback_data=2),
         InlineKeyboardButton("Pubg", callback_data=3),
         InlineKeyboardButton("Roblox", callback_data=4)
        ],
        [
            InlineKeyboardButton("Fortnite", callback_data=5),
            InlineKeyboardButton("Valorant", callback_data=6),
            InlineKeyboardButton("Minecraft", callback_data=7),
            InlineKeyboardButton("Terarria", callback_data=8)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(games)
    await update.message.reply_text("По какой игре ?", reply_markup=reply_markup)
    return ASK_COOP


# --- Profile ---

async def _game(update, context):
    games = [
        [
            InlineKeyboardButton("CS2", callback_data=1),
            InlineKeyboardButton("Dota 2", callback_data=2),
            InlineKeyboardButton("Pubg", callback_data=3),
            InlineKeyboardButton("Roblox", callback_data=4)
        ],
        [
            InlineKeyboardButton("Fortnite", callback_data=5),
            InlineKeyboardButton("Valorant", callback_data=6),
            InlineKeyboardButton("Minecraft", callback_data=7),
            InlineKeyboardButton("Terarria", callback_data=8)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(games)
    await update.message.reply_text("По какой игре ?", reply_markup=reply_markup)
    query = update.callback_query
    query.answer()
    return ASK_COOP


async def _coop(update, context):
    r_coop = [InlineKeyboardButton('Сокомадника', callback_data='solo'),
              InlineKeyboardButton('Команду', callback_data='team')]
    markup = InlineKeyboardMarkup([r_coop])
    await update.message.reply_text("Кого ищешь ?", reply_markup=markup)
    return ASK_HOURS


async def _hours(update, context):
    await update.message.reply_text("Сколько часов в твоей игре ?")
    return ASK_DESC


async def _description(update, context):
    await update.message.reply_text("Расскажи о себе и кого хочешь найти. Это поможет лучше подобрать тебе компанию.")
    return ConversationHandler.END


async def cancel(update, context):
    update.message.reply_text("Диалог отменен.")
    return ConversationHandler.END


# ---------------- Responses ----------------

# def hundle_response(text: str):
#     pass


# Обработчик коллбэк-запросов после ASK_COOP
async def handle_callback(update, context):
    query = update.callback_query
    chosen_game = query.data

    # Сохраняем выбор пользователя или выполняем другую логику, если это необходимо
    user_data = context.user_data
    user_data['chosen_game'] = chosen_game
    await query.edit_message_text('Игра была добавлена.')
    # Продолжаем диалог или переходим к следующему шагу
    # В зависимости от логики вашего приложения


def main():
    app = Application.builder().token(TOKEN).build()

    # Connecting commands...
    app.add_handler('start', start)
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler('stop', stop)
    app.add_handler('view', view)

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

    # Connecting messages...

    # Connecting callback...
    app.add_handler(CallbackQueryHandler(handle_callback))