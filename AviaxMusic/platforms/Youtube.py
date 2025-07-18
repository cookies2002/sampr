import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

COOKIES_PATH = "AviaxMusic/assets/cookies.txt"

def get_youtube_info(url: str):
    if not os.path.exists(COOKIES_PATH):
        print(f"❌ Cookie file not found: {COOKIES_PATH}")
        return None

    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best",
        "cookiefile": COOKIES_PATH,
        "nocheckcertificate": True,
        "extract_flat": False,
        "forcejson": True,
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "webpage_url": info.get("webpage_url"),
                "audio_url": info.get("url"),
                "id": info.get("id"),
            }
    except DownloadError as e:
        print(f"❌ yt_dlp Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def download_audio(url: str, output_dir="downloads"):
    if not os.path.exists(COOKIES_PATH):
        print(f"❌ Cookie file not found: {COOKIES_PATH}")
        return None

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "cookiefile": COOKIES_PATH,
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
        print("✅ Audio download complete.")
        return True
    except Exception as e:
        print(f"❌ Audio download failed: {e}")
        return False


# 🧪 Test block
if __name__ == "__main__":
    test_url = input("🎵 Enter YouTube video URL to test: ").strip()
    info = get_youtube_info(test_url)
    if info:
        print("🎶 Title:", info['title'])
        print("📻 Audio URL:", info['audio_url'])
        print("📷 Thumbnail:", info['thumbnail'])
        download = input("⏬ Do you want to download the MP3? (y/n): ").strip().lower()
        if download == "y":
            download_audio(test_url)
    else:
        print("❌ Failed to fetch video info.")
        
