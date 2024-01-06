import requests
from telegram import Update
from telegram.ext import CallbackContext

from TitanXManager import dispatcher
from TitanXManager.modules.disable import DisableAbleCommandHandler


def truth(update: Update, context: CallbackContext):
    truth = requests.get(f"https://api.truthordarebot.xyz/v1/truth").json()["question"]
    update.effective_message.reply_text(truth)


def dare(update: Update, context: CallbackContext):
    dare = requests.get(f"https://api.truthordarebot.xyz/v1/dare").json()["question"]
    update.effective_message.reply_text(dare)


TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth, run_async=True)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare, run_async=True)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)


__help__ = """
 ✧ /truth *:* Sends a random truth string.
 ✧ /dare *:* Sends a random dare string.
"""

__mod_name__ = "◈ 𝐓ʀᴜᴛʜ & 𝐃ᴀʀᴇ ◈"
