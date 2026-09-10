from yt_dlp import  YoutubeDL

url = [""]

opts = {}

with YoutubeDL({
    "format" : "bestaudio/best",
    "postprocessors" : [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',      # extract to mp3
        'preferredquality': '192',    # bitrate in kbps (optional)
    }],
    "outtmpl" : "%(title)s.%(ext)s"
}) as ydl:
    fiel = ydl.download("ytsearch1:Cueshe Pangako lyrics")
