from telegram.ext import CommandHandler, Updater, MessageHandler, Filters  # import modules
from telegram import Update, Bot
from multiprocessing import Process
from sentry import *

my_token = '1880353936:AAE6gygO6mq3rj-dVNzzE8Q-sP1D6YcBAxg'
kDuration = 1
kPeriod = 12

print('start telegram chat bot')

def startwithVal(duration, period, update, context):
    text = str(period)+"시간 주기로 "+str(duration)+"시간 동안 깨어있음"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    global subprocess
    subprocess = Process(target=SentryRoutine, args=(duration, period))
    subprocess.start()

# message reply function
def start(update, context):
    startwithVal(kDuration, kPeriod, update, context)

def setup (update, context):
    duration = int(context.args[0])
    period = int(context.args[1])
    startwithVal(duration, period, update, context)

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="중단시작.")
    subprocess.kill()
    context.bot.send_message(chat_id=update.effective_chat.id, text="중단완료.")

def status(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="확인중")
    text = getStatus()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    if subprocess.is_alive():
        context.bot.send_message(chat_id=update.effective_chat.id, text="작동중")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="작동없음")
updater = Updater(my_token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('setup', setup, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('status', status, pass_args=True))

updater.start_polling()
updater.idle()
