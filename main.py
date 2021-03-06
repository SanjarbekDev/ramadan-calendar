from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw

from telegram import *
from telegram.ext import *

from conf import TOKEN, DB_NAME
from db_helper import DBHelper

BTN_TODAY, BTN_TOMORROW, BTN_MONTH, BTN_REGION, BTN_DUA = (
    'βοΈ Bgun', 'β³ Erta',"π To'liq taqvim", 'πΊπΏ Mintaqalar', 'π€² Duo')
main_buttons = ReplyKeyboardMarkup([
    [BTN_TODAY], [BTN_TOMORROW, BTN_MONTH], [BTN_REGION], [BTN_DUA]
], resize_keyboard=True)

STATE_REGION = 1
STATE_CALENDAR = 2

user_region = dict()
db = DBHelper(DB_NAME)


def region_buttons():
    regions = db.get_regions()
    buttons = []
    tmp_b = []
    for region in regions:
        tmp_b.append(InlineKeyboardButton(region['name'], callback_data=region['id']))
        if len(tmp_b) == 2:
            buttons.append(tmp_b)
            tmp_b = []
    return buttons


def start(update, context):
    user = update.message.from_user
    user_region[user.id] = None
    buttons = region_buttons()

    update.message.reply_html(
        'π€ Assalomu aleykum <b>{}!</b>\n \n<b>Ramazon oyi muborak bo\'sin π</b>\n \nSizga qaysi mintaqa bo\'yicha malumot kerak βοΈ'.
            format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons))

    return STATE_REGION


def inline_callback(update, context):
    try:
        query = update.callback_query
        user_id = query.from_user.id
        user_region[user_id] = int(query.data)
        query.message.delete()
        query.message.reply_html(text='<b>ππ Ramazon taqvimi</b> 2οΈβ£0οΈβ£2οΈβ£1οΈβ£\n \nQuyidagilardan birini tanlang π',
                                 reply_markup=main_buttons)

        return STATE_CALENDAR
    except Exception as e:
        print('error ', str(e))
        
def calendar_today(update, context):
    try:
        my_image = Image.open("images/image_temp.jpg")
        title_font = ImageFont.truetype('Mulish_wght.ttf', 20)
        title_text = "Bgun {}\n       @http_master".format(str(datetime.now().date()))
        image_editable = ImageDraw.Draw(my_image)
        image_editable.text((400,15), title_text, (237, 230, 211), font=title_font)
        my_image.save('images/img.jpg')
        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return STATE_REGION
        region_id = user_region[user_id]
        region = db.get_region(region_id)
        today = str(datetime.now().date())
        calendar = db.get_calendar_by_region(region_id, today)
        photo_path = 'images/img.jpg'
        message = '<b>Ramazon</b> 2021\n<b>{}</b> vaqti\n \nSaharlik: <b>{}</b>\nIftorlik: <b>{}</b>'.format(
            region['name'], calendar['fajr'][:5], calendar['maghrib'][:5])

        update.message.reply_photo(photo=open(photo_path, 'rb'), caption=message, parse_mode='HTML',
                                   reply_markup=main_buttons)
    except Exception as e:
        print('Error ', str(e))


def calendar_tomorrow(update, context):
    try:
        my_image = Image.open("images/image_temp.jpg")
        title_font = ImageFont.truetype('Mulish_wght.ttf', 20)
        title_text = "Ertaga {}\n          @http_master".format( str(datetime.now().date() + timedelta(days=1)))
        image_editable = ImageDraw.Draw(my_image)
        image_editable.text((400,15), title_text, (237, 230, 211), font=title_font)
        my_image.save('images/img.jpg')
        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return STATE_REGION
        region_id = user_region[user_id]
        region = db.get_region(region_id)
        dt = str(datetime.now().date() + timedelta(days=1))

        calendar = db.get_calendar_by_region(region_id, dt)
        photo_path = 'images/img.jpg'
        message = '<b>Ramazon</b> 2021\n<b>{}</b> vaqti\n \nSaharlik: <b>{}</b>\nIftorlik: <b>{}</b>'.format(
            region['name'], calendar['fajr'][:5], calendar['maghrib'][:5])

        update.message.reply_photo(photo=open(photo_path, 'rb'), caption=message, parse_mode='HTML',
                                   reply_markup=main_buttons)
    except Exception as e:
        print('Error ', str(e))


def calendar_month(update, context):
    
    user_id = update.message.from_user.id
    if not user_region[user_id]:
        return STATE_REGION
    region_id = user_region[user_id]
    region = db.get_region(region_id)
    photo_path = 'images/table/region_{}.jpg'.format(region['id'])
    message = '<b>Ramazon</b> 2021\n<b>{}</b> Vaqti'.format(region['name'])
    update.message.reply_photo(photo=open(photo_path, 'rb'), caption=message, parse_mode='HTML',
                                   reply_markup=main_buttons)
    


