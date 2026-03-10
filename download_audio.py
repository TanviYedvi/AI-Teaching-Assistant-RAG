import yt_dlp

playlist_url = "https://www.youtube.com/playlist?list=PLTDARY42LDV7WGmlzZtY-w9pemyPrKNUZ"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'video/%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])