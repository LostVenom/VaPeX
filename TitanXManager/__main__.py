import importlib
import re
import time
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import TitanXManager.modules.sql.users_sql as sql
from TitanXManager import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from TitanXManager.modules import ALL_MODULES
from TitanXManager.modules.helper_funcs.chat_status import is_user_admin
from TitanXManager.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """
Hii {}
"""


PM_START_TEXT = """
*𝐻𝑒𝑦* {}, 🫧🖤

*๏ Ｍʏsᴇʟғ* {} !

*⧉ 𝖠ɴ 𝖠ᴅᴠᴀɴᴄᴇ 🔍 & 𝖥ᴀꜱᴛ⚡️𝖦ʀᴏᴜᴘ 🦾𝖬ᴀɴᴀɢᴇᴍᴇɴᴛ👨‍💻 𝖡ᴏᴛ 𝖶ɪᴛʜ 𝖫ᴏᴛs 𝖮ғ 𝖴sᴇғᴜʟ 𝖠ɴᴅ 𝖢ᴏᴏʟ 𝖥ᴇᴀᴛᴜʀᴇs.*

*⧉ I'ᴍ🥋 𝖧ᴇʀᴇ 𝖳ᴏ 𝖧ᴇʟᴘ 𝖸ᴏᴜ 🦾𝖬ᴀɴᴀɢᴇ 𝖸ᴏᴜʀ 💡𝖦ʀᴏᴜᴘs!*

*⧉ 𝖠ᴅᴅ🔌 𝖬ᴇ 𝖨ɴ 𝖦ʀᴏᴜᴘs 𝖠ɴᴅ 🎖𝖯ʀᴏᴍᴏᴛᴇ 𝖬ᴇ 𝖳ᴏ 𝖫ᴇᴛ 𝖬ᴇ 𝖦ᴇᴛ 𝖨ɴ 𝖠ᴄᴛɪᴏɴ🥋.*

*⧉ 𝖳𝖺𝗉 𝗈𝗇 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝖡𝗎𝗍𝗍𝗈𝗇🎛 𝖳𝗈 𝖫𝖾𝖺𝗋𝗇 𝖬𝗈𝗋𝖾📄 𝖠𝖻𝗈𝗎𝗍 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 & 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌 𝖮𝖿 𝖳𝖨𝖳𝖠𝖭.*
"""

buttons = [
    [
        InlineKeyboardButton(
            text="🐼 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ 🐼",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="🕷 ᴀʙᴏᴜᴛ 🕷", callback_data="titan_"),
       InlineKeyboardButton(text="🛠 ᴄᴏᴍᴍᴀɴᴅs 🛠", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text="🔎 ꜱᴜᴘᴘᴏʀᴛ 🔍", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="🏴‍☠ ɴᴇᴛᴡᴏʀᴋ 🏴‍☠", url=f"https://t.me/TitanNetwrk",),
    ],
]

