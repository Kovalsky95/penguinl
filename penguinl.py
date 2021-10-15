from telegram import Update;
from telegram import KeyboardButton;
from telegram import ReplyKeyboardMarkup;
from telegram import InlineKeyboardButton;
from telegram import InlineKeyboardMarkup;
from telegram.ext import Updater;
from telegram.ext import CallbackContext;
from telegram.ext import CommandHandler;
from telegram.ext import MessageHandler;
from telegram.ext import CallbackQueryHandler;
from telegram.ext import Filters;


import calculate as calc;
import os, apiai, json, time;

from config import P_Bot;

class App():
    def hola_user(app, update: Update, context: CallbackContext):
        if app.p_inf.search_person(update.message.chat_id) == 0:
            app.p_inf.add_person(update.message.chat_id);
            content = "Приветствую!!";
            app.send_answer(
                update,
                context,
                app.p_inf.get_admin_id(),
                "кто-то пришёл: {0:n} сюда: {1:n}".format(update.message.chat_id, update.message.chat_id),
                "markdown"
            );
        else:
            content = "Мы уже с Вами знакомы, день добрый!!";
        context.bot.delete_message(update.message.chat_id, update.message.message_id);
        app.send_answer(
            update,
            context,
            update.message.chat_id,
            content,
            "markdown"
        );
    #
    def help_user(app, update: Update, context: CallbackContext):
        pass;
    #
    def la_calculadora(app, update: Update, context: CallbackContext):
        c = app.c;
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("1", callback_data=1),
                    InlineKeyboardButton("2", callback_data=2),
                    InlineKeyboardButton("3", callback_data=3),
                    InlineKeyboardButton("4", callback_data=4)],
            [InlineKeyboardButton("5", callback_data=5),
                    InlineKeyboardButton("6", callback_data=6),
                    InlineKeyboardButton("7", callback_data=7),
                    InlineKeyboardButton("8", callback_data=8)],
            [InlineKeyboardButton("9", callback_data=9),
                    InlineKeyboardButton("0", callback_data=0),
                    InlineKeyboardButton(".", callback_data="."),
                    InlineKeyboardButton("bin", callback_data="0b"),
                    InlineKeyboardButton("oct", callback_data="0o"),
                    InlineKeyboardButton("hex", callback_data="0x")],
             [InlineKeyboardButton("+", callback_data='+'),
                    InlineKeyboardButton("-", callback_data='-'),
                    InlineKeyboardButton("*", callback_data='*'),
                    InlineKeyboardButton("/", callback_data='/'),
                    InlineKeyboardButton("%", callback_data='%')],
             [InlineKeyboardButton("=", callback_data='=')]]
        );

        update.message.reply_text('Please choose:', reply_markup=reply_markup);
        context.bot.delete_message(update.message.chat_id, update.message.message_id);
    def calc_b(app, update: Update, context: CallbackContext):
        c = app.c;
        query = update.callback_query;
        try:
            if query.data.find(".") != -1:
                app.f_flag = True;
                if len(c.num) == 1:
                    c.num[0] = float(c.num[0]);
                elif len(c.num) == 3:
                    c.num[2] = float(c.num[2]);
            elif app.f_flag:
                if len(c.num) == 1:
                    c.num[0] = float(
                        str(c.num[0]).replace(".0", ".") + query.data
                        if
                            str(c.num[0]).find(".0") != -1
                        else
                            str(c.num[0])+ query.data
                    );
                elif len(c.num) == 3:
                    c.num[2] = float(
                        str(c.num[2]).replace(".0", ".") + query.data
                        if
                            str(c.num[2]).find(".0") != -1
                        else
                            str(c.num[2])+ query.data
                    );
            else:
                c.num.append(int(query.data));
                if len(c.num) == 2:
                    c.num[0] = int(str(c.num[0]) + query.data);
                    c.num.remove(c.num[1]);
                elif len(c.num) > 3:
                    c.num[2] = int(str(c.num[2]) + query.data);
                    c.num.remove(c.num[3]);
        except:
            app.f_flag = False;
            c.num.append(query.data);
        if query.data == '=':
            res = 0;
            a = c.num[0];
            act = c.num[1];
            b = c.num[2];

            res = c.do_act[act](a, b);
            c.num = [];
            query.edit_message_text(res, timeout = 25);
            app.f_flag = False;
            context.bot.delete_message(query.message.chat_id, query.message.message_id, timeout = 25);
    #
    def cr_unplan(app, update: Update, context: CallbackContext):
        tmp = update.message.text.replace("/crearplan ", "").split(" ");
        app.p_inf.crear_unplan(update.message.chat_id, tmp);
        context.bot.delete_message(update.message.chat_id, update.message.message_id);
    def el_minutero(app, update: Update, context: CallbackContext):
        tmp = update.message.text.replace("/el_minutero ", "").split("\n");
        app.p_inf.estab_unplan(update.message.chat_id, tmp);
        context.bot.delete_message(update.message.chat_id, update.message.message_id);
    def show_all_in(app, update: Update, context: CallbackContext):
        tmp = update.message.text.replace("/show_all_in ", "");
        try:
            context.bot.delete_message(update.message.chat_id, update.message.message_id-2);
            context.bot.delete_message(update.message.chat_id, update.message.message_id-1);
        except:
            pass;
        context.bot.delete_message(update.message.chat_id, update.message.message_id);
        app.send_answer(
            update,
            context,
            update.message.chat_id,
            app.p_inf.get_from(update.message.chat_id, tmp),
            "html"
        );
        time.sleep(25);
        context.bot.delete_message(update.message.chat_id, update.message.message_id+1);
    def yt_down(app, update: Update, context: CallbackContext):
        link = update.message.text.replace("/yt_down ", "");
        
        from pytube import YouTube;
        #YouTube(tmp).streams.first().download();
        yt = YouTube(link);
        
        tmp = yt.streams.filter(
            progressive=True,
            file_extension='mp4'
            ).order_by('resolution').desc().first().default_filename;
        
        try:
            context.bot.delete_message(update.message.chat_id, update.message.message_id);
            
            app.send_answer(
                update,
                context,
                update.message.chat_id,
                'down init: {0:}'.format(tmp),
                "html"
            );
        except:
            pass;
        
        yt.streams.filter(
            progressive=True,
            file_extension='mp4'
            ).order_by('resolution').desc().first().download();
        
