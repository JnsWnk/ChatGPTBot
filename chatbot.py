import base64
import json
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import logging
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from ChatGPT_HKBU import HKBU_ChatGPT

def load_firebase_creds():
    try:
        print("Available env vars:", list(os.environ.keys()))
    
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
        self.dispatcher.add_handler(CommandHandler("start", self._start))
        self.dispatcher.add_handler(CommandHandler("help", self._help))
        self.dispatcher.add_handler(CommandHandler("set_interests", self._set_interests))
        
        # Message handler for ChatGPT
        self.dispatcher.add_handler(
            MessageHandler(Filters.text & (~Filters.command), self._handle_message)
        )
    
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
        user_info = self._extract_user_info(update)
        user_ref = db.collection("users").document(user_info["user_id"])
        
        user_data = {
            **user_info,
            "interests": interests or [],
            "last_active": firestore.SERVER_TIMESTAMP,
            "chat_history": firestore.ArrayUnion([{
                "message": update.message.text,
                "timestamp": datetime.now().isoformat()
            }])
        }
        
        # Merge data instead of overwriting
        user_ref.set(user_data, merge=True)
        logging.info(f"Saved user data for {user_info['user_id']}")
    
    def get_user(self, user_id: str) -> dict:
        doc_ref = db.collection("users").document(str(user_id))
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None
    
    def _start(self, update: Update, context: CallbackContext) -> None:
        self.save_user(update) 
        welcome_msg = (
            "Welcome!\n\n"
            "I can help you connect with people who share your interests.\n"
            "Use /set_interests to tell me what you're interested in."
        )
        update.message.reply_text(welcome_msg)
    
    def _help(self, update: Update, context: CallbackContext) -> None:
        help_text = (
            "Bot Commands:\n"
            "/start - Begin using the bot\n"
            "/set_interests - Set your interests (comma separated)\n"
            "/help - Show this help message\n\n"
            "Just type normally to chat with the AI!"
        )
        update.message.reply_text(help_text)
    
    def _set_interests(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            update.message.reply_text("Please specify your interests separated by commas.\nExample: /set_interests gaming,VR,technology")
            return
        
        interests = [interest.strip().lower() for interest in " ".join(context.args).split(",")]
        self.save_user(update, interests)
        update.message.reply_text(f"Interests updated! You've set: {', '.join(interests)}")
    
    def _handle_message(self, update: Update, context: CallbackContext) -> None:
        self.save_user(update)
        
        # Get ChatGPT response
        reply_message = self.chatgpt.submit(update.message.text)
        
        logging.info(f"User {update.effective_user.id} message: {update.message.text}")
        logging.info(f"Bot reply: {reply_message}")
        
        # Send response
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_message
        )
    
    def run(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    bot = TelegramChatBot()
    bot.run()