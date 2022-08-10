import pygsheets
import telebot
import pytz
from telebot import types
from datetime import datetime

# video tutorial google sheet = https://www.youtube.com/watch?v=anqwLrVPBYg
# pygsheets
service_file = r'autobot-357606-2c6c0d27a1b7.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'NexLogicIn'
sh = gc.open(sheetname)
wks = sh.worksheet_by_title('test')
wksusers = sh.worksheet_by_title('users')


API_TOKEN = '5350033732:AAFPDf3iJYQyveTMhOL9z_hJGLwoRuEwen8'
bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
print(" Start Up...")

class User:
    def __init__(self, name):
        self.timein = name
        self.timeout = None


@bot.message_handler(commands=['start'])
def process_start(message):
    msg = bot.reply_to(message, "NexLogic Internship Timelog.\n")

@bot.message_handler(commands=['help'])
def process_help(message):
    msg = bot.reply_to(message, """
Available commands: 
Use /timein
Use /timeout
Use /timecheck
""")

@bot.message_handler(commands=['timein'])   
def process_timein(message):
    username = message.chat.username
    finduser = wksusers.find(username)
    numfound = int(len(finduser))
    if numfound >= 1:
        try:
            now = datetime.now(pytz.timezone('Asia/Manila'))
            date_time = now.strftime("%H:%M:%S")
            time = now.strftime("%H:%M:%S")
            date = now.strftime('%m/%d/%Y')
            chat_id = message.chat.id
            timein = message.text

            user = User(timein)
            user_dict[chat_id] = user
            user.timein = date_time
            
            if timein == "/timein":
                user_first_name = str(message.chat.first_name)
                user_last_name = str(message.chat.last_name)
                full_name = user_first_name + " "+ user_last_name
                sheet_data = wks.get_all_records()
                num = 2
                for i in range(len(sheet_data)):
                    num+=1
                    if full_name == sheet_data[i].get("Name") and date == sheet_data[i].get("Date"):
                        bot.reply_to(message, f'Already logged for the day')
                        break
                else:
                    wks.update_value((num, 1), full_name)
                    wks.update_value((num, 2), date)
                    wks.update_value((num, 3), time)
                    # NexLogicIn = []
                    # NexLogicIn.append(str(full_name))
                    # NexLogicIn.append(str(date))
                    # NexLogicIn.append(str(time))
                    # wks.append_table(NexLogicIn)    
                    bot.reply_to(message, f'Timein on {str(date_time)}')

        except Exception as e:
            bot.reply_to(message, 'Something went wrong. Please try again')
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')
    

@bot.message_handler(commands=['timeout'])  
# Timeout
def process_timeout(message):
    try:
        now2 = datetime.now(pytz.timezone('Asia/Manila'))
        date_time2 = now2.strftime("%H:%M:%S")
        time = now2.strftime("%H:%M:%S")
        timeout = message.text 
        user = User(timeout)
        user.timeout = date_time2
        user_first_name = str(message.chat.first_name)
        user_last_name = str(message.chat.last_name)
        full_name = user_first_name + " "+ user_last_name
        date = now2.strftime('%m/%d/%Y')

        if timeout == "/timeout":
            sheet_data = wks.get_all_records()
            num = 1
            for i in range(len(sheet_data)):
                num += 1
                if full_name == sheet_data[i].get("Name") and date == sheet_data[i].get("Date") and sheet_data[i].get("Timeout")== '':
                    wks.update_value((num,4),time)
                    bot.reply_to(message, f'Successfully timeout on {str(date_time2)}')
                    break
                
                elif full_name == sheet_data[i].get("Name") and date == sheet_data[i].get("Date") and sheet_data[i].get("Timeout")!= '':
                    bot.reply_to(message, 'You already timed out for this day')

    except Exception as e:
        bot.reply_to(message, 'UwU Weong Command')


# TimeCheck
@bot.message_handler(commands=['timecheck'])
def process_timecheck(message):
    username = message.chat.username
    finduser = wksusers.find(username)
    numfound = int(len(finduser))
    if numfound >= 1:
        user_first_name = str(message.chat.first_name) 
        user_last_name = str(message.chat.last_name)
        full_name = user_first_name + " "+ user_last_name
        now = datetime.now(pytz.timezone('Asia/Manila'))
        date = now.strftime('%B %d %Y')
        sheet_data = wks.get_all_records()
        num = 1
        for i in range(len(sheet_data)):
            num += 1
            if full_name == sheet_data[i].get("Name") and date == sheet_data[i].get("Date") and sheet_data[i].get("Timein")!= '' and sheet_data[i].get("Timeout")!= '':
                bot.reply_to(message, f'{date}\nTimein: {sheet_data[i].get("Timein")}\nTimeout: {sheet_data[i].get("Timeout")}')
                break
            elif full_name == sheet_data[i].get("Name") and date == sheet_data[i].get("Date") and sheet_data[i].get("Timein")!= '' and sheet_data[i].get("Timeout")== '':
                bot.reply_to(message, f'{date}\nTimein: {sheet_data[i].get("Timein")}\nTimeout: NONE')
                break
        else:
            bot.reply_to(message, "You haven't timed in yet today")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')
    
        # chat_id = message.chat.id
        # user = user_dict[chat_id]

        # now3 = datetime.now()
        # date_time3 = now3.strftime("%m-%d-%Y")

        # time_1 = datetime.strptime(str(user.timein), '%H:%M:%S')
        # time_2 = datetime.strptime(str(user.timeout), '%H:%M:%S')

        # time_interval = time_2 - time_1
        # # print(time_interval)

        # bot.send_message(chat_id, 'Date:    ' + str(date_time3) + '\nTimein:    ' + str(user.timein) + '\nTimeout:    ' + str(user.timeout) + '\nWorking hours:    ' + str(time_interval))
   

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()