#        app.edit_answer(
#            update,
#            context,
#            update.message.chat_id,
#            update.message.message_id+1,
#            'down completed: {0:}\njst send..'.format(tmp),
#            "html"
#        );
        context.bot.delete_message(update.message.chat_id, update.message.message_id+1);
        app.send_answer(
            update,
            context,
            update.message.chat_id,
            'down completed: {0:}\njst send..'.format(tmp),
            "html"
        );
        
#        app.edit_media(
#            update,
#            context,
#            update.message.chat_id,
#            update.message.message_id+1,
#            tmp
#        );
        context.bot.delete_message(update.message.chat_id, update.message.message_id+2);
        app.send_video(
            update,
            context,
            update.message.chat_id,
            tmp
        );
    #
    def answer_user(app, update: Update, context: CallbackContext):
#        req = apiai.ApiAI(app.p_inf.get_dtoken()).text_request();
#        req.lang = "ru";
#        req.session_id = "PenguinL";
#        req.query = update.message.text;
#
#        res = json.loads(req.getresponse().read().decode("utf-8"));
#        res = res["result"]["fulfillment"]["speech"];
        res = False
        if res:
            app.send_answer(
                update,
                context,
                update.message.chat_id,
                res,
                "html"
            );
        else:
            app.send_answer(
                update,
                context,
                update.message.chat_id,
                "Рад Вашему слову.",
                "html"
            );
    #
    def send_answer(app, update, context, chat_id, text, p_m):
        if app.p_inf.search_person(update.message.chat_id) != 0:
            l_event = app.p_inf.sub_show_plan(chat_id);
            context.bot.send_message(
                chat_id = chat_id,
                text = "*"+text+"*" if p_m == "markdown" else "<em>"+text+"</em>",
                parse_mode = p_m,
                timeout = 25,
                reply_markup = ReplyKeyboardMarkup([
                    list(
                        (KeyboardButton("/show_all_in {0:s}".format(q)) for q in l_event)
                        if len(l_event) != 0
                        else [(KeyboardButton("Эй!"))]
                )],
                resize_keyboard=True, one_time_keyboard=True, selective=True)
            );
        else:
            context.bot.delete_message(update.message.chat_id, update.message.message_id);
            text = "Вы не зарегистрированы в системе."+\
                   "Используйте /start для того, чтобы начать наше продуктивное общение.";
            p_m = "html"
            context.bot.send_message(
                chat_id = chat_id,
                text = "*"+text+"*" if p_m == "markdown" else "<em>"+text+"</em>",
                parse_mode = p_m,
                timeout = 25
            );
            context.bot.delete_message(update.message.chat_id, update.message.message_id+1, timeout = 25);
    def edit_answer(app, update, context, chat_id, message_id, text, p_m):
