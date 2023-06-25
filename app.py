import openai
import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

API_KEY = os.environ.get('AI_TOKEN')
openai.api_key = API_KEY


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hmm")


@bot.message_handler(commands=['takon'])
def send_reply(message):
    sendrep = bot.send_message(message.chat.id, "Po?")
    bot.register_next_step_handler(sendrep, ai_handler)


def ai_handler(message):
    text = message.text

    if text.lower() == "Metu":
        bot.send_message(message.chat.id, "Y")
        return

    chat_log = []
    user_message = text
    chat_log.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']
    bot.send_message(message.chat.id, assistant_response.strip("\n"))
    chat_log.append({"role": "assistant", "content": assistant_response.strip("\n")})

    bot.register_next_step_handler(message, ai_handler)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
