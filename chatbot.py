import base64
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
                         CallbackContext, CallbackQueryHandler)
import logging
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from ChatGPT_HKBU import HKBU_ChatGPT
from google.cloud.firestore import FieldFilter
import threading
from health_server import run_health_server

def load_firebase_creds():
    try:    
        if "FIREBASE_CREDENTIALS" not in os.environ:
            raise ValueError("FIREBASE_CREDENTIALS not found in environment. Available vars: " + ", ".join(os.environ.keys()))
    
        creds_json = base64.b64decode(os.environ["FIREBASE_CREDENTIALS"])
        return json.loads(creds_json)
    except Exception as e:
        raise ValueError(f"Invalid Firebase credentials: {str(e)}")

cred = credentials.Certificate(load_firebase_creds())
firebase_admin.initialize_app(cred)
db = firestore.client()

class TelegramChatBot:
    def __init__(self):
        self.updater = Updater(token=os.environ['T_ACCESS_TOKEN'], use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.chatgpt = HKBU_ChatGPT(os.environ['C_ACCESS_TOKEN'])
        
        # Set up logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        handlers = [
            CommandHandler("start", self._start),
            CommandHandler("help", self._help),
            CommandHandler("interests", self._set_interests),
            CommandHandler("match", self._find_matches),
            MessageHandler(Filters.text & (~Filters.command), self._handle_message),
            CallbackQueryHandler(self._handle_button_click),
            CommandHandler("summarize", self._summarize_text),
            CommandHandler("translate", self._translate_text),
        ]
        for handler in handlers:
            self.dispatcher.add_handler(handler)
    
    
    def _extract_user_info(self, update: Update) -> dict:
        user = update.effective_user
        return {
            "user_id": str(user.id),
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language_code": user.language_code
        }
    
    def save_user(self, update: Update, interests: list = None) -> None:
        try:
            user_info = self._extract_user_info(update)
            user_ref = db.collection("users").document(user_info["user_id"])
            
            update_data = {
                **user_info,
                "last_active": firestore.SERVER_TIMESTAMP,
                "chat_history": firestore.ArrayUnion([{
                    "message": update.message.text,
                    "timestamp": datetime.now().isoformat()
                }])
            }
            
            if interests is not None:
                update_data["interests"] = interests 
                
            user_ref.set(update_data, merge=True)
            logging.info(f"Saved data for user {user_info['user_id']}")
        except Exception as e:
            logging.error(f"Error saving user: {str(e)}")
            raise
    
    def get_user(self, user_id: str) -> dict:
        doc_ref = db.collection("users").document(str(user_id))
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None
    
    def _start(self, update: Update, context: CallbackContext) -> None:
        self.save_user(update) 
        welcome_msg = (
            "Welcome!\n\n"
            "I can help you connect with people who share your interests.\n"
            "Use /interests to tell me what you're interested in."
        )
        update.message.reply_text(welcome_msg)
    
    def _help(self, update: Update, context: CallbackContext) -> None:
        help_text = (
            "Bot Commands:\n"
            "/start - Begin using the bot\n"
            "/interests - Set your interests (comma separated)\n"
            "/help - Show this help message\n"
            "/match - Find other people with same interests\n"
            "/translate - Translate a sentence with AI\n"
            "/summarize - Let AI summarize a text for you\n"
            "Just type normally to chat with the AI!"
        )
        update.message.reply_text(help_text)
    
    def _set_interests(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            update.message.reply_text(
                "Please specify interests separated by commas.\n"
                "Example: /interests gaming,food,hiking"
            )
            return
        
        interests = [interest.strip().lower() 
                    for interest in " ".join(context.args).split(",")
                    if interest.strip()]
        
        if not interests:
            update.message.reply_text("No valid interests provided.")
            return
            
        self.save_user(update, interests)
        update.message.reply_text(f"✅ Interests saved: {', '.join(interests)}")
    
    def _handle_message(self, update: Update, context: CallbackContext) -> None:
        self.save_user(update)
        
        # Get or create chat history from context
        chat_history = context.chat_data.get('chat_history', [])
        chat_history.append({"role": "user", "content": update.message.text})
        user_data = self.get_user(str(update.effective_user.id))
        
        # Get ChatGPT response with full context
        reply_message = self.chatgpt.submit_with_history(
            chat_history, user_data)
        
        # Store bot's response in history
        chat_history.append({"role": "assistant", "content": reply_message})
        context.chat_data['chat_history'] = chat_history
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_message
        )

    def _summarize_text(self, update: Update, context: CallbackContext):
        if not context.args:
            update.message.reply_text("Please provide text to summarize after the command.")
            return
        
        text = " ".join(context.args)
        prompt = f"Please summarize the following text in 3 sentences or less:\n\n{text}"
        summary = self.chatgpt.submit(prompt)
        update.message.reply_text(f"📝 Summary:\n\n{summary}")

    def _translate_text(self, update: Update, context: CallbackContext):
        if len(context.args) < 2:
            update.message.reply_text("Usage: /translate <target_language> <text>")
            return
        
        target_lang = context.args[0]
        text = " ".join(context.args[1:])
        prompt = f"Translate the following text to {target_lang}. Only provide the translation, no additional text:\n\n{text}"
        translation = self.chatgpt.submit(prompt)
        update.message.reply_text(f"🌍 Translation:\n\n{translation}")
        
    def _find_matches(self, update: Update, context: CallbackContext) -> None:
        try:
            # Get the appropriate message context
            if update.callback_query:
                bot = update.callback_query
                send_message = bot.edit_message_text
                chat_id = update.callback_query.message.chat_id
            else:
                send_message = update.message.reply_text
                chat_id = update.message.chat_id

            # Get current user's data
            current_user_id = str(update.effective_user.id)
            current_user = self.get_user(current_user_id)
            
            if not current_user or not current_user.get("interests"):
                return send_message("Please set your interests first with /interests")
            
            # First query: Get users with matching interests
            matching_users = []
            for interest in current_user["interests"]:
                query = db.collection("users").where(
                    "interests", "array_contains", interest
                ).limit(5)
                matching_users.extend([doc.to_dict() for doc in query.stream()])
            
            # Filter out current user and duplicates
            unique_matches = {
                u["user_id"]: u for u in matching_users 
            }
            
            if not unique_matches:
                return send_message("No matches found yet. Try again later!")
            
            # Create buttons for matches
            buttons = []
            for user_id, user in list(unique_matches.items())[:5]:  # Limit to 5 matches
                name = user.get("first_name", "")
                username = user.get("username", "")
                button_text = f"{name} (@{username})" if name else f"@{username}"
                
                buttons.append([
                    InlineKeyboardButton(
                        button_text,
                        callback_data=f"profile_{user_id}"
                    )
                ])
            
            # Send the message with buttons
            send_message(
                text="People with similar interests:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            
        except Exception as e:
            logging.error(f"Error in _find_matches: {e}")
            # Fallback error message that works in both contexts
            context.bot.send_message(
                chat_id=chat_id,
                text="⚠️ An error occurred while searching for matches"
            )

    def _handle_button_click(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        data = query.data
        
        if data.startswith("profile_"):
            user_id = data.split("_")[1]
            user_data = self.get_user(user_id)
            
            if not user_data:
                query.answer("User not found")
                return
                
            # Show simple profile info
            profile_msg = (
                f"Name: {user_data.get('first_name', 'N/A')}\n"
                f"Username: @{user_data.get('username', 'N/A')}\n"
                f"Interests: {', '.join(user_data.get('interests', []))}"
            )
            
            query.edit_message_text(
                text=profile_msg,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="back_to_matches")]
                ])
            )
        elif data == "back_to_matches":
            # Re-run the match search when going back
            self._find_matches(update, context)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{your-firebase-project-id}"

def record_metric(metric_type, value):
    series = monitoring_v3.TimeSeries()
    series.metric.type = f"custom.googleapis.com/{metric_type}"
    series.resource.type = "global"
    
    point = series.points.add()
    point.value.int64_value = value
    point.interval.end_time.seconds = int(time.time())
    
    client.create_time_series(name=project_name, time_series=[series])

if __name__ == '__main__':
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()
    chatbot = TelegramChatBot()
    chatbot.run()