#             contex.bot.edit_message_text(chat_id=message.chat_id,
#                   message_id=message.message_id,
#                   *args,
#                   **kwargs)
            context.bot.edit_message_text(
                chat_id = chat_id,
                message_id = message_id,
                text = "*"+text+"*" if p_m == "markdown" else "<em>"+text+"</em>",
                parse_mode = p_m,
                timeout = 25
            );
    def edit_media(app, update, context, chat_id, message_id, m_media):
#             contex.bot.edit_message_media(chat_id=message.chat_id,
#                    message_id=message.message_id,
#                    *args,
#                    **kwargs)
            from telegram import InputMediaVideo;
            context.bot.edit_message_media(
                chat_id = chat_id,
                message_id = message_id,
                timeout = 25,
                media = InputMediaVideo(media = m_media)
            );
    def send_video(app, update, context, chat_id, vd):
            context.bot.send_video(
                chat_id = chat_id,
                timeout = 25,
                video = open(vd, 'rb'),
                supports_streaming=True
            );
            if os.path.exists(vd):
                os.remove(vd);
    #
    def __init__(app):
        app.commande_handler = [];
        app.p_inf = P_Bot();
        app.updater = Updater(
            token = app.p_inf.get_token(),
            base_url = app.p_inf.get_base_url(),
            use_context = True
        );

        app.c = calc.Calculate();
        app.f_flag = True;

        app.commande_handler.append(CommandHandler("start", app.hola_user));
        app.commande_handler.append(CommandHandler("la_comienzo", app.hola_user));
        app.commande_handler.append(CommandHandler("la_calculadora", app.la_calculadora));
        app.commande_handler.append(CommandHandler("crearplan", app.cr_unplan));
        app.commande_handler.append(CommandHandler("el_minutero", app.el_minutero));
        app.commande_handler.append(CommandHandler("show_all_in", app.show_all_in));
        app.commande_handler.append(CommandHandler("yt_down", app.yt_down));
        app.commande_handler.append(MessageHandler(Filters.text, app.answer_user));
        app.commande_handler.append(CallbackQueryHandler(app.calc_b));
        
        for el in app.commande_handler:
            app.updater.dispatcher.add_handler(el);
        app.app_run();
    def app_run(app):
        if app.f_flag:
            app.updater.start_polling();
        else:
            # add handlers
            app.updater.start_webhook(
                listen = "0.0.0.0",
                port = int(os.environ.get('PORT', '8443')),
                url_path = app.p_inf.get_token(),
                webhook_url = "https://penguinl.herokuapp.com/" + app.p_inf.get_token()
                #url_path = app.p_inf.get_token()
            );
            #app.updater.bot.set_webhook("https://penguinl.herokuapp.com/" + app.p_inf.get_token());

        app.updater.idle();
if __name__ == "__main__":
    App();
