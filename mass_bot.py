import os
import telebot
from openai import OpenAI

# --- Берем ключи из переменных окружения ---
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# --- СОЗДАЕМ КЛИЕНТОВ ---
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# --- ОБРАБОТЧИК СООБЩЕНИЙ ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text

    # Формируем системный промпт
    system_prompt = """
    Ты MassGain Coach — персональный ИИ-помощник для набора мышечной массы с ограниченным бюджетом.
    Ты помогаешь с питанием, тренировками, сном и бюджетом.
    Отвечай кратко, по делу, с эмодзи. Если пользователь просто поздоровался, представься и спроси, с чего начнем.
    """

    try:
        # Отправляем запрос к OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500
        )

        # Извлекаем ответ от ИИ
        ai_response = response.choices[0].message.content

        # Отправляем ответ пользователю
        bot.reply_to(message, ai_response)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

# --- ЗАПУСКАЕМ БОТА ---
if __name__ == "__main__":
    print("MassGain Bot запущен и работает!")
    bot.infinity_polling()
