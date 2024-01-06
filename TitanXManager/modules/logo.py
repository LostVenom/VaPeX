import glob
import io
import os
import random

import requests
from PIL import Image, ImageDraw, ImageFont

from TitanXManager import BOT_NAME, BOT_USERNAME, OWNER_ID, telethn
from TitanXManager.events import register

LOGO_LINKS = [
    "https://telegra.ph/file/627c4bfdf3b8d13648a9b.jpg",
    "https://telegra.ph/file/76af296f88ae8a4cd8e6d.jpg",
    "https://telegra.ph/file/f835d571eadf7cd83b29d.jpg",
    "https://telegra.ph/file/2b0aee788f0d6f1377e96.jpg",
    "https://telegra.ph/file/e0379f9c98f061b6251fb.jpg",
    "https://telegra.ph/file/9b63f539d1cbb06e1fcfb.jpg",
    "https://telegra.ph/file/83b65c773002472d2c763.jpg",
    "https://telegra.ph/file/06c304b084a8ca6b4213a.jpg",
    "https://telegra.ph/file/67d649062d057d453c6eb.jpg",
    "https://telegra.ph/file/94b2b4497d823f52b7e93.jpg",
    "https://telegra.ph/file/0990480ef0d1ddbc5e0dc.jpg",
    "https://telegra.ph/file/ed095942d81e38b983b4f.jpg",
    "https://telegra.ph/file/f7249a5427b373b4114cb.jpg",
    "https://telegra.ph/file/c45735d16c6185e50a555.jpg",
    "https://telegra.ph/file/1cdff205a28e5d171e7e9.jpg",
    "https://telegra.ph/file/416b0dfce3eaafc8da089.jpg",
    "https://telegra.ph/file/0610863018ca05640ffb3.jpg",
    "https://telegra.ph/file/a6962560738382c8fdf20.jpg",
    "https://telegra.ph/file/d313daf9f8562c28fc416.jpg",
    "https://telegra.ph/file/f2f5ef7b62602b69b2e74.jpg",
    "https://telegra.ph/file/3c2090c172c01ca9faa35.jpg",
    "https://telegra.ph/file/46dbd80dbf5d187cff2ab.jpg",
    "https://telegra.ph/file/bb55db499c5d63992ed27.jpg",
    "https://telegra.ph/file/9b59c60c1177449cf1862.jpg",
    "https://telegra.ph/file/ea98928adc131f6cc8e02.jpg",
    "https://telegra.ph/file/fc5210fd311649676001e.jpg",
    "https://telegra.ph/file/e26cc4da3a942e7d3bf9b.jpg",
    "https://telegra.ph/file/15991af8e951b8fe7b0a0.jpg",
    "https://telegra.ph/file/501c209015cd1f94b8617.jpg",
    "https://telegra.ph/file/d76336c0df4db81a3c55a.jpg",
    "https://telegra.ph/file/6dc10a65db8501a5ce98f.jpg",
    "https://telegra.ph/file/48b0fd22d60c3a42beb7d.jpg",
    "https://telegra.ph/file/47fa88aa97fe839448d10.jpg",
    "https://telegra.ph/file/2fcdf47b27069d0402cdb.jpg",
    "https://telegra.ph/file/6ecae3c28dd0eec03b51d.jpg",
    "https://telegra.ph/file/236ee7741d4ed04ca7300.jpg",
    "https://telegra.ph/file/5db3111a64e315c13d92b.jpg",
    "https://telegra.ph/file/e58ae01a7bff5d38611db.jpg",
    "https://telegra.ph/file/cba6baabc2684e86b228a.jpg",
    "https://telegra.ph/file/1d44beaf5d566a150e279.jpg",
    "https://telegra.ph/file/4203b9c2c116aec5eec3c.jpg",
    "https://telegra.ph/file/fc9d0b204414165359cfc.jpg",
    "https://telegra.ph/file/2e51e6d7c8df65fd91bf1.jpg",
    "https://telegra.ph/file/174aebe854a2e4d8f8a6f.jpg",
    "https://telegra.ph/file/22a18e6865dcc26538120.jpg",
    "https://telegra.ph/file/3030012526a2ed5f0d91a.jpg",
    "https://telegra.ph/file/2f898543462d0957e70ed.jpg",
    "https://telegra.ph/file/fbb0178d7ea502186d446.jpg",
    "https://telegra.ph/file/8a640765fd218a3d12c51.jpg",
    "https://telegra.ph/file/ebe45a46306aae267ec76.jpg",
    "https://telegra.ph/file/175b25eee8b0284c2a795.jpg",
    "https://telegra.ph/file/01306957538a5ffa280b7.jpg",
    "https://telegra.ph/file/2492cbb35d365fca8572a.jpg",
    "https://telegra.ph/file/29232d5682d28a9c875e6.jpg",
    "https://telegra.ph/file/1fbe6774acc41792e97f0.jpg",
    "https://telegra.ph/file/e5d31b179fb5bd048324c.jpg",
    "https://telegra.ph/file/3d6336b293168a9584cc4.jpg",
    "https://telegra.ph/file/738f9e9e9a01bd22ba87d.jpg",
    "https://telegra.ph/file/62e83ce328210ce0f1fdb.jpg",
    "https://telegra.ph/file/ba72958f67ee8a39fc868.jpg",
    "https://telegra.ph/file/0966abd92bb8f47ffcd90.jpg",
    "https://telegra.ph/file/6c198eb18b599d5163259.jpg",
    "https://telegra.ph/file/90705039f5e995720394f.jpg",
    "https://telegra.ph/file/1591a5f629ff0bc20222c.jpg",
    "https://telegra.ph/file/98584924cc0472f7883e7.jpg",
    "https://telegra.ph/file/70794eb80ed80a5451df1.jpg",
    "https://telegra.ph/file/ac8fa8b4c775ff5ee8f10.jpg",
    "https://telegra.ph/file/43d50381c8f7689140512.jpg",
    "https://telegra.ph/file/0faab7034ca8f8355dacc.jpg",
    "https://telegra.ph/file/dc85d43c4fc5062de7274.jpg",
    "https://telegra.ph/file/db12cf905f557487abc60.jpg",
]


@register(pattern="^/logo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id != OWNER_ID and not quew:
        await event.reply(
            "ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ʟᴏɢᴏ !\nExample : `/logo <ANONYMOUS>`"
        )
        return
    pesan = await event.reply("**ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏɢᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ...**")
    try:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = glob.glob("./TitanXManager/resources/fonts/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "titan.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME})",
        )
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)
    except Exception:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = glob.glob("./TitanXManager/resources/fonts/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "titan.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME})",
        )
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)


__mod_name__ = "◈ 𝐋ᴏɢᴏ ◈"

__help__ = """
I am here to create beautiful and attractive logos for you.

✧ /logo <text>*:* Create a logo with your given text.
"""
