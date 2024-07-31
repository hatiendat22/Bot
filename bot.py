import discord
from discord.ext import commands
import youtube_dl

# Khởi tạo bot với prefix "!"
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Kiểm tra nếu bot đã sẵn sàng
@bot.event
async def on_ready():
    print(f'Bot đã đăng nhập thành {bot.user}')

# Tham gia kênh thoại
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Bạn phải tham gia vào kênh thoại trước!")

# Rời khỏi kênh thoại
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Bot không tham gia vào kênh thoại!")

# Phát nhạc từ YouTube
@bot.command()
async def play(ctx, url):
    if ctx.voice_client:
        ctx.voice_client.stop()
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2)
            ctx.voice_client.play(source)
        await ctx.send(f'Đang phát: {info["title"]}')
    else:
        await ctx.send("Bot chưa tham gia vào kênh thoại!")

# Chạy bot với token
bot.run('MTI2NzM2NjE0MzMxNjg1Njg0Mg.G1tyxM.xUeKfmuMJ2SMf9XiCsxzKH3BOyT5gByz8n4xjI')
    
