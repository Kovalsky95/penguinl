from time import sleep;
from telegram import Bot;
from telegram import Update;
from telegram.ext import Updater;
from telegram.ext import CommandHandler;
from telegram.ext import MessageHandler;
from telegram.ext import Filters;

from config import P_Bot;

command_handler = p_bot = p_inf = updater = null;
def hola_user(p_bot: Bot, update: Update):
    p_bot.send_message(
        chat_id=update.message.chat_id,
        text="hola"
    );
def answer_user(p_bot: Bot, update: Update):
    p_bot.send_message(
        chat_id=update.message.chat_id,
        text="answer"
    );
class App():
    global command_handler, p_bot, p_inf, updater;
    def __init__(app):
        commande_handler = [];
        p_bot = Bot(
            token=p_inf.get_token(),
            base_url=p_inf.get_base_url()
        );
        p_inf = P_Bot();
        updater = Updater(bot=p_bot);

        commande_handler.append(CommandHandler("start", hola_user));
        commande_handler.append(MessageHandler(Filters.text, answer_user));
        
        for el in commande_handler:
            updater.dispatcher.add_handler(el);
    def app_run(app):
        p_bot.send_message(
            chat_id=p_inf.get_admin(),
            text="worked."
        );
        updater.start_polling();

if(__name__ == "__main__"):
    app = App();
    while(True):
        app.app_run();
        sleep(120);#600);#11400);
