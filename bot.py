import telebot
from telebot import types
import threading
import schedule
import time
import random
import requests
import json

BOT_TOKEN = "8936530333:AAFEjUby9Syj8YUwudYTA-Et5Ebyh7FHgWg"
CHANNEL_ID = "@OdishaTGT_PGT_OAVSEnglish"
GROUP_ID = "@OdishaTgt_Pgt_Oavs_English"

bot = telebot.TeleBot(BOT_TOKEN)

words_pool = [
    {
        "word": "Objective Correlative",
        "type": "Literary Term / Criticism",
        "definition": "A set of objects, a situation, or a chain of events that serves as the formula for a particular emotion.",
        "example": "T. S. Eliot used this concept in his critique of Shakespeare's 'Hamlet'.",
        "exam_tip": "High frequency in TGT/PGT English literary criticism sections."
    },
    {
        "word": "Catharsis",
        "type": "Literary Term (Aristotelian Poetics)",
        "definition": "The purification or purgation of emotions—especially pity and fear—through art or extreme change.",
        "example": "The tragic conclusion of King Lear evokes intense catharsis in the audience.",
        "exam_tip": "Core concept for questions on Aristotelian drama and tragedy."
    },
    {
        "word": "Direct Method",
        "type": "ELT Pedagogy",
        "definition": "A language teaching approach where target language is used exclusively, with mother tongue prohibited.",
        "example": "Focuses on inductive grammar teaching and everyday oral communication.",
        "exam_tip": "Crucial distinction from the Grammar-Translation Method."
    },
    {
        "word": "Anaphora",
        "type": "Rhetorical Device / Figure of Speech",
        "definition": "The repetition of a word or phrase at the beginning of successive clauses.",
        "example": "'It was the best of times, it was the worst of times...'",
        "exam_tip": "Frequently tested under stylistic devices and poetic techniques."
    }
]

quizzes_pool = [
    {
        "question": "🎯 [ELT] Which method emphasizes grammatical rules and translation of texts into the native language?",
        "options": ["A) Direct Method", "B) Audio-Lingual Method", "C) Grammar-Translation Method", "D) Communicative Language Teaching"],
        "correct_id": 2,
        "explanation": "GTM relies explicitly on prescriptive grammar rules and translation into the mother tongue."
    },
    {
        "question": "🎯 [Grammar] Identify the error: 'Neither the principal nor the teachers (A) / was present (B) / in the meeting. (C) / No error (D)'",
        "options": ["A) Part A", "B) Part B", "C) Part C", "D) Part D"],
        "correct_id": 1,
        "explanation": "Rule of proximity: when connected by 'neither... nor', the verb agrees with the nearer subject ('teachers were')."
    },
    {
        "question": "🎯 [Literature] Who among the following authored the post-colonial African masterpiece 'Things Fall Apart'?",
        "options": ["A) Chinua Achebe", "B) Wole Soyinka", "C) Ngũgĩ wa Thiong'o", "D) Nadine Gordimer"],
        "correct_id": 0,
        "explanation": "Chinua Achebe wrote 'Things Fall Apart' in 1958, capturing Igbo society prior to colonization."
    },
    {
        "question": "🎯 [Reasoning] Complete the number series: 3, 7, 15, 31, 63, ___",
        "options": ["A) 127", "B) 126", "C) 125", "D) 128"],
        "correct_id": 0,
        "explanation": "Pattern: multiply the previous term by 2 and add 1. (63 × 2) + 1 = 127."
    }
]

def send_daily_batch():
    try:
        word = random.choice(words_pool)
        card = f"""📖 **WORD OF THE DAY**
━━━━━━━━━━━━━━━━━━━
🔤 **Term:** `{word['word']}`
🏷 **Type:** *{word['type']}*

📌 **Meaning:** {word['definition']}
📝 **Context:** _{word['example']}_

💡 **Exam Tip:** {word['exam_tip']}
━━━━━━━━━━━━━━━━━━━
📢 *Attempt today's pinned 4-subject quiz in our discussion group!*"""

        bot.send_message(CHANNEL_ID, card, parse_mode="Markdown")

        for q in quizzes_pool:
            res = bot.send_poll(
                chat_id=GROUP_ID,
                question=q["question"],
                options=q["options"],
                type="quiz",
                correct_option_id=q["correct_id"],
                explanation=q["explanation"],
                is_anonymous=True
            )
            bot.pin_chat_message(GROUP_ID, res.message_id, disable_notification=True)
            time.sleep(2)
    except Exception as e:
        print(f"Error in batch: {e}")

def run_scheduler():
    schedule.every().day.at("02:30").do(send_daily_batch)
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=run_scheduler, daemon=True).start()

@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message):
    for user in message.new_chat_members:
        if user.id == bot.get_me().id:
            continue
        welcome_text = (
            f"👋 Welcome {user.first_name} to **Odisha TGT/PGT OAVS English Exam Hub**!\n\n"
            "📌 Check the pinned messages above for today's English Literature & Grammar quizzes.\n"
            "🔔 Join our official channel for notes & updates."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Main Channel", url="https://t.me/OdishaTGT_PGT_OAVSEnglish"))
        bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "Hello! I am William, your English Exam Assistant.\nType /syllabus for the complete breakdown.")

@bot.message_handler(commands=["syllabus"])
def handle_syllabus(message):
    syllabus_text = """
📚 **OAVS / TGT / PGT Complete Exam Syllabus**

1️⃣ **English Language Teaching (ELT)**
• Methods & Approaches (CLT, Direct, Audio-Lingual, GTM)
• Teaching of Prose, Poetry, Grammar & Composition
• Evaluation, Assessment & Remedial Teaching

2️⃣ **Literature Core & Movements**
• Shakespeare & Classical Drama (Tragedies & Comedies)
• Romantic Poets (Wordsworth, Coleridge, Keats, Shelley, Byron)
• 19th & 20th Century English & American Literature
• Modern World Literature in English (Post-Colonial & Commonwealth)
• Indian Writing in English

3️⃣ **Writing Ability & Applied Grammar**
• Precis, Reports, Paragraph & Letter Formats
• Error Spotting, Clauses, Tenses, Voice, Prepositions

4️⃣ **General Paper Essentials**
• Reasoning Ability (Verbal & Non-Verbal)
• Odia Grammar (ସନ୍ଧି, ସମାସ, କୃଦନ୍ତ, ତଦ୍ଧିତ, ବାଚ୍ୟ, ଶୁଦ୍ଧ-ଅଶୁଦ୍ଧ)

👉 *Daily topic quizzes are pinned in this group!*
"""
    bot.reply_to(message, syllabus_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def filter_group_messages(message):
    if message.chat.type == "private":
        return
    text = (message.text or message.caption or "").lower()
    if any(k in text for k in ["http://", "https://", "t.me/", "telegram.me/"]):
        try:
            status = bot.get_chat_member(message.chat.id, message.from_user.id).status
            if status not in ["administrator", "creator"]:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, f"⚠️ @{message.from_user.username or message.from_user.first_name}, promotional links are not allowed.")
        except Exception:
            pass

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
      
