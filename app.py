import logging
from telegram import ForceReply, Update, Location
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import openai

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(rf"Hello {user.mention_html()}! I am an Emergency Registration Chatbot what's your Emergency ?? ")

async def accident(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usertext = "I have met with an Accident"
    messages.append({'role': 'user', 'content': usertext})
    await update.message.reply_html(rf" Did you have any injuries and do you need any Ambulance Assisance ?? ")

async def fire(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usertext = "There is a fire accident near me"
    messages.append({'role': 'user', 'content': usertext})
    await update.message.reply_html(rf" Did you have any injuries and do you need any Fire Brigade Assisance ?? ")

async def police(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usertext = "I have vitnessed a crime"
    messages.append({'role': 'user', 'content': usertext})
    await update.message.reply_html(rf" Whats the Crime ? are you safe ?? ")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_location = update.message.location
    if user_location:
        context.user_data['location'] = user_location
        llm_reply = context.user_data.get('llm_reply')

        doctors = ['ambulance','die','dead']
        policework = ['crime','police']
        fireworks = ['fire accident','fires']

        if any(word in llm_reply.lower() for word in doctors):
            admin_message = f"Send an Ambulance for : \n{llm_reply} \nLocation : {user_location}\n"
            await context.bot.send_message(chat_id='5372122748', text=admin_message)
            await update.message.reply_text("Thank you for sharing your location. Ambulance will arrive shortly")

        if any(word in llm_reply.lower() for word in policework):
            admin_message = f"Send an Police Force for : \n{llm_reply} \nLocation : {user_location}\n"
            await context.bot.send_message(chat_id='5372122748', text=admin_message)
            await update.message.reply_text("Thank you for sharing your location. Police will arrive shortly")

        if any(word in llm_reply.lower() for word in fireworks):
            admin_message = f"Send a Fire Brigade and Ambulance for : \n{llm_reply} \nLocation : {user_location}\n"
            await context.bot.send_message(chat_id='5372122748', text=admin_message)
            await update.message.reply_text("Thank you for sharing your location. Fire Brigade and Ambulance  will arrive shortly")

    else:
        await update.message.reply_text("Sorry, I couldn't retrieve your location.")

openai.api_type = "open_ai"
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "Whatever"
messages = [{'role': 'system', 'content': 'You are an Emergency Registering Chatbot in India. Responses should be short, and only one question at a time. Do not suggest calling 911, 112, or 108. If the problem is serious, ask for the user location. and send an ambulance or fire brigade or police respectively'}]

async def bot_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Emergency Description from User: %s", update.message.text)

    if update.message.text != '':
        user_input = update.message.text
        messages.append({'role': 'user', 'content': user_input})
        response = openai.ChatCompletion.create(model='gpt-4', messages=messages, temperature=0, max_tokens=-1)
        messages.append({'role': 'assistant', 'content': response.choices[0].message.content})
        llm_reply = response.choices[0].message.content
        context.user_data['llm_reply'] = llm_reply
    else:
        return

    await update.message.reply_text(llm_reply)

def main() -> None:
    application = Application.builder().token("7025468713:AAGwIEtbNxN7PnHIxIZivYAD5fRJRtnqZpI").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_reply))
    application.add_handler(MessageHandler(filters.LOCATION, location))
    application.add_handler(MessageHandler(filters.TEXT, accident))
    application.add_handler(MessageHandler(filters.TEXT, police))
    application.add_handler(MessageHandler(filters.TEXT, fire))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
