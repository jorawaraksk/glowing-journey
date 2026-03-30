#    This file is part of the CompressorQueue distribution.
#    Copyright (c) 2021 Danish_00
#    Script Improved by Anshusharma

from .FastTelethon import download_file, upload_file
from .funcn import *
from .config import *
from telethon import TelegramClient
from telethon.sessions import StringSession
from .db import db
from . import bot
import os

async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, id = wh.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(Path(dl).stat().st_size))
        processing_file_name = dl.replace(f"downloads/", "").replace(f"_", " ")
        ans = f"Processing Media:\n{processing_file_name}\n\nDownloaded:\n{ov}\n\nCompressed:\n{ot}"
        await e.answer(ans, cache_time=0, alert=True)
    except Exception as er:
        LOGS.info(er)
        await e.answer(
            "Someting Went Wrong.\nSend Media Again.", cache_time=0, alert=True
        )

async def dl_link(event):
    if not event.is_private:
        return
    if str(event.sender_id) not in OWNER and event.sender_id !=DEV:
        return
    link, name = "", ""
    try:
        link = event.text.split()[1]
        name = event.text.split()[2]
    except BaseException:
        pass
    if not link:
        return
    if WORKING or QUEUE:
        QUEUE.update({link: name})
        return await event.reply(f"** Added {link} in QUEUE**")
    WORKING.append(1)
    s = dt.now()
    xxx = await event.reply("** Downloading...**")
    try:
        dl = await fast_download(xxx, link, name)
    except Exception as er:
        WORKING.clear()
        LOGS.info(er)
        return
    es = dt.now()
    kk = dl.split("/")[-1]
    aa = kk.split(".")[-1]
    newFile = dl.replace(f"downloads/", "").replace(f"_", " ")
    rr = "encode"
    bb = kk.replace(f".{aa}", ".mkv")
    out = f"{rr}/{bb}"
    thum = "thumb.jpg"
    dtime = ts(int((es - s).seconds) * 1000)
    hehe = f"{out};{dl};0"
    wah = code(hehe)
    nn = await xxx.edit(
        "**🗜 Compressing...**",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL", data=f"skip{wah}")],
        ],
    )
    cmd = f"""ffmpeg -i "{dl}" {ffmpegcode[0]} "{out}" -y"""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await xxx.edit(str(er) + "\n\n**ERROR**")
            WORKING.clear()
            os.remove(dl)
            return os.remove(out)
    except BaseException:
        pass
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await xxx.client.send_message(xxx.chat_id, "** Uploading...**")
    with open(out, "rb") as f:
        ok = await upload_file(
            client=xxx.client,
            file=f,
            name=out,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "** Uploading...**")
            ),
        )
    await nnn.delete()
    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    a1 = await info(dl, xxx)
    a2 = await info(out, xxx)
    dk = f"<b>File Name:</b> {newFile}\n\n<b>Original File Size:</b> {hbs(org)}\n<b>Encoded File Size:</b> {hbs(com)}\n<b>Encoded Percentage:</b> {per}\n\n<b>Get Mediainfo Here:</b> <a href='{a1}'>Before</a>/<a href='{a2}'>After</a>\n\n<i>Downloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}</i>"
    ds = await event.client.send_file(
        event.chat_id, file=ok, force_document=True, caption=dk, link_preview=False, thumb=thum, parse_mode="html"
    )
    os.remove(dl)
    os.remove(out)
    WORKING.clear()

