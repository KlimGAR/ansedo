import logging

from telegram.ext import Application, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"<b>Привет {user.mention_html()}! Я бот, который поможет найти команду или сокомадника.Для начала ознакомьтесь с командами ( /help ).</b>",
    )


async def help_command(update, context) -> None:
    await update.message.reply_html("<b>🠖</b> /new - <i>создать или обновить свою анкету</i>\n"
                                    "<b>🠖</b> /view - <i>перейти к поиску</i>\n"
                                    "<b>🠖</b> /stop - <i>отключить свою анкету и завершить работу бота</i>\n"
                                    )


async def new(update, context) -> None:
    await update.message.reply_text("soon..")


async def view(update, context) -> None:
    await update.message.reply_text("soon..")


async def stop(update, context) -> None:
    await update.message.reply_text("soon..")


def main() -> None:
    application = Application.builder().token('6693149081:AAEoLL-E4KTBBPMrccPoa_vysJeZVi4unVg').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("new", new))
    application.add_handler(CommandHandler("view", view))
    application.add_handler(CommandHandler("stop", stop))
    application.run_polling()
