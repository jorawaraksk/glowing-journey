from telethon import events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from . import bot
from .config import APP_ID, API_HASH, OWNER, DEV
from .db import db

@bot.on(events.NewMessage(pattern="/login"))
async def login_handler(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.reply("**Sorry You're not An Authorised User!**")
    
    if not db:
        return await event.reply("**Database is not configured in environment variables.**")

    # Start an interactive conversation with the user
    async with bot.conversation(event.chat_id, timeout=300) as conv:
        await conv.send_message("**📱 Enter your phone number with country code (e.g. +91...):**")
        phone_msg = await conv.get_response()
        phone = phone_msg.text.strip()
        
        # Create a temporary client to authenticate the user
        temp_client = TelegramClient(StringSession(), APP_ID, API_HASH)
        await temp_client.connect()
        
        try:
            # Request the OTP
            code_request = await temp_client.send_code_request(phone)
            await conv.send_message("**✉️ Code sent! Please enter the code (use spaces between numbers if Telegram blocks you, e.g., '1 2 3 4 5'):**")
            code_msg = await conv.get_response()
            code = code_msg.text.replace(" ", "")
            
            try:
                # Attempt to sign in
                await temp_client.sign_in(phone, code)
            except SessionPasswordNeededError:
                # Handle Two-Step Verification
                await conv.send_message("**🔐 Two-Step Verification is enabled. Please enter your password:**")
                pwd_msg = await conv.get_response()
                await temp_client.sign_in(password=pwd_msg.text)
            
            # Save the session to MongoDB
            session_string = temp_client.session.save()
            
            if not await db.is_user_exist(event.sender_id):
                await db.add_user(event.sender_id, event.sender.first_name)
                
            await db.set_session(event.sender_id, session_string)
            await conv.send_message("**✅ Login Successful! Your session has been saved to the database.**")
            
        except Exception as e:
            await conv.send_message(f"**❌ Login Failed:** `{str(e)}`")
        finally:
            await temp_client.disconnect()

@bot.on(events.NewMessage(pattern="/logout"))
async def logout_handler(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return
        
    if db:
        await db.remove_session(event.sender_id)
        await event.reply("**✅ Successfully logged out and session deleted from the database.**")