HELP_STRINGS = f"""
*☞ 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎*
𝖧𝖾𝗒! 𝖨 𝖺𝗆 𝖺 𝖦𝗋𝗈𝗎𝗉 🦾𝖬𝖺𝗇𝖺𝗀𝖾𝗆𝖾𝗇𝗍 𝖡𝗈𝗍🤖, 𝖨 𝖧𝖺𝗏𝖾 𝖫𝗈𝗍𝗌 𝖮𝖿 𝖧𝖺𝗇𝖽𝗒 𝖠𝗇𝖽 𝖴𝗌𝖾𝖿𝗎𝗅 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌🏅!

♧ /start : 𝖲𝗍𝖺𝗋𝗍𝗌 𝖬𝖾! 𝖨 𝖳𝗁𝗂𝗇𝗄 𝖸𝗈𝗎'𝖵𝖾 𝖯𝗋𝗈𝖻𝖺𝖻𝗅𝗒 𝖠𝗅𝗋𝖾𝖺𝖽𝗒 𝖴𝗌𝖾𝖽 𝖳𝗁𝗂𝗌.
♧ /help  : 𝖲𝖾𝗇𝖽𝗌 𝖳𝗁𝗂𝗌 𝖬𝖾𝗌𝗌𝖺𝗀𝖾! 𝖨'𝗅𝗅 𝖳𝖾𝗅𝗅 𝖸𝗈𝗎 𝖬𝗈𝗋𝖾 𝖠𝖻𝗈𝗎𝗍 𝖬𝗒𝗌𝖾𝗅𝖿!

  ☞ If you have any Doubts or Queries on how to use me, must visit [TITAN](https://t.me/TitanXSupport) to get your Queries ressolved as soon as possible. All commands can be used with the following: / !
"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("TitanXManager.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="🔙", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAID6mWdkhJeUGuBf2z6RTYCUYaG2Gi0AALYCwACSwnZVguLAAEiT7OTEjQE")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("⚡")
            time.sleep(0.4)
            lol.edit_text("👻")
            time.sleep(0.3)
            lol.edit_text("Starting.")
            time.sleep(0.3)
            lol.edit_text("Starting..")
            time.sleep(0.3)
            lol.edit_text("Starting...")
            time.sleep(0.5)
            lol.delete()
            
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "⧉ *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass


def Titan_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "titan_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*ʜᴇʏ👋🏻!,*"
            
            "\n\n➳ I am a 𝖦roup 𝖬anagement 𝖡ot🤖, build to 🦾help you manage your Group 👻easily and efficiently🫰🏻!"
            
            "\n\n➳ I have 🫲🏻lots🫱🏻 of handy features, which will help to manage your group ✌🏻easily and 🦾helps you in keeping your group safe🥋 from spammers📵 and raiders🚷."
            
            "\n\n➳ Thanks🙏🏻 to all our supporters✌🏻 and everyone🫰🏻 who reports issues🚫 or suggests new features🔖.."
            
            "\n\n➳ We also thank🙏🏻 all the 𝗚𝗿𝗼𝘂𝗽𝘀 who rely on our Bot🤖 for Management Services, 🫠we hope you will always ❣️like it: we are constantly 💻working to improve it💡!"
            
            f"\n\n✦ ᴛᴀᴘ ᴏɴ ʙᴜᴛᴛᴏɴ🎛 ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴀɴᴅ ʟᴇᴀʀɴ ᴍᴏʀᴇ ʙᴀsɪᴄs ᴀʙᴏᴜᴛ{BOT_NAME}.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🛠 ᴄᴏᴍᴍᴀɴᴅs 🛠", callback_data="help_back"
                        ),
                        InlineKeyboardButton(
                            text="👻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 👻", url=f"tg://user?id={OWNER_ID}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🔙", callback_data="titan_back"),
                    ],
                ]
            ),
        )
    elif query.data == "TitanXSupport":
        query.message.edit_text(
            text="*๏ ᴛᴀᴘ ᴏɴ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴀɴᴅ ᴍᴏʀᴇ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍᴇ.*"
            f"\n\nɪғ ʏᴏᴜ ғᴏᴜɴᴅ ᴀɴʏ ʙᴜɢ ɪɴ {BOT_NAME} ᴏʀ ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ɢɪᴠᴇ ғᴇᴇᴅʙᴀᴄᴋ ᴀʙᴏᴜᴛ ᴛʜᴇ {BOT_NAME}, ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔎 ꜱᴜᴘᴘᴏʀᴛ 🔍", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="🏴‍☠ ɴᴇᴛᴡᴏʀᴋ 🏴‍☠", url=f"https://t.me/TitanNetwrk"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ",
                            url="https://github.com/Pirate303",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🔙", callback_data="titan_"),
                    ],
                ]
            ),
        )
    elif query.data == "titan_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=True,
        )


def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=f"""
*Hey,
 Myself {BOT_NAME},
*

""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔙", callback_data="source_back")]]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=True,
        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʜᴇʟᴘ",
                                url="https://t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "๏ ᴛᴀᴘ ᴏɴ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Open in Private ",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                              ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Open Here",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔙", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current Settings⚙️ :" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which Module would you like to 🔍Check {}'s Settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔙",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hey there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hey there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hey there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not Modified✎",
            "Query_id_invalid",
            "Message can't be Deleted❌",
        ]:
            LOGGER.exception("Exception in Settings⚙️ Buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "𝖳𝖺𝗉 𝗈𝗇 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌⚙️ 𝗍𝗈 𝗀𝖾𝗍 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🛠 sᴇᴛᴛɪɴɢs 🛠",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "𝖳𝖺𝗉 𝗈𝗇 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌⚙️ 𝗍𝗈 𝗀𝖾𝗍 𝖸𝗈𝗎𝗋 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    global x
    x=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🐼 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ 🐼",
                            url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                            )
                       ]
                ]
                     )
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                chat_id=f"@{SUPPORT_CHAT}",
                photo=START_IMG,
                caption=f"""
🎶 {BOT_NAME} ☆● ιѕ σиℓιиє ●☆.......❤️‍🔥👻💫

╔╦════••✠•❀•✠••═════╦╗
ㅤ★**ᴍᴀᴅᴇ ʙʏ [•⏤͟͞𓆩×͜ ❛🇹𝗜𝗧𝗔𝗡𓆪ꪾ](https://t.me/TitanNetwrk)**
  ★ **ᴘʏᴛʜᴏɴ :** `{y()}`
ㅤ★ **ʟɪʙʀᴀʀʏ :** `{telever}`
ㅤ★ **ᴛᴇʟᴇᴛʜᴏɴ :** `{tlhver}`
ㅤ★ **ᴩʏʀᴏɢʀᴀᴍ :** `{pyrover}`
╚╩════••✠•❀•✠••═════╩╝
""",reply_markup=x,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Titan_about_callback, pattern=r"titan_", run_async=True
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )

    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("Titan Started...")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
