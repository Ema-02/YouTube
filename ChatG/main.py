## Rights of the developer Ahmed, do not mess with me and do not change my rights if you want to steal
## Contact me on Telegram @z_o_i , my channel : @cczza

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os, re, yt_dlp, asyncio, wget

@Client.on_message(filters.private & filters.text)
async def main(bot: Client, msg):
	if msg.text == "/start":
		await bot.send_message(msg.chat.id, f"‹ أهلاً بك عزيزي {msg.from_user.mention}\n‹ في بوت التحميل من اليوتيوب 🎙️\n‹ فقط أرسل لي أسم الفيديو أو الأغنية 🔎")
	if msg.text != "/start" and not re.findall(r"(.*?)dl(.*?)", msg.text):
		wait = await bot.send_message(msg.chat.id, f'🔎︙البحث عن "{msg.text}"...')
		search = VideosSearch(msg.text).result()
		txt = ''
		for i in range(9):
			title = search["result"][i]["title"]
			channel = search["result"][i]["channel"]["name"]
			duration = search["result"][i]["duration"]
			views = search["result"][i]["viewCount"]["short"]
			id = search["result"][i]["id"].replace("-","virus")
			txt += f"🎬 [{title}](https://youtu.be/{id})\n👤 {channel}\n🕑 {duration} - 👁 {views}\n🔗 /dl_{id}\n\n"
		await wait.edit(f'🔎︙نتائج البحث لـ "{msg.text}"\n\n{txt}', disable_web_page_preview=True)
	if re.findall(r"(.*?)dl(.*?)", msg.text):
		vid_id = msg.text.replace("virus","-").replace("/dl_","")
		wait = await bot.send_message(msg.chat.id, f'🔎︙البحث عن "https://youtu.be/{vid_id}"...', disable_web_page_preview=True)
		info = YouTube(f"https://youtu.be/{vid_id}")
		keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("مقطع فيديو 🎞",callback_data=f"video&&{vid_id}"),InlineKeyboardButton("ملف صوتي 📼",callback_data=f"audio&&{vid_id}")]])
		await bot.send_photo(msg.chat.id,
		photo=f"https://youtu.be/{vid_id}",
		caption=f"🎬 Name: [{info.title}](https://youtu.be/{vid_id})\n👤 Channel: {info.author}\n👁 Views: {info.views}",
		reply_markup=keyboard
		)
		await wait.delete()

@Client.on_callback_query(filters.regex("&&") , group = 24)
async def download(bot: Client, query: CallbackQuery) :
	video_id = query.data.split("&&")[1]
	if query.data.split("&&")[0] == "video":
		await bot.delete_messages(query.message.chat.id, query.message.id)
		wait = await bot.send_message(query.message.chat.id, "- جار التحميل ...")
		video_link = f"https://youtu.be/{video_id}"
		with yt_dlp.YoutubeDL({"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}) as ytdl:
			info = ytdl.extract_info(video_link, download=False)
			video = ytdl.prepare_filename(info)
			ytdl.process_info(info)
		information = YouTube(video_link)
		thumb = wget.download(information.thumbnail_url)
		await wait.edit("- يتم الرفع ...")
		await bot.send_video(query.message.chat.id,
		video=video,
		duration=information.length,
    	thumb=thumb,
		caption=f"By : @Chkstribot"
		)
		await wait.delete()
		try :
			os.remove(video)
			os.remove(thumb)
		except:
			pass
	if query.data.split("&&")[0] == "audio":
		await bot.delete_messages(query.message.chat.id, query.message.id)
		wait = await bot.send_message(query.message.chat.id, "- جار التحميل ...")
		video_link = f"https://youtu.be/{video_id}"
		with yt_dlp.YoutubeDL({"format": "bestaudio[ext=m4a]"}) as ytdl:
			info = ytdl.extract_info(video_link, download=False)
			audio = ytdl.prepare_filename(info)
			ytdl.process_info(info)
		information = YouTube(video_link)
		thumb = wget.download(information.thumbnail_url)
		await wait.edit("- أنتظر جار الرفع ...")
		await bot.send_audio(query.message.chat.id,
		audio=audio,
		caption=f"By : @Chkstribot",
		title=information.title,
    	duration=information.length,
    	thumb=thumb,
    	performer=information.author
		)
		await wait.delete()
		try :
			os.remove(audio)
			os.remove(thumb)
		except:
			pass
