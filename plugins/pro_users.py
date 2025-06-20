from pyrogram import filters
from pyrogram.types import Message

from bot import Bot
from config import OWNER_ID
from database.database import add_pro, is_pro, remove_pro, get_pros_list


@Bot.on_message(filters.command('authorize') & filters.private)
async def add_admin_command(client: Bot, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        await message.reply_text("Baka! Only Owner Can Use this command..")
        return

    # Check if the command has the expected number of arguments
    if len(message.command) != 2:
        await message.reply_text("<b>ese use karo sir 🙂</b> /authorize userid")
        return
    try:
        user_id_to_add = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a valid user ID.")
        return
    # Add the user to the admin list in the database
    added = await add_pro(user_id_to_add)
    if added:
        await message.reply_text(f"<b>User {user_id_to_add} has been added to the authorize list.</b>")
    else:
        await message.reply_text(f"<b>User {user_id_to_add} is already an pro.</b>")


@Bot.on_message(filters.command('unauthorize') & filters.private)
async def remove_admin_command(client: Bot, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        await message.reply_text("Baka! Only Owner Can Use this command..")
        return
    # Check if the command has the expected number of arguments
    if len(message.command) != 2:
        await message.reply_text("<b>ese use karo sir 🙂</b> /unauthorize userid")
        return
    try:
        user_id_to_remove = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a valid user ID.")
        return
    # Remove the user from the admin list in the database
    removed = await remove_pro(user_id_to_remove)
    if removed:
        await message.reply_text(f"<b>User {user_id_to_remove} has been removed from the authorized list.</b>")
    else:
        await message.reply_text(f"<b>User {user_id_to_remove} is not an admin or was not found in the pro list.</b>")

@Bot.on_message(filters.command('authorized') & filters.private)
async def admin_list_command(client: Bot, message: Message):
    user_id = message.from_user.id
    is_user_pro = await is_pro(user_id)
    if user_id != OWNER_ID:
        await message.reply_text("Baka! Only Owner Can Use this command..")
        return

    pro_user_ids = await get_pros_list()  
    formatted_admins = []

    for user_id in pro_user_ids:
        user = await client.get_users(user_id)
        if user:
            username = user.username
            full_name = user.first_name + (" " + user.last_name if user.last_name else "")
            if username:
                profile_link = f"{full_name} - @{username}"
            else:
                profile_link = full_name
            formatted_admins.append(profile_link)

    if formatted_admins:
        admins_text = "\n".join(formatted_admins)
        text = f"<b>List of admin users:</b>\n\n{admins_text}"
    else:
        text = "<b>No admin users found.</b>"

    await message.reply_text(text, disable_web_page_preview=True)
