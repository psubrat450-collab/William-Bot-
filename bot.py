import json
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import schedule
import telebot
from telebot import types

# --- Tiny Web Server to satisfy Render free web service ---
class SimpleHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"William Bot is running!")


def run_web_server():
  port = int(os.environ.get("PORT", 8080))
  server = HTTPServer(("0.0.0.0", port), SimpleHandler)
  server.serve_forever()


threading.Thread(target=run_web_server, daemon=True).start()

# --- Bot & AI Configuration ---
BOT_TOKEN = "8936530333:AAFEjUby9Syj8YUwudYTA-Et5Ebyh7FHgWg"
GEMINI_KEY = "AQ.Ab8RN6I4X4nkJ4h74M17FK00FtzMATEJHNz_oXac9GQSf2lovA"

CHANNEL_ID = "@OdishaTGT_PGT_OAVSEnglish"
GROUP_ID = "@OdishaTgt_Pgt_Oavs_English"

bot = telebot.TeleBot(BOT_TOKEN)


def generate_daily_pack():
  prompt = """
You are an expert exam setter for Odisha TGT/PGT and OAVS English recruitment.
Generate today's daily content pack strictly as a JSON object with this exact structure:
{
  "word_card": {
    "word": "Term Name",
    "type": "Category (Literary Theory, ELT, Rhetoric, Linguistics, etc.)",
    "definition": "Clear concise meaning",
    "example": "Context or work it appears in",
    "exam_tip": "Why it matters for TGT/PGT/OAVS"
  },
  "quizzes": [
    {
      "question": "🎯 [ELT] Question text",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_id": 0,
      "explanation": "Brief explanation why this option is correct."
    },
    {
      "question": "🎯 [Grammar] Question text",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_id": 1,
      "explanation": "Grammar rule applied here."
    },
    {
      "question": "🎯 [Literature] Question text",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_id": 2,
      "explanation": "Literary historical fact."
    },
    {
      "question": "🎯 [Reasoning] Question text",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_id": 0,
      "explanation": "Logical derivation."
    }
  ]
}
Return raw JSON only, without any markdown formatting or backticks.
"""
  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
  headers = {"Content-Type": "application/json"}
  payload = {"contents": [{"parts": [{"text": prompt}]}]}

  res = requests.post(url, headers=headers, json=payload)
  res_data = res.json()
  raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
  raw_text = re.sub(r"^```json\s*", "", raw_text)
  raw_text = re.sub(r"\s*```$", "", raw_text)
  return json.loads(raw_text)


def send_daily_batch():
  try:
    data = generate_daily_pack()
    w = data["word_card"]

    card_text = f"""📖 **WORD OF THE DAY**
━━━━━━━━━━━━━━━━━━━
🔤 **Term:** `{w['word']}`
🏷 **Type:** *{w['type']}*

📌 **Meaning:** {w['definition']}
📝 **Context:** _{w['example']}_

💡 **Exam Tip:** {w['exam_tip']}
━━━━━━━━━━━━━━━━━━━
📢 *Attempt today's pinned 4-subject quiz in our discussion group!*"""

    bot.send_message(CHANNEL_ID, card_text, parse_mode="Markdown")

    for q in data["quizzes"]:
      res = bot.send_poll(
          chat_id=GROUP_ID,
          question=q["question"],
          options=q["options"],
          type="quiz",
          correct_option_id=q["correct_id"],
          explanation=q["explanation"],
          is_anonymous=True,
      )
      bot.pin_chat_message(GROUP_ID, res.message_id, disable_notification=True)
      time.sleep(2)

  except Exception as e:
    print(f"Error in automated daily post: {e}")


def run_scheduler():
  schedule.every().day.at("02:30").do(send_daily_batch)  # 02:30 UTC = 8:00 AM IST
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
        f"👋 Welcome {user.first_name} to **Odisha TGT/PGT OAVS English Exam"
        " Hub**!\n\n📌 Check the pinned messages above for today's English"
        " Literature & Grammar quizzes.\n🔔 Join our official channel for notes"
        " & updates."
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📢 Main Channel", url="https://t.me/OdishaTGT_PGT_OAVSEnglish"
        )
    )
    bot.reply_to(
        message, welcome_text, parse_mode="Markdown", reply_markup=markup
    )


@bot.message_handler(commands=["start"])
def handle_start(message):
  bot.reply_to(
      message,
      "Hello! I am William, your English Exam Assistant.\nType /syllabus for"
      " the complete breakdown.",
  )


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
        bot.send_message(
            message.chat.id,
            f"⚠️ @{message.from_user.username or message.from_user.first_name},"
            " promotional links are not allowed.",
        )
    except Exception:
      pass


if __name__ == "__main__":
  bot.infinity_polling(skip_pending=True)
    
