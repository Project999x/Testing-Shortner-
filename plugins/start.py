#(©)CodeXBotz




import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user
from database.database import add_pro, is_pro, remove_pro, get_pros_list, total_click, add_click
from plugins.shortner import get_short

SHORT_MSG = "total clicks :-  {total_count} Here is your link tap on short link and bypass the ads👇"

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        if not await present_user(user_id):
            await add_user(user_id)
    except Exception as e:
        print(f"Error adding user: {e}")

    text = message.text

    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]
            if basic.startswith("yu3elk"):
                base64_string = basic[6:-1]
            else:
                base64_string = text.split(" ", 1)[1]
                
        except Exception as e:
            print(f"Error processing message: {e}")
            return

        is_user_pro = await is_pro(user_id)
        if not is_user_pro and user_id != OWNER_ID and not basic.startswith("yu3elk"):
            await short_url(client, message, base64_string)                        
            return

       
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception as e:
                print(f"Error calculating start/end: {e}")
                return
            if start <= end:
                ids = range(start, end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error processing argument: {e}")
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            print(f"Error getting messages: {e}")
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()
        await add_click(user_id, base64_string)

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)                
                
            except Exception as e:
                print(f"Error copying message: {e}")

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data="about"),
                    InlineKeyboardButton("🔒 Close", callback_data="close")
                ]
            ]
        )
        try:
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        except Exception as e:
            print(f"Error replying to message: {e}")
        return
                


#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##


async def short_url(client: Client, message: Message, base64_string):
    try:
        prem_link = f"https://t.me/{client.username}?start=yu3elk{base64_string}7"      
        short_link = get_short(prem_link)
        total_clicks = await total_click(base64_string)
        
        buttons = [
            [
                InlineKeyboardButton(text="⛩️𝗕𝘂𝘆 𝗣𝗿𝗲𝗺𝗶𝘂𝗺⛩️", callback_data="premium"),
                InlineKeyboardButton(text="𝗛𝗼𝘄 𝘁𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱", url="https://t.me/open_links_to/5"),
            ],
            [
                InlineKeyboardButton(text="💦𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱💦", url=short_link)
            ]
        ]

        await message.reply(
            text=SHORT_MSG.format(               
                total_count=total_clicks
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            disable_web_page_preview=True
        )

    except IndexError:
        pass

@Bot.on_message(filters.command('request') & filters.private)
async def request(client: Bot, message: Message):
    user_id = message.from_user.id
    is_user_pro = await is_pro(user_id)
 
    if not is_user_pro and user_id != OWNER_ID:   
        inline_button = InlineKeyboardButton("Upgrade to Premium", callback_data="premium")
        inline_keyboard = InlineKeyboardMarkup([[inline_button]])
        
        await message.reply(
            "You are not a premium user. Upgrade to premium to access this feature.",
            reply_markup=inline_keyboard
        )
        return
  
    if len(message.command) < 2:
        await message.reply("Send me your request in this format: /request hentai Name Quality Episode")
        return

    requested = " ".join(message.command[1:])
    
    owner_message = f"{message.from_user.first_name} ({message.from_user.id}) \n\nuplaod karo:- {requested}"
    await client.send_message(OWNER_ID, owner_message)
  
    await message.reply("Thanks for your request! Your request will be uploaded soon. Please wait.")
    
        
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink),
            InlineKeyboardButton(text="Join Channel", url=client.invitelink2),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('profile') & filters.private)
async def profile(client: Bot, message: Message):
    user_id = message.from_user.id
    is_user_pro = await is_pro(user_id)
 
    if not is_user_pro and user_id != OWNER_ID:
        preference = "Enabled"
        absence = "Disabled"
    else:
        preference = "Disabled"
        absence = "Enabled"
        
    await message.delete()
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    new_msg_text = f"Name: {message.from_user.first_name}\n\nAd Link: {preference}\nDirect Links: {absence}\nOn-Demand Hentai: {absence}"
 
    if preference == "Disabled":
        new_msg_text += "\n\n🌟 You are a Pro User 🌟"
  
    new_msg = await msg.edit_text(new_msg_text)

    if preference == "Enabled":
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Premium", callback_data="premium")]])
        await new_msg.edit_text(new_msg.text, reply_markup=reply_markup)
        

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")





@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast ho rha till then FUCK OFF </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
      
