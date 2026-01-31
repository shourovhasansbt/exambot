import telebot
from telebot import types

# আপনার টেলিগ্রাম বটের API TOKEN এখানে বসান
API_TOKEN = '8374278581:AAGGEXpmuJOy79MClooemHkyhUX5iTCygfk'

bot = telebot.TeleBot(API_TOKEN)

# প্রশ্ন এবং উত্তরের ডেটাবেস (আমি পিডিএফ থেকে প্রথম ৫টি প্রশ্ন স্যাম্পল হিসেবে দিয়েছি)
# আপনি বাকি প্রশ্নগুলো এই ফরম্যাটে নিচে যোগ করে নেবেন।
quiz_data = [
    {
        "question": "১. একটি গাড়ি 7 মিটার ব্যাসার্ধের একটি বৃত্তাকার পথে 44 মিটার ঘুরতে 10 N বল প্রয়োগ করা হলে সম্পন্ন কাজের পরিমাণ কত?",
        "options": ["০ জুল", "4.4 জুল", "10 জুল", "70 জুল"],
        "correct_index": 0  # সঠিক উত্তর: ০ জুল (অপশন ইনডেক্স ০ থেকে শুরু)
    },
    {
        "question": "২. নিচের ম্যাচ বাক্সের কাঠি দিয়ে বাক্সে 3N বলে ঘষা হলো। কাঠিটিকে 4 cm টানা হলে কাঠি ঘষতে কত শক্তি ব্যয় হলো?",
        "options": ["0.12 J", "1.2 J", "1.176 J", "12 J"],
        "correct_index": 0 # সঠিক উত্তর: 0.12 J
    },
    {
        "question": "৩. 25 N বল কোন স্প্রিংকে টেনে 10 cm বৃদ্ধি করে। স্প্রিংকে 6 cm প্রসারিত করতে কত কাজ সম্পন্ন হয়?",
        "options": ["0.45 J", "0.045 J", "0.25 J", "2.5 J"],
        "correct_index": 0 # সঠিক উত্তর: 0.45 J
    },
    {
        "question": "৪. 19.6 kg ভরের একটি বস্তু নির্দিষ্ট উচ্চতায় তুলতে 980 J কাজ করতে হয়। বস্তুটিকে মুক্তভাবে ছেড়ে দিলে কত বেগে ভূমিতে আঘাত করবে?",
        "options": ["5 ms⁻¹", "10 ms⁻¹", "15 ms⁻¹", "20 ms⁻¹"],
        "correct_index": 1 # সঠিক উত্তর: 10 ms⁻¹
    },
    {
        "question": "৫. কোন রাশি যুগলের মাত্রা একই?",
        "options": ["কাজ ও কর্মদক্ষতা", "কাজ ও ক্ষমতা", "কাজ ও শক্তি", "ক্ষমতা ও শক্তি"],
        "correct_index": 2 # সঠিক উত্তর: কাজ ও শক্তি
    }
]

# ইউজারদের প্রগ্রেস ট্র্যাক করার জন্য ডিকশনারি
user_states = {}

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    # গেম রিসেট করা
    user_states[chat_id] = {'current_q': 0, 'score': 0}
    
    markup = types.InlineKeyboardMarkup()
    start_btn = types.InlineKeyboardButton("পরীক্ষা শুরু করুন", callback_data="start_quiz")
    markup.add(start_btn)
    
    bot.send_message(chat_id, "স্বাগতম! ফিজিক্স কুইজ টেস্টে আপনাকে স্বাগতম।\nমোট প্রশ্ন: ৩৫টি\nশুরু করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

# প্রশ্ন পাঠানোর ফাংশন
def send_question(chat_id):
    user_data = user_states.get(chat_id)
    q_index = user_data['current_q']
    
    # যদি সব প্রশ্ন শেষ হয়ে যায়
    if q_index >= len(quiz_data):
        score = user_data['score']
        total = len(quiz_data)
        percentage = (score / total) * 100
        bot.send_message(chat_id, f"✅ পরীক্ষা শেষ!\n\nআপনার স্কোর: {score}/{total}\nপ্রাপ্ত নম্বর: {percentage:.2f}%")
        # স্টেট ক্লিয়ার করা (অপশনাল)
        del user_states[chat_id]
        return

    question_data = quiz_data[q_index]
    question_text = question_data['question']
    options = question_data['options']

    markup = types.InlineKeyboardMarkup()
    
    # অপশন বাটন তৈরি
    for i, option in enumerate(options):
        # callback_data তে অপশনের ইনডেক্স পাঠানো হচ্ছে
        markup.add(types.InlineKeyboardButton(option, callback_data=f"ans_{i}"))

    bot.send_message(chat_id, f"প্রশ্ন {q_index + 1}:\n{question_text}", reply_markup=markup)

# কলব্যাক কোয়েরি হ্যান্ডলার (বাটন ক্লিকের জন্য)
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "start_quiz":
        send_question(chat_id)
        
    elif call.data.startswith("ans_"):
        # ইউজার যদি ইতিমধ্যে সেশন শেষ করে ফেলে
        if chat_id not in user_states:
            bot.send_message(chat_id, "দয়া করে /start দিয়ে পুনরায় শুরু করুন।")
            return

        selected_index = int(call.data.split("_")[1])
        user_data = user_states[chat_id]
        q_index = user_data['current_q']
        
        # সঠিক উত্তর চেক করা
        correct_index = quiz_data[q_index]['correct_index']
        
        if selected_index == correct_index:
            user_states[chat_id]['score'] += 1
            bot.answer_callback_query(call.id, "✅ সঠিক উত্তর!")
        else:
            correct_ans_text = quiz_data[q_index]['options'][correct_index]
            bot.answer_callback_query(call.id, "❌ ভুল উত্তর!")
            bot.send_message(chat_id, f"ভুল উত্তর! সঠিক উত্তরটি হলো: {correct_ans_text}")

        # পরের প্রশ্নে যাওয়া
        user_states[chat_id]['current_q'] += 1
        send_question(chat_id)

# বট চালু রাখা
print("Bot is running...")
bot.infinity_polling()
