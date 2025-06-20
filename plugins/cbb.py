from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=f"<b>╔════════════⦿\n├⋗ ᴄʀᴇᴀᴛᴏʀ : <a href='tg://user?id={OWNER_ID}'>⚚ Goku  </a>\n╚═════════════════⦿</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data == "premium":
        await query.message.edit_text(
            text=f"<b>@Hentai_Cinema Premium benefits\nDirect Channel links,No ad links\nSpecial Acess in events\n\n1. <a href='https://t.me/+aVGWTVnbM2BiNDdl'>Corn_Cinema</a>\n2. <a href='https://t.me/+dPaKYC1IDLNlYTVl'>Jav_Cosplay_Cinema</a>\n3. <a href='https://t.me/+uBh_4qLYUlNmNTZl'>Hentai_Cinema</a>\n4. <a href='https://t.me/+RVDTZanGoUQ1MTI9'>Indian_18Cinema</a>\n5. <a href='https://t.me/+VPp5pqHk3XUyNTc1'>Only_Fans_Cinema</a>\n6. <a href='https://t.me/+jr6WX0Edf1EyODRl'>Parody_Cinema</a>\n7. <a href='https://t.me/+AOIGOd9Lqng5ZmRl'>Japanese_Cinema</a>\n\nPricing Rates\n1 Month - INR 80\n3 Months - INR 200\n6 Months - INR 400\n12 Months - INR 750\n\nWant To Buy?\nContact or Dm - @Mr_Goku_UI \n\nWe Have Limited Seats For Premium Users</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("18+ Cinema", url="https://t.me/+aVGWTVnbM2BiNDdl"),
                        InlineKeyboardButton("H*ntai", url="https://t.me/+uBh_4qLYUlNmNTZl")              
                    ],
                    [
                        InlineKeyboardButton("🔒 Close", callback_data="close"),
                        InlineKeyboardButton("🔒 Close", callback_data="close")
                    ]
                ]
            )
        )
