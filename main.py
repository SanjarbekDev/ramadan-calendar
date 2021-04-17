from telegram import InlineKeyboardButton, InlineKeyboardMarkup , ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)

BTN_TODAY, BTN_TOMORROW, BTN_MONTH, BTN_REGION, BTN_DUA = ('Bugun', 'Ertaga', 'To\'liq taqvim', 'Mintaqa', 'Duo')

main_buttons = ReplyKeyboardMarkup([
    [BTN_TODAY], [BTN_TOMORROW,  BTN_MONTH], [BTN_REGION], [BTN_DUA]
], resize_keyboard=True)

STATE_REGION = 1
STATE_CALENDAR = 2
    
def start(update, context):
    buttons =[
        [
            InlineKeyboardButton('TOSHKENT', callback_data= 'region-1'),
            InlineKeyboardButton('ANDIJON', callback_data= 'region-2')
        ]
    ]
    user = update.message.from_user
    update.message.reply_html('Assalomu aleykum <b>{}\n \n</b><b>   Ramazon oyi muborak bo\'lsin😊😊</b>\n🏢 Sizga qaysi mintaqa uchun malumot kerak?'.format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons))
    
    return STATE_REGION

def inline_callback(update, context):
    try:
        query = update.callback_query
        query.message.delete()
        query.message.reply_html('<b>Ramazon taqvimi</b>2️⃣0️⃣2️⃣1️⃣\n Quyidagilarni tanlang 👇',reply_markup=main_buttons)
        
        return STATE_CALENDAR
    
    except Exception as e:
        print('error', str(e))

def calendar_today(update , context):
    update.message.reply_text('BUGUN TANLANDI')
    
def calendar_tomorrow(update , context):
    update.message.reply_text('ERTANGI KUN TANLANDI')
    
def calendar_month(update , context):
    update.message.reply_text('TO\'LIQ TAQVIM TANLANDI')
    
def select_region(update , context):
    update.message.reply_text('REGION TANLASH')
    
def select_dua(update , context):
    update.message.reply_text('DUA TANLANDI')
    
def main():
    # Updatrni o'rnatamiz
    updater = Updater('1750900541:AAENQhwMy2ThSm9c_qk8_KQe5cwLZRnp_p0', use_context = True)

    #Dispatcher eventlaini aniqlash
    dispatcher = updater.dispatcher

    #start komandasini tutish
    #dispatcher.add_handler(CommandHandler('start', start))
    
    # inline buutton query 
    dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    
    #conversation plagins
    conv_handler = ConversationHandler(
         entry_points = [CommandHandler('start', start)],
         
         states={
                 STATE_REGION: [CallbackQueryHandler(inline_callback)],
                 STATE_CALENDAR: [
                    MessageHandler(Filters.regex('^('+BTN_TODAY+')$',calendar_today)),
                    MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$',calendar_tomorrow)),
                    MessageHandler(Filters.regex('^('+BTN_MONTH+')$',calendar_month)),
                    MessageHandler(Filters.regex('^('+BTN_REGION+')$',select_region)),
                    MessageHandler(Filters.regex('^('+BTN_DUA+')$',select_dua))
            ],
        },
         fallbacks = [CommandHandler('start', start)]
    )
    
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

main()