def select_region(update, context):
    buttons = region_buttons()
    update.message.reply_text('π’ππ‘Sizga qaysi mintaqa malumoti kerak ?',
                              reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_REGION


def select_dua(update, context):
    my_image = Image.open("images/dua_temp.jpg")
    title_font = ImageFont.truetype('OrelegaOne-Regular.ttf', 55)
    title_text = "Saharlik (og'iz yopish) duosi:\nNavaytu an asuma sovma shaxri Ramazona \nminal fajri ilal mag'ribi,   xolisan lillaxi ta'la.\n \n \nIftorlik (Og'iz ochish) duosi:\nAlloxumma laka sumtu va bika amantu va \na'alayka tavakkaltu va aala rizkika aftartu, \nfag'firli, ya Gofforu, ma qoddamtu vama axxortu."
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((30,100), title_text, (237, 230, 211), font=title_font)
    my_image.save('images/img_dua.jpg')
    saharlik = "<b>Π‘Π°?³Π°ΡΠ»ΠΈΠΊ (ΠΎ?ΠΈΠ· ΡΠΏΠΈΡ) Π΄ΡΠΎΡΠΈ:</b>\nΠΠ°Π²Π°ΠΉΡΡ Π°Π½ Π°ΡΡΠΌΠ° ΡΠΎΠ²ΠΌΠ° ΡΠ°?³ΡΠΈ Π Π°ΠΌΠ°Π·ΠΎΠ½Π° ΠΌΠΈΠ½Π°Π» ΡΠ°ΠΆΡΠΈ ΠΈΠ»Π°Π» ΠΌΠ°?ΡΠΈΠ±ΠΈ, ΡΠΎΠ»ΠΈΡΠ°Π½ Π»ΠΈΠ»Π»Π°?³ΠΈ ΡΠ°ΡΠ°Π»Π°."
    iftorlik = "<b>ΠΡΡΠΎΡΠ»ΠΈΠΊ (ΠΎ?ΠΈΠ· ΠΎΡΠΈΡ) Π΄ΡΠΎΡΠΈ:</b>\nΠΠ»Π»ΠΎ?³ΡΠΌΠΌΠ° Π»Π°ΠΊΠ° ΡΡΠΌΡΡ Π²Π° Π±ΠΈΠΊΠ° Π°ΠΌΠ°Π½ΡΡ Π²Π° Π°ΡΠ°Π»Π°ΠΉΠΊΠ° ΡΠ°Π²Π°ΠΊΠΊΠ°Π»ΡΡ Π²Π° ΡΠ°Π»Π° ΡΠΈΠ·?ΠΈΠΊΠ° Π°ΡΡΠ°ΡΡΡ, ΡΠ°?ΡΠΈΡΠ»ΠΈ, ΠΉΠ° ?ΠΎΡΡΠ°ΡΡ, ΠΌΠ° ?ΠΎΠ΄Π΄Π°ΠΌΡΡ Π²Π°ΠΌΠ° Π°ΡΡΠΎΡΡΡ."
    update.message.reply_photo(photo=open('images/img_dua.jpg', 'rb'),
                               caption="{}\n \n{}".format(saharlik, iftorlik), parse_mode='HTML',
                               reply_markup=main_buttons)


def main():
    # Updater o`rnatib olamiz
    updater = Updater(TOKEN, use_context=True)

    # Dispatcher eventlarni aniqlash uchun
    dispatcher = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_REGION: [
                CallbackQueryHandler(inline_callback),
                MessageHandler(Filters.regex('^(' + BTN_TODAY + ')$'), calendar_today),
                MessageHandler(Filters.regex('^(' + BTN_TOMORROW + ')$'), calendar_tomorrow),
                MessageHandler(Filters.regex('^(' + BTN_MONTH + ')$'), calendar_month),
                MessageHandler(Filters.regex('^(' + BTN_REGION + ')$'), select_region),
                MessageHandler(Filters.regex('^(' + BTN_DUA + ')$'), select_dua)

            ],
            STATE_CALENDAR: [
                MessageHandler(Filters.regex(BTN_TODAY), calendar_today),
                MessageHandler(Filters.regex(BTN_TOMORROW), calendar_tomorrow),
                MessageHandler(Filters.regex(BTN_MONTH), calendar_month),
                MessageHandler(Filters.regex(BTN_REGION), select_region),
                MessageHandler(Filters.regex(BTN_DUA), select_dua)
            ],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()