async def encod(event):
    try:
        if not event.is_private:
            return
        if str(event.sender_id) not in OWNER and event.sender_id !=DEV:
            return await event.reply("**Sorry You're not An Authorised User!**")
        if not event.media:
            return
        if hasattr(event.media, "document"):
            if not event.media.document.mime_type.startswith(
                ("video", "application/octet-stream")
            ):
                return
        else:
            return
        if WORKING or QUEUE:
            xxx = await event.reply("**Adding To Queue...**")
            doc = event.media.document
            if doc.id in list(QUEUE.keys()):
                return await xxx.edit("**This File is Already Added in Queue**")
            name = event.file.name
            if not name:
                name = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
            QUEUE.update({doc.id: [name, doc]})
            return await xxx.edit(
                "**Added This File in Queue**"
            )
        WORKING.append(1)
        xxx = await event.reply("** Downloading...**")
        s = dt.now()
        ttt = time.time()
        dir = f"downloads/"
        try:
            if hasattr(event.media, "document"):
                file = event.media.document
                filename = event.file.name
                if not filename:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
                dl = dir + filename
                with open(dl, "wb") as f:
                    ok = await download_file(
                        client=event.client,
                        location=file,
                        out=f,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                xxx,
                                ttt,
                                f"** Downloading**\n__{filename}__",
                            )
                        ),
                    )
            else:
                filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
                dl = await event.client.download_media(
                    event.media,
                    dir,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, xxx, ttt, f"** Downloading**\n__{filename}__")
                    ),
                )
        except Exception as er:
            WORKING.clear()
            LOGS.info(er)
            return os.remove(dl)
        es = dt.now()
        kk = dl.split("/")[-1]
        aa = kk.split(".")[-1]
        rr = f"encode"
        bb = kk.replace(f".{aa}", ".mkv")
        newFile = dl.replace(f"downloads/", "").replace(f"_", " ")
        out = f"{rr}/{bb}"
        thum = "thumb.jpg"
        dtime = ts(int((es - s).seconds) * 1000)
        e = xxx
        hehe = f"{out};{dl};0"
        wah = code(hehe)
        nn = await e.edit(
            "**🗜 Compressing...**",
            buttons=[
                [Button.inline("STATS", data=f"stats{wah}")],
                [Button.inline("CANCEL", data=f"skip{wah}")],
            ],
        )
        cmd = f"""ffmpeg -i "{dl}" {ffmpegcode[0]} "{out}" -y"""
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        er = stderr.decode()
        try:
            if er:
                await e.edit(str(er) + "\n\n**ERROR**")
                WORKING.clear()
                os.remove(dl)
                return os.remove(out)
        except BaseException:
            pass
        ees = dt.now()
        ttt = time.time()
        await nn.delete()
        nnn = await e.client.send_message(e.chat_id, "** Uploading...**")
        with open(out, "rb") as f:
            ok = await upload_file(
                client=e.client,
                file=f,
                name=out,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, nnn, ttt, f"** Uploading**\n__{out.replace(f'encode/', '')}__")
                ),
            )
        await nnn.delete()
        org = int(Path(dl).stat().st_size)
        com = int(Path(out).stat().st_size)
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}") + "%"
        eees = dt.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        a1 = await info(dl, e)
        a2 = await info(out, e)
        dk = f"<b>File Name:</b> {newFile}\n\n<b>Original File Size:</b> {hbs(org)}\n<b>Encoded File Size:</b> {hbs(com)}\n<b>Encoded Percentage:</b> {per}\n\n<b>Get Mediainfo Here:</b> <a href='{a1}'>Before</a>/<a href='{a2}'>After</a>\n\n<i>Downloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}</i>"
        ds = await e.client.send_file(
            e.chat_id, file=ok, force_document=True, caption=dk, link_preview=False, thumb=thum, parse_mode="html"
        )
        os.remove(dl)
        os.remove(out)
        WORKING.clear()
    except BaseException as er:
        LOGS.info(er)
        WORKING.clear()

# ==========================================
# DYNAMIC DB LOGIC FOR RESTRICTED CONTENT SAVING
# ==========================================
async def save_restricted(event):
    if not db:
        return await event.reply("**Database is not connected!**")

    # Fetch the user's session from MongoDB
    user_session_string = await db.get_session(event.sender_id)
    if not user_session_string:
        return await event.reply("**You are not logged in! Please use /login first.**")

    try:
        link = event.text.split()[1]
    except IndexError:
        return await event.reply("**Please provide a link. Usage:** `/save https://t.me/c/123/456`")
    
    msg = await event.reply("`Connecting to your account...`")
    
    # Initialize the temporary client using the session from the DB
    temp_user_client = TelegramClient(StringSession(user_session_string), APP_ID, API_HASH)
    await temp_user_client.connect()
    
    try:
        chat_id = None
        msg_id = None
        
        # Link Parsing Logic
        if "t.me/c/" in link:
            parts = link.split("/")
            chat_id = int("-100" + parts[-2])
            msg_id = int(parts[-1])
        elif "t.me/b/" in link:
            parts = link.split("/")
            chat_id = parts[-2]
            msg_id = int(parts[-1])
        else:
            parts = link.split("/")
            chat_id = parts[-2]
            msg_id = int(parts[-1])
            
        # 1. Fetch message using the USER client (bypasses restrictions)
        message = await temp_user_client.get_messages(chat_id, ids=msg_id)
        if not message:
            await temp_user_client.disconnect()
            return await msg.edit("**Could not fetch the message. Make sure your account is in the channel.**")
            
        await msg.edit("`Downloading restricted content...`")
        
        # 2. Extract and send directly (bypasses FFmpeg compression)
        if message.media:
            # Download via User Client
            file_path = await temp_user_client.download_media(message, file="downloads/")
            
            await msg.edit("`Uploading content to you...`")
            
            # Send to user via Bot Client
            await bot.send_file(
                event.chat_id,
                file_path,
                caption=message.text if message.text else "",
            )
            os.remove(file_path) # Clean up file
            await msg.delete()
        else:
            # If it's just text
            await bot.send_message(event.chat_id, message.text)
            await msg.delete()
            
    except Exception as e:
        await msg.edit(f"**Error:** `{str(e)}`")
    finally:
        await temp_user_client.disconnect()
