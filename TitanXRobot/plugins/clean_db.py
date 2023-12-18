import time
from asyncio import sleep
from traceback import format_exc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import PeerIdInvalid, UserNotParticipant

from TitanXRobot import LOGGER, MESSAGE_DUMP, TIME_ZONE
from TitanXRobot.bot_class import Titan
from TitanXRobot.database.approve_db import Approve
from TitanXRobot.database.blacklist_db import Blacklist
from TitanXRobot.database.chats_db import Chats
from TitanXRobot.database.disable_db import Disabling
from TitanXRobot.database.filters_db import Filters
from TitanXRobot.database.flood_db import Floods
from TitanXRobot.database.greetings_db import Greetings
from TitanXRobot.database.notes_db import Notes, NotesSettings
from TitanXRobot.database.pins_db import Pins
from TitanXRobot.database.reporting_db import Reporting
# from TitanXRobot.database.users_db import Users
from TitanXRobot.database.warns_db import Warns, WarnSettings
from TitanXRobot.utils.custom_filters import command
from TitanXRobot.vars import Config


async def clean_my_db(c:Titan,is_cmd=False, id=None):
    to_clean = list()
    chats_list = Chats.list_chats_by_id()
    to_clean.clear()
    start = time.time()
    for chats in chats_list:
        try:
            stat = await c.get_chat_member(chat_id=chats,user_id=Config.BOT_ID)
            if stat.status not in [CMS.MEMBER, CMS.ADMINISTRATOR, CMS.OWNER]:
                to_clean.append(chats)
        except UserNotParticipant:
            to_clean.append(chats)
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(format_exc())
            if not is_cmd:
                return e
            else:
                to_clean.append(chats)
    for i in to_clean:
        Approve(i).clean_approve()
        Blacklist(i).clean_blacklist()
        Chats.remove_chat(i)
        Disabling(i).clean_disable()
        Filters().rm_all_filters(i)
        Floods().rm_flood(i)
        Greetings(i).clean_greetings()
        Notes().rm_all_notes(i)
        NotesSettings().clean_notes(i)
        Pins(i).clean_pins()
        Reporting(i).clean_reporting()
        Warns(i).clean_warn()
        WarnSettings(i).clean_warns()
    x = len(to_clean)
    txt = f"#INFO\n\nCleaned db:\nTotal chats removed: {x}"
    to_clean.clear()
    nums = time.time()-start
    if is_cmd:
        txt += f"\nClean type: Forced\nInitiated by: {(await c.get_users(user_ids=id)).mention}"
        txt += f"\nClean type: Manual\n\tTook {round(nums,2)} seconds to complete the process"
        await c.send_message(chat_id=MESSAGE_DUMP,text=txt)
        return txt
    else:
        txt += f"\nClean type: Auto\n\tTook {round(nums,2)} seconds to complete the process"
        await c.send_message(chat_id=MESSAGE_DUMP,text=txt)
        return txt
